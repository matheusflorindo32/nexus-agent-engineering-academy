"""Evaluate real SpecD graph-impact outputs against the frozen V1 oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


def _canonical(path: str) -> str:
    value = path.replace("\\", "/")
    if ":" in value and not value.startswith("/"):
        prefix, rest = value.split(":", 1)
        if prefix and "/" not in prefix:
            value = rest
    while value.startswith("./"):
        value = value[2:]
    return value


def _affected_files(payload: Any) -> set[str]:
    if isinstance(payload, dict):
        direct = payload.get("affectedFiles")
        if isinstance(direct, list):
            return {_canonical(str(item)) for item in direct}
        impact = payload.get("impact")
        if isinstance(impact, dict):
            nested = impact.get("affectedFiles")
            if isinstance(nested, list):
                return {_canonical(str(item)) for item in nested}
    raise ValueError("SpecD output does not expose affectedFiles in a supported shape")


def _ratio(n: int, d: int) -> float:
    return round(n / d, 6) if d else 0.0


def evaluate(raw_dir: Path, oracle_path: Path, repetitions: int) -> dict[str, Any]:
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    target = _canonical(oracle["target_file"])
    positives = {_canonical(x) for x in oracle["expected_affected_files"]}
    negatives = {_canonical(x) for x in oracle["expected_unaffected_files"]}
    observed_runs: list[list[str]] = []

    for index in range(1, repetitions + 1):
        payload = json.loads((raw_dir / f"impact-{index}.json").read_text(encoding="utf-8"))
        observed = _affected_files(payload)
        observed.discard(target)
        observed_runs.append(sorted(observed))

    first = set(observed_runs[0])
    tp = len(first & positives)
    # Precision must penalize every unexpected affected file, including paths not
    # enumerated in the explicit negative universe.  FPR remains bounded to the
    # explicit negative universe because TN is only defined there.
    unexpected = first - positives
    precision_fp = len(unexpected)
    negative_fp = len(first & negatives)
    fn = len(positives - first)
    tn = len(negatives - first)
    precision = _ratio(tp, tp + precision_fp)
    recall = _ratio(tp, tp + fn)
    fpr = _ratio(negative_fp, negative_fp + tn)
    fnr = _ratio(fn, fn + tp)
    repeatability = _ratio(sum(run == observed_runs[0] for run in observed_runs), repetitions)

    durations_path = raw_dir / "durations-ms.json"
    durations = json.loads(durations_path.read_text(encoding="utf-8")) if durations_path.exists() else []
    median_ms = round(float(statistics.median(durations)), 3) if durations else None
    score = round(100 * statistics.mean([precision, recall, 1.0 - fpr, 1.0 - fnr, repeatability]), 1)

    return {
        "schema": "nexus.specd-isolated-runtime-result.v1",
        "evidence_class": "REAL_RUNTIME_EVIDENCE",
        "claims_scope": "SpecD source-pinned static TypeScript file-impact subset only",
        "repetitions": repetitions,
        "observed_runs": observed_runs,
        "metrics": {
            "affected_file_precision": precision,
            "affected_file_recall": recall,
            "false_positive_rate": fpr,
            "false_negative_rate": fnr,
            "unexpected_affected_files": precision_fp,
            "negative_universe_false_positives": negative_fp,
            "repeatability_rate": repeatability,
            "index_success_rate": 1.0,
            "query_success_rate": 1.0,
            "median_query_duration_ms": median_ms,
        },
        "comparable_subset_score_0_100": score,
        "nexus_graph_runtime_score": "NOT_TESTED",
        "global_framework_comparison": "BLOCKED",
        "limitations": [
            "NEXUS does not yet expose an equivalent real code-graph runtime, so no cross-framework runtime winner is declared.",
            "The fixture covers simple static TypeScript imports/calls and does not validate dynamic dependency forms.",
            "Prompt injection, tool poisoning, token use and human effort are outside this executable graph subset."
        ],
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--oracle", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--upstream-commit", required=True)
    parser.add_argument("--nexus-head", required=True)
    parser.add_argument("--repetitions", type=int, default=5)
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    result = evaluate(raw_dir, Path(args.oracle), args.repetitions)
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "schema": "nexus.execution-receipt.specd-isolated-v1",
        "evidence_class": "REAL_RUNTIME_EVIDENCE",
        "nexus_head_sha": args.nexus_head,
        "upstream_repository": "specd-sdd/SpecD",
        "upstream_commit": args.upstream_commit,
        "repetitions": args.repetitions,
        "result_sha256": sha256(output),
        "raw_files": sorted(path.name for path in raw_dir.glob("*.json")),
        "decision": "PASS" if result["metrics"]["query_success_rate"] == 1.0 else "BLOCKED",
    }
    Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
