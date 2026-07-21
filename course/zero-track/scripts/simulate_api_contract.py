"""Simulador local de contrato HTTP sem rede, credenciais ou efeitos externos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

REDACTED = "[REDACTED]"


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    headers: dict[str, str]
    body: dict[str, Any]


@dataclass(frozen=True)
class Response:
    status: int
    body: dict[str, Any]


def safe_headers(headers: dict[str, str]) -> dict[str, str]:
    """Return headers safe for demonstration logs."""
    return {
        key: REDACTED if key.casefold() in {"authorization", "cookie", "set-cookie"} else value
        for key, value in headers.items()
    }


def handle(request: Request, seen_keys: set[str]) -> Response:
    method = request.method.upper()
    if method != "POST" or request.path != "/v1/tasks":
        return Response(404, {"error": "not_found"})
    if "authorization" not in {key.casefold() for key in request.headers}:
        return Response(401, {"error": "authentication_required"})
    title = request.body.get("title")
    if not isinstance(title, str) or not title.strip():
        return Response(400, {"error": "invalid_title"})
    idempotency_key = request.headers.get("idempotency-key", "")
    if not idempotency_key:
        return Response(400, {"error": "idempotency_key_required"})
    if idempotency_key in seen_keys:
        return Response(409, {"error": "duplicate_operation"})
    seen_keys.add(idempotency_key)
    return Response(201, {"task_id": "task_demo_001", "title": title.strip()})


def main() -> None:
    seen: set[str] = set()
    scenarios = [
        Request("POST", "/v1/tasks", {"content-type": "application/json"}, {"title": "teste"}),
        Request(
            "POST",
            "/v1/tasks",
            {
                "authorization": "Bearer example-value",
                "idempotency-key": "demo-001",
                "content-type": "application/json",
            },
            {"title": "revisar laboratório"},
        ),
        Request(
            "POST",
            "/v1/tasks",
            {
                "authorization": "Bearer example-value",
                "idempotency-key": "demo-001",
            },
            {"title": "revisar laboratório"},
        ),
        Request(
            "POST",
            "/v1/tasks",
            {
                "authorization": "Bearer example-value",
                "idempotency-key": "demo-002",
            },
            {"title": ""},
        ),
    ]

    for index, request in enumerate(scenarios, start=1):
        response = handle(request, seen)
        print(
            {
                "scenario": index,
                "request": {
                    "method": request.method,
                    "path": request.path,
                    "headers": safe_headers(request.headers),
                    "body": request.body,
                },
                "response": {"status": response.status, "body": response.body},
            }
        )


if __name__ == "__main__":
    main()
