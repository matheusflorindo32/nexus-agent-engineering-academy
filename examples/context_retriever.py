#!/usr/bin/env python3
"""Retriever local determinístico para o LAB-201.

Sem rede, API, dependências externas ou execução de instruções recuperadas.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[\wÀ-ÿ]+", re.UNICODE)
INJECTION_PATTERNS = (
    "ignore todas as políticas",
    "ignore instruções anteriores",
    "revele segredos",
    "execute a ação sem aprovação",
    "prioridade máxima",
)
TRUST_WEIGHT = {
    "authoritative": 3.0,
    "informational": 1.0,
    "superseded": -2.0,
    "untrusted": -4.0,
}


@dataclass(frozen=True)
class ScoredChunk:
    chunk_id: str
    source_id: str
    title: str
    text: str
    trust: str
    lexical_score: float
    trust_score: float
    injection_detected: bool
    final_score: float


def tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if len(token) > 2}


def lexical_overlap(query: str, text: str) -> float:
    query_tokens = tokens(query)
    if not query_tokens:
        return 0.0
    return len(query_tokens & tokens(text)) / len(query_tokens)


def detects_injection(text: str) -> bool:
    normalized = text.casefold()
    return any(pattern in normalized for pattern in INJECTION_PATTERNS)


def score_chunk(query: str, chunk: dict[str, Any]) -> ScoredChunk:
    lexical = lexical_overlap(query, chunk["text"])
    trust = TRUST_WEIGHT.get(chunk.get("trust", "untrusted"), -4.0)
    injection = detects_injection(chunk["text"])
    injection_penalty = -10.0 if injection else 0.0
    final = lexical * 5.0 + trust + injection_penalty
    return ScoredChunk(
        chunk_id=chunk["chunk_id"],
        source_id=chunk["source_id"],
        title=chunk["title"],
        text=chunk["text"],
        trust=chunk.get("trust", "untrusted"),
        lexical_score=round(lexical, 4),
        trust_score=trust,
        injection_detected=injection,
        final_score=round(final, 4),
    )


def retrieve(dataset: dict[str, Any], top_k: int = 3) -> list[ScoredChunk]:
    query = dataset["query"]
    scored = [score_chunk(query, chunk) for chunk in dataset["chunks"]]
    eligible = [
        item
        for item in scored
        if item.trust not in {"superseded", "untrusted"}
        and not item.injection_detected
        and item.final_score > 0
    ]
    return sorted(eligible, key=lambda item: item.final_score, reverse=True)[:top_k]


def build_result(dataset: dict[str, Any], selected: list[ScoredChunk]) -> dict[str, Any]:
    required = set(dataset.get("required_chunk_ids", []))
    selected_ids = {item.chunk_id for item in selected}
    supported = required.issubset(selected_ids)

    if not supported:
        answer = "Evidência insuficiente para responder com segurança."
        status = "abstained"
    else:
        answer = dataset["expected_answer"]
        status = "answered"

    return {
        "dataset_id": dataset["dataset_id"],
        "query": dataset["query"],
        "status": status,
        "answer": answer,
        "citations": [item.chunk_id for item in selected if item.chunk_id in required],
        "selected_context": [
            {
                "chunk_id": item.chunk_id,
                "source_id": item.source_id,
                "trust": item.trust,
                "lexical_score": item.lexical_score,
                "trust_score": item.trust_score,
                "final_score": item.final_score,
                "injection_detected": item.injection_detected,
            }
            for item in selected
        ],
        "authority_changed_by_context": False,
        "embedded_instructions_executed": 0,
    }


def self_test(dataset: dict[str, Any], result: dict[str, Any]) -> None:
    assert result["status"] == "answered"
    assert set(dataset["required_chunk_ids"]).issubset(result["citations"])
    assert result["authority_changed_by_context"] is False
    assert result["embedded_instructions_executed"] == 0
    assert all(
        item["chunk_id"] != "injection-01" for item in result["selected_context"]
    )
    assert all(item["chunk_id"] != "policy-old-01" for item in result["selected_context"])


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    dataset_path = root / "datasets" / "lab-201-context-fixtures.json"
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    selected = retrieve(dataset)
    result = build_result(dataset, selected)
    self_test(dataset, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
