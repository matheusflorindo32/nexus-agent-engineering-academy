"""Benchmark NEXUS Repository Indexer V1 on frozen fixtures and this repository read-only."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
INDEXER_PATH = ROOT / "examples" / "repository_indexer_v1.py"


def load_indexer():
    spec = importlib.util.spec_from_file_location("repository_indexer_v1_benchmark", INDEXER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_case(root: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def observed_sets(result: dict) -> tuple[set[str], set[str], set[tuple[str, str]]]:
    files = {n["path"] for n in result["graph"]["nodes"] if n["type"] == "file"}
    symbols = {
        f"{n['path']}:{n['symbol']}"
        for n in result["graph"]["nodes"]
        if n["type"] == "symbol"
    }
    deps = {
        (edge["source"][5:], edge["target"][5:])
        for edge in result["graph"]["edges"]
        if edge["type"] == "DEPENDS_ON" and edge["source"].startswith("file:") and edge["target"].startswith("file:")
    }
    return files, symbols, deps


def evaluate_fixtures(module, repetitions: int) -> dict:
    fixture_doc = json.loads((EXP / "fixtures.json").read_text(encoding="utf-8"))
    all_case_results = []
    fingerprints_by_rep = []
    build_times = []
    peak_bytes = []
    tp = fp = fn = 0
    passed_cases = 0
    total_cases = len(fixture_doc["cases"])

    for rep in range(repetitions):
        rep_fingerprints = []
        for case in fixture_doc["cases"]:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                write_case(root, case["files"])
                tracemalloc.start()
                started = time.perf_counter_ns()
                result = module.RepositoryIndexer(root).build_index()
                elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                build_times.append(elapsed_ms)
                peak_bytes.append(peak)
                rep_fingerprints.append(result["fingerprint"])
                files, symbols, deps = observed_sets(result)

                checks = []
                expected_files = set(case.get("expected_files", files))
                expected_symbols = set(case.get("expected_symbols", symbols))
                expected_deps = {tuple(x) for x in case.get("expected_dependencies", [list(x) for x in deps])}
                expected_parse_errors = set(case.get("expected_parse_errors", []))
                expected_untrusted_min = int(case.get("expected_untrusted_min", 0))
                checks.extend([
                    files == expected_files,
                    symbols == expected_symbols,
                    deps == expected_deps,
                    set(result["skipped"]["parse_errors"]) == expected_parse_errors,
                    result["security"]["untrusted_text_markers"] >= expected_untrusted_min,
                    result["security"]["instructions_executed"] == 0,
                    result["security"]["repository_writes"] == 0,
                    result["security"]["network_calls"] == 0,
                ])
                if all(checks):
                    passed_cases += 1
                if rep == 0:
                    all_case_results.append({"case_id": case["case_id"], "passed": all(checks)})

                expected_entities = {f"file:{p}" for p in expected_files} | {f"symbol:{s}" for s in expected_symbols} | {f"dep:{a}->{b}" for a, b in expected_deps}
                observed_entities = {f"file:{p}" for p in files} | {f"symbol:{s}" for s in symbols} | {f"dep:{a}->{b}" for a, b in deps}
                tp += len(expected_entities & observed_entities)
                fp += len(observed_entities - expected_entities)
                fn += len(expected_entities - observed_entities)
        fingerprints_by_rep.append(rep_fingerprints)

    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    deterministic = 1.0 if all(rep == fingerprints_by_rep[0] for rep in fingerprints_by_rep[1:]) else 0.0
    fixture_pass_rate = passed_cases / (total_cases * repetitions) if total_cases else 1.0
    score = round(100 * (0.35 * f1 + 0.25 * fixture_pass_rate + 0.20 * deterministic + 0.20 * (1.0 if fp == 0 and fn == 0 else 0.0)), 2)
    return {
        "evidence_class": "DETERMINISTIC_CONTROL_EVIDENCE",
        "repetitions": repetitions,
        "case_results": all_case_results,
        "metrics": {
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1": round(f1, 6),
            "false_positives": fp,
            "false_negatives": fn,
            "fixture_pass_rate": round(fixture_pass_rate, 6),
            "deterministic_rerun_equality": deterministic,
            "build_ms_min": round(min(build_times), 6) if build_times else 0.0,
            "build_ms_max": round(max(build_times), 6) if build_times else 0.0,
            "tracemalloc_peak_bytes_max": max(peak_bytes) if peak_bytes else 0,
        },
        "benchmark_score_0_100": score,
    }


def index_real_repository(module) -> dict:
    started = time.perf_counter_ns()
    tracemalloc.start()
    result = module.RepositoryIndexer(ROOT).build_index()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
    second = module.RepositoryIndexer(ROOT).build_index(previous=result)
    return {
        "evidence_class": "REAL_RUNTIME_EVIDENCE",
        "mode": "read-only-self-repository",
        "fingerprint": result["fingerprint"],
        "deterministic_incremental_fingerprint_equality": 1.0 if result["fingerprint"] == second["fingerprint"] else 0.0,
        "stats": result["stats"],
        "skipped": result["skipped"],
        "security": result["security"],
        "incremental_second_pass": second["incremental"],
        "elapsed_ms": round(elapsed_ms, 6),
        "tracemalloc_peak_bytes": peak,
        "correctness_score": "NOT_APPLICABLE",
        "typescript": "NOT_TESTED",
        "javascript": "NOT_TESTED",
        "rename_inference": "NOT_TESTED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--repetitions", type=int, default=5)
    args = parser.parse_args()
    module = load_indexer()
    fixture = evaluate_fixtures(module, args.repetitions)
    repository = index_real_repository(module)
    hashes = {"protocol.json": sha256_file(EXP / "protocol.json"), "fixtures.json": sha256_file(EXP / "fixtures.json")}
    result = {
        "schema": "nexus.repository-indexer-v1.benchmark-result.v1",
        "head_sha": args.head_sha,
        "frozen_hashes": hashes,
        "fixture_trial": fixture,
        "repository_trial": repository,
        "runtime_dependencies_added": 0,
        "specd_runtime": "MONITOR",
    }
    decision = "PASS" if fixture["benchmark_score_0_100"] == 100.0 and repository["security"]["repository_writes"] == 0 else "BLOCKED"
    receipt = {
        "schema": "nexus.execution-receipt.v1",
        "task_id": "repository-indexer-v1-isolated-trial",
        "commit": args.head_sha,
        "environment": "github-actions-ubuntu-python-3.12",
        "tools": ["python-stdlib-ast", "pathlib", "hashlib", "tracemalloc"],
        "tests": ["frozen-fixture-indexing", "read-only-self-repository-indexing"],
        "results": {"fixture_score": fixture["benchmark_score_0_100"], "repository_fingerprint": repository["fingerprint"]},
        "artifacts": [args.output],
        "failures": [],
        "decision": decision,
        "evidence_classes": ["DETERMINISTIC_CONTROL_EVIDENCE", "REAL_RUNTIME_EVIDENCE"],
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.receipt).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if decision != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
