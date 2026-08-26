"""NEXUS Hardening V2 reliability and action-integrity reference runtime.

Stdlib-only, deterministic, and side-effect free. It models four controls:
- terminal transport failure propagation with bounded waits;
- scoped HITL state transitions;
- idempotent side-effect execution with receipts;
- staged Skill promotion with integrity hashes and atomic rename.

It is a teaching/reference artifact, not a production transaction engine.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
from pathlib import Path
import json
import os
import tempfile
import threading
import time
from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class TransportClosed(RuntimeError):
    """Raised when a terminal transport error makes future responses impossible."""


class BoundedChannel(Generic[T]):
    """Condition-backed queue that persists terminal failure for future readers."""

    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._items: list[T] = []
        self._terminal_error: BaseException | None = None
        self._cancelled = False

    def put(self, item: T) -> None:
        with self._condition:
            if self._terminal_error is not None or self._cancelled:
                raise TransportClosed("channel is not writable")
            self._items.append(item)
            self._condition.notify_all()

    def fail(self, error: BaseException) -> None:
        with self._condition:
            if self._terminal_error is None:
                self._terminal_error = error
            self._condition.notify_all()

    def cancel(self) -> None:
        with self._condition:
            self._cancelled = True
            self._condition.notify_all()

    def get(self, timeout_seconds: float) -> T:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        deadline = time.monotonic() + timeout_seconds
        with self._condition:
            while True:
                if self._items:
                    return self._items.pop(0)
                if self._terminal_error is not None:
                    raise TransportClosed(str(self._terminal_error)) from self._terminal_error
                if self._cancelled:
                    raise TransportClosed("channel cancelled")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("bounded wait expired")
                self._condition.wait(remaining)


@dataclass(frozen=True)
class Approval:
    approval_id: str
    operation_id: str
    principal: str
    approved: bool


@dataclass(frozen=True)
class ExecutionReceipt:
    operation_id: str
    tool_name: str
    principal: str
    status: str
    requested_at: float
    approved_at: float | None = None
    executed_at: float | None = None
    verified_at: float | None = None
    resource_id: str | None = None
    result_hash: str | None = None
    retry_count: int = 0


class ActionLedger:
    """In-memory reference ledger for approval, idempotency and verification."""

    def __init__(self) -> None:
        self._receipts: dict[str, ExecutionReceipt] = {}
        self._approvals: dict[str, Approval] = {}

    def request(self, operation_id: str, tool_name: str, principal: str) -> ExecutionReceipt:
        existing = self._receipts.get(operation_id)
        if existing is not None:
            return existing
        receipt = ExecutionReceipt(
            operation_id=operation_id,
            tool_name=tool_name,
            principal=principal,
            status="REQUESTED",
            requested_at=time.time(),
        )
        self._receipts[operation_id] = receipt
        return receipt

    def approve(self, approval: Approval) -> ExecutionReceipt:
        receipt = self._require(approval.operation_id)
        if approval.principal != receipt.principal:
            raise PermissionError("approval principal does not match operation principal")
        if not approval.approved:
            denied = replace(receipt, status="DENIED")
            self._receipts[receipt.operation_id] = denied
            return denied
        self._approvals[approval.operation_id] = approval
        approved = replace(receipt, status="APPROVED", approved_at=time.time())
        self._receipts[receipt.operation_id] = approved
        return approved

    def execute_once(
        self,
        operation_id: str,
        tool_name: str,
        effect: Callable[[], tuple[str, object]],
        *,
        require_approval: bool = True,
    ) -> ExecutionReceipt:
        receipt = self._require(operation_id)
        if receipt.tool_name != tool_name:
            raise ValueError("tool does not match requested operation")
        if receipt.status in {"EXECUTED", "VERIFIED"}:
            return replace(receipt, retry_count=receipt.retry_count + 1)
        if require_approval and operation_id not in self._approvals:
            raise PermissionError("operation has no scoped approval")
        if receipt.status == "DENIED":
            raise PermissionError("operation was denied")
        resource_id, result = effect()
        digest = sha256(json.dumps(result, sort_keys=True, default=str).encode()).hexdigest()
        executed = replace(
            receipt,
            status="EXECUTED",
            executed_at=time.time(),
            resource_id=resource_id,
            result_hash=f"sha256:{digest}",
        )
        self._receipts[operation_id] = executed
        return executed

    def verify(self, operation_id: str, resource_id: str) -> ExecutionReceipt:
        receipt = self._require(operation_id)
        if receipt.status != "EXECUTED":
            raise RuntimeError("only executed operations can be verified")
        if receipt.resource_id != resource_id:
            raise RuntimeError("verification resource does not match execution receipt")
        verified = replace(receipt, status="VERIFIED", verified_at=time.time())
        self._receipts[operation_id] = verified
        return verified

    def receipt(self, operation_id: str) -> ExecutionReceipt:
        return self._require(operation_id)

    def _require(self, operation_id: str) -> ExecutionReceipt:
        try:
            return self._receipts[operation_id]
        except KeyError as exc:
            raise KeyError(f"unknown operation_id: {operation_id}") from exc


class SkillIntegrityError(RuntimeError):
    """Raised when staged Skill content does not match declared integrity."""


class SkillRegistry:
    """Filesystem reference for immutable staged Skill promotion."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.staging = root / ".staging"
        self.versions = root / "versions"
        self.current = root / "current"
        for directory in (self.staging, self.versions, self.current):
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def digest(content: str) -> str:
        return "sha256:" + sha256(content.encode("utf-8")).hexdigest()

    def stage(self, name: str, version: str, skill_md: str) -> tuple[Path, str]:
        target = self.staging / name / version
        target.mkdir(parents=True, exist_ok=False)
        path = target / "SKILL.md"
        path.write_text(skill_md, encoding="utf-8")
        digest = self.digest(skill_md)
        (target / "CONTENT.SHA256").write_text(digest + "\n", encoding="utf-8")
        return target, digest

    def promote(self, name: str, version: str, expected_digest: str) -> Path:
        staged = self.staging / name / version
        skill_path = staged / "SKILL.md"
        if not skill_path.is_file():
            raise SkillIntegrityError("staged SKILL.md missing")
        actual = self.digest(skill_path.read_text(encoding="utf-8"))
        if actual != expected_digest:
            raise SkillIntegrityError("Skill content hash mismatch")
        destination = self.versions / name / version
        destination.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staged, destination)
        pointer_tmp = self.current / f".{name}.tmp"
        pointer = self.current / f"{name}.json"
        pointer_tmp.write_text(
            json.dumps({"name": name, "version": version, "digest": actual}, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(pointer_tmp, pointer)
        return destination


TRUST_LEVELS = {
    "T0": 0,
    "T1": 1,
    "T2": 2,
    "T3": 3,
    "T4": 4,
    "T5": 5,
    "T6": 6,
    "T7": 7,
}


def may_override(source_level: str, target_level: str) -> bool:
    """Return False when a lower-trust source attempts to override higher trust."""
    return TRUST_LEVELS[source_level] <= TRUST_LEVELS[target_level]


def run_self_tests() -> int:
    checks: list[tuple[str, bool]] = []

    channel: BoundedChannel[str] = BoundedChannel()
    channel.fail(ConnectionError("transport lost"))
    try:
        channel.get(0.01)
    except TransportClosed:
        checks.append(("terminal failure propagates to future reader", True))
    else:
        checks.append(("terminal failure propagates to future reader", False))

    ledger = ActionLedger()
    ledger.request("op-1", "publish", "human-1")
    ledger.approve(Approval("approval-1", "op-1", "human-1", True))
    calls = {"count": 0}

    def effect() -> tuple[str, object]:
        calls["count"] += 1
        return "resource-1", {"ok": True}

    ledger.execute_once("op-1", "publish", effect)
    ledger.execute_once("op-1", "publish", effect)
    verified = ledger.verify("op-1", "resource-1")
    checks.append(("idempotent side effect", calls["count"] == 1))
    checks.append(("verified receipt", verified.status == "VERIFIED"))

    with tempfile.TemporaryDirectory() as tmp:
        registry = SkillRegistry(Path(tmp))
        _, digest = registry.stage("reviewer", "1.0.0", "# Skill\nSafe content\n")
        promoted = registry.promote("reviewer", "1.0.0", digest)
        checks.append(("atomic skill promotion", (promoted / "SKILL.md").is_file()))

    checks.append(("untrusted MCP cannot override T1", not may_override("T6", "T1")))

    failed = [name for name, passed in checks if not passed]
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'} - {name}")
    print(json.dumps({"passed": len(checks) - len(failed), "total": len(checks), "failed": failed}))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_self_tests())
