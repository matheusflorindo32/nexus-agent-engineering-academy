"""Safe local tool boundary with preview, approval hash and idempotency."""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import hashlib
import json

ALLOWED_ACTIONS = {"label_record", "archive_record"}
ALLOWED_SCOPES = {"training"}


class ToolError(Exception):
    code = "tool_error"


class ValidationError(ToolError):
    code = "validation_error"


class AuthorizationError(ToolError):
    code = "authorization_error"


class ApprovalError(ToolError):
    code = "approval_error"


class IdempotencyConflict(ToolError):
    code = "idempotency_conflict"


@dataclass(frozen=True)
class Request:
    action: str
    record_id: str
    scope: str
    label: str | None = None
    idempotency_key: str = ""
    dry_run: bool = True

    def validate(self) -> None:
        if self.action not in ALLOWED_ACTIONS:
            raise ValidationError("action not allowed")
        if self.scope not in ALLOWED_SCOPES:
            raise AuthorizationError("scope not allowed")
        if not self.record_id.startswith("rec-"):
            raise ValidationError("invalid record_id")
        if self.action == "label_record" and not self.label:
            raise ValidationError("label required")
        if len(self.idempotency_key) < 8:
            raise ValidationError("idempotency_key too short")

    def canonical(self) -> str:
        return json.dumps({
            "action": self.action,
            "record_id": self.record_id,
            "scope": self.scope,
            "label": self.label,
            "idempotency_key": self.idempotency_key,
        }, sort_keys=True, separators=(",", ":"))


class SafeTool:
    def __init__(self) -> None:
        self._idempotency: dict[str, str] = {}
        self._effects: list[dict[str, str | None]] = []

    @staticmethod
    def preview_hash(request: Request) -> str:
        return hashlib.sha256(request.canonical().encode()).hexdigest()

    def preview(self, request: Request) -> dict[str, object]:
        request.validate()
        return {
            "effect": request.action,
            "target": request.record_id,
            "scope": request.scope,
            "label": request.label,
            "preview_hash": self.preview_hash(request),
            "requires_approval": not request.dry_run,
        }

    def execute(self, request: Request, approval_hash: str | None = None) -> dict[str, object]:
        preview = self.preview(request)
        payload_hash = self.preview_hash(request)
        prior = self._idempotency.get(request.idempotency_key)
        if prior and prior != payload_hash:
            raise IdempotencyConflict("key reused with different payload")
        if prior:
            return {"status": "reconciled", "duplicate_effect": False, "preview": preview}
        if request.dry_run:
            return {"status": "preview", "duplicate_effect": False, "preview": preview}
        if approval_hash != payload_hash:
            raise ApprovalError("approval does not match current preview")
        self._idempotency[request.idempotency_key] = payload_hash
        self._effects.append({
            "action": request.action,
            "record_id": request.record_id,
            "label": request.label,
        })
        return {"status": "executed", "duplicate_effect": False, "preview": preview}


def self_test() -> None:
    tool = SafeTool()
    request = Request("label_record", "rec-001", "training", "reviewed", "idem-0001", False)
    digest = tool.preview_hash(request)
    first = tool.execute(request, digest)
    second = tool.execute(request, digest)
    assert first["status"] == "executed"
    assert second["status"] == "reconciled"
    assert len(tool._effects) == 1
    try:
        tool.execute(Request("shell", "rec-001", "training", None, "idem-0002", True))
    except ValidationError:
        pass
    else:
        raise AssertionError("wide action accepted")
    try:
        changed = Request("label_record", "rec-001", "training", "changed", "idem-0001", False)
        tool.execute(changed, tool.preview_hash(changed))
    except IdempotencyConflict:
        pass
    else:
        raise AssertionError("idempotency conflict not detected")
    print("safe_tool_boundary self-test passed: 0 duplicate effects; hostile cases blocked")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    tool = SafeTool()
    request = Request("label_record", "rec-001", "training", "reviewed", "idem-demo", True)
    print(json.dumps(tool.execute(request), indent=2))


if __name__ == "__main__":
    main()
