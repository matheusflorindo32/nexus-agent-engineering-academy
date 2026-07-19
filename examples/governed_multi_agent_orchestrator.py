#!/usr/bin/env python3
"""Governed, deterministic multi-agent orchestration reference.

Uses only the Python standard library. It demonstrates contracts, scoped
handoffs, integrity hashes, cycle detection, authority checks, partial-failure
recovery and a local self-test suite. It does not call models or networks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StopReason(str, Enum):
    COMPLETE = "complete"
    UNKNOWN_AGENT = "unknown_agent"
    AUTHORITY_VIOLATION = "authority_violation"
    CYCLE_DETECTED = "cycle_detected"
    BUDGET_EXHAUSTED = "budget_exhausted"
    SCOPE_VIOLATION = "scope_violation"
    SCHEMA_INVALID = "schema_invalid"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    APPROVAL_REQUIRED = "approval_required"
    INTEGRITY_FAILURE = "integrity_failure"
    PARTIAL_FAILURE = "partial_failure"


@dataclass(frozen=True)
class Scope:
    tenant_id: str
    project_id: str
    run_id: str


@dataclass(frozen=True)
class AgentContract:
    agent_id: str
    capabilities: frozenset[str]
    allowed_tools: frozenset[str] = frozenset()
    may_delegate_to: frozenset[str] = frozenset()
    may_approve_effects: bool = False


@dataclass(frozen=True)
class Delegation:
    delegation_id: str
    sender: str
    receiver: str
    objective: str
    capability: str
    scope: Scope
    parent_id: str | None = None

    def digest(self) -> str:
        payload = json.dumps(
            {
                "delegation_id": self.delegation_id,
                "sender": self.sender,
                "receiver": self.receiver,
                "objective": self.objective,
                "capability": self.capability,
                "scope": self.scope.__dict__,
                "parent_id": self.parent_id,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode()).hexdigest()


@dataclass
class Artifact:
    artifact_id: str
    kind: str
    content: dict[str, Any]
    producer: str
    scope: Scope
    valid: bool = True


@dataclass
class RunReport:
    reason: StopReason
    handoffs: int
    trace: list[dict[str, Any]]
    artifacts: list[Artifact]
    detail: str = ""


@dataclass
class Orchestrator:
    contracts: dict[str, AgentContract]
    scope: Scope
    max_handoffs: int = 6
    trace: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    seen_edges: set[tuple[str, str]] = field(default_factory=set)
    delegation_hashes: dict[str, str] = field(default_factory=dict)
    handoffs: int = 0

    def _stop(self, reason: StopReason, detail: str = "") -> RunReport:
        self.trace.append({"event": "stop", "reason": reason.value, "detail": detail})
        return RunReport(reason, self.handoffs, list(self.trace), list(self.artifacts), detail)

    def delegate(self, delegation: Delegation, supplied_hash: str | None = None) -> RunReport | None:
        if delegation.scope != self.scope:
            return self._stop(StopReason.SCOPE_VIOLATION, "handoff crossed scope")
        sender = self.contracts.get(delegation.sender)
        receiver = self.contracts.get(delegation.receiver)
        if sender is None or receiver is None:
            return self._stop(StopReason.UNKNOWN_AGENT, delegation.receiver)
        if delegation.receiver not in sender.may_delegate_to:
            return self._stop(StopReason.AUTHORITY_VIOLATION, "sender cannot delegate to receiver")
        if delegation.capability not in receiver.capabilities:
            return self._stop(StopReason.AUTHORITY_VIOLATION, "receiver lacks capability")
        if self.handoffs >= self.max_handoffs:
            return self._stop(StopReason.BUDGET_EXHAUSTED, "max_handoffs")
        edge = (delegation.sender, delegation.receiver)
        reverse = (delegation.receiver, delegation.sender)
        if edge in self.seen_edges or reverse in self.seen_edges:
            return self._stop(StopReason.CYCLE_DETECTED, f"edge {edge}")
        digest = delegation.digest()
        prior = self.delegation_hashes.get(delegation.delegation_id)
        if supplied_hash is not None and supplied_hash != digest:
            return self._stop(StopReason.INTEGRITY_FAILURE, "hash mismatch")
        if prior is not None and prior != digest:
            return self._stop(StopReason.INTEGRITY_FAILURE, "delegation id reused")
        self.delegation_hashes[delegation.delegation_id] = digest
        self.seen_edges.add(edge)
        self.handoffs += 1
        self.trace.append({"event": "delegate", "id": delegation.delegation_id, "edge": edge, "hash": digest})
        return None

    def use_tool(self, agent_id: str, tool: str) -> RunReport | None:
        contract = self.contracts[agent_id]
        if tool not in contract.allowed_tools:
            return self._stop(StopReason.AUTHORITY_VIOLATION, f"{agent_id}:{tool}")
        self.trace.append({"event": "tool", "agent": agent_id, "tool": tool})
        return None

    def add_artifact(self, artifact: Artifact) -> RunReport | None:
        if artifact.scope != self.scope:
            return self._stop(StopReason.SCOPE_VIOLATION, "artifact crossed scope")
        self.artifacts.append(artifact)
        self.trace.append({"event": "artifact", "id": artifact.artifact_id, "valid": artifact.valid})
        return None

    def review(self, artifact: Artifact, evidence_required: int = 1) -> RunReport | None:
        required = {"title", "body", "evidence"}
        if set(artifact.content) != required or not isinstance(artifact.content["evidence"], list):
            return self._stop(StopReason.SCHEMA_INVALID, artifact.artifact_id)
        if len(artifact.content["evidence"]) < evidence_required:
            return self._stop(StopReason.INSUFFICIENT_EVIDENCE, artifact.artifact_id)
        self.trace.append({"event": "review_pass", "artifact": artifact.artifact_id})
        return None

    def request_effect(self, approver: str | None) -> RunReport | None:
        if approver is None or not self.contracts.get(approver, AgentContract("", frozenset())).may_approve_effects:
            return self._stop(StopReason.APPROVAL_REQUIRED, "human approval missing")
        self.trace.append({"event": "approved", "by": approver})
        return None

    def complete(self) -> RunReport:
        return self._stop(StopReason.COMPLETE, "governed run complete")


def contracts() -> dict[str, AgentContract]:
    return {
        "supervisor": AgentContract("supervisor", frozenset({"route"}), may_delegate_to=frozenset({"researcher", "writer", "reviewer"})),
        "researcher": AgentContract("researcher", frozenset({"research"}), allowed_tools=frozenset({"local_reference_index"})),
        "writer": AgentContract("writer", frozenset({"write"}), may_delegate_to=frozenset({"reviewer"})),
        "reviewer": AgentContract("reviewer", frozenset({"review"})),
        "human_approver": AgentContract("human_approver", frozenset({"approve"}), may_approve_effects=True),
    }


def fresh(max_handoffs: int = 6) -> Orchestrator:
    return Orchestrator(contracts(), Scope("tenant-a", "project-a", "run-1"), max_handoffs=max_handoffs)


def valid_delegation(identifier: str, receiver: str, capability: str, sender: str = "supervisor") -> Delegation:
    return Delegation(identifier, sender, receiver, "bounded task", capability, Scope("tenant-a", "project-a", "run-1"))


def self_test() -> None:
    # M1 valid governed run
    o = fresh()
    assert o.delegate(valid_delegation("d1", "researcher", "research")) is None
    assert o.use_tool("researcher", "local_reference_index") is None
    research = Artifact("a1", "facts", {"facts": ["local fact"]}, "researcher", o.scope)
    assert o.add_artifact(research) is None
    assert o.delegate(valid_delegation("d2", "writer", "write")) is None
    draft = Artifact("a2", "draft", {"title": "T", "body": "B", "evidence": ["a1"]}, "writer", o.scope)
    assert o.add_artifact(draft) is None
    assert o.delegate(valid_delegation("d3", "reviewer", "review", sender="writer")) is None
    assert o.review(draft) is None
    assert o.complete().reason == StopReason.COMPLETE

    # M2 unknown agent
    o = fresh(); assert o.delegate(valid_delegation("d", "ghost", "x")).reason == StopReason.UNKNOWN_AGENT
    # M3 unauthorized tool
    o = fresh(); assert o.use_tool("writer", "shell").reason == StopReason.AUTHORITY_VIOLATION
    # M4 cycle
    o = fresh(); assert o.delegate(valid_delegation("d1", "writer", "write")) is None
    assert o.delegate(valid_delegation("d2", "supervisor", "route", sender="writer")).reason == StopReason.AUTHORITY_VIOLATION
    o.contracts["writer"] = AgentContract("writer", frozenset({"write"}), may_delegate_to=frozenset({"supervisor"}))
    assert o.delegate(valid_delegation("d3", "supervisor", "route", sender="writer")).reason == StopReason.CYCLE_DETECTED
    # M5 handoff budget
    o = fresh(max_handoffs=0); assert o.delegate(valid_delegation("d", "writer", "write")).reason == StopReason.BUDGET_EXHAUSTED
    # M6 scope isolation
    o = fresh(); bad = Delegation("d", "supervisor", "writer", "x", "write", Scope("tenant-b", "project-a", "run-1"))
    assert o.delegate(bad).reason == StopReason.SCOPE_VIOLATION
    # M7 schema invalid
    o = fresh(); malformed = Artifact("a", "draft", {"body": "x"}, "writer", o.scope)
    assert o.review(malformed).reason == StopReason.SCHEMA_INVALID
    # M8 valid artifact survives partial failure
    o = fresh(); artifact = Artifact("a", "facts", {"facts": ["ok"]}, "researcher", o.scope)
    assert o.add_artifact(artifact) is None
    report = o._stop(StopReason.PARTIAL_FAILURE, "worker timeout")
    assert any(a.artifact_id == "a" for a in report.artifacts)
    # M9 insufficient evidence
    o = fresh(); weak = Artifact("a", "draft", {"title": "t", "body": "b", "evidence": []}, "writer", o.scope)
    assert o.review(weak).reason == StopReason.INSUFFICIENT_EVIDENCE
    # M10 approval gate
    o = fresh(); assert o.request_effect(None).reason == StopReason.APPROVAL_REQUIRED
    # M11 integrity
    o = fresh(); d = valid_delegation("d", "writer", "write")
    assert o.delegate(d, supplied_hash="tampered").reason == StopReason.INTEGRITY_FAILURE
    # M12 architecture comparison is explicit and conservative
    single = {"quality": 1.0, "coordination_cost": 0, "steps": 3}
    multi = {"quality": 1.0, "coordination_cost": 3, "steps": 6}
    recommendation = "single_agent" if multi["quality"] <= single["quality"] and multi["coordination_cost"] > 0 else "multi_agent"
    assert recommendation == "single_agent"

    print("PASS: 12 governed multi-agent scenarios")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print("Run with --self-test")


if __name__ == "__main__":
    main()
