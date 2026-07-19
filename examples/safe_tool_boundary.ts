type Action = "label_record" | "archive_record";
type Scope = "training";

type Request = {
  action: Action;
  recordId: string;
  scope: Scope;
  label?: string;
  idempotencyKey: string;
  dryRun: boolean;
};

type Preview = {
  effect: Action;
  target: string;
  scope: Scope;
  label?: string;
  previewHash: string;
  requiresApproval: boolean;
};

class ToolError extends Error {
  constructor(public readonly code: string, message: string) {
    super(message);
  }
}

function stablePayload(request: Request): string {
  return JSON.stringify({
    action: request.action,
    idempotencyKey: request.idempotencyKey,
    label: request.label ?? null,
    recordId: request.recordId,
    scope: request.scope,
  });
}

async function sha256(value: string): Promise<string> {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

class SafeToolBoundary {
  private readonly idempotency = new Map<string, string>();
  private readonly effects: Array<{ action: Action; recordId: string; label?: string }> = [];

  private validate(request: Request): void {
    if (!request.recordId.startsWith("rec-")) {
      throw new ToolError("validation_error", "invalid recordId");
    }
    if (request.action === "label_record" && !request.label) {
      throw new ToolError("validation_error", "label required");
    }
    if (request.idempotencyKey.length < 8) {
      throw new ToolError("validation_error", "idempotencyKey too short");
    }
  }

  async preview(request: Request): Promise<Preview> {
    this.validate(request);
    return {
      effect: request.action,
      target: request.recordId,
      scope: request.scope,
      label: request.label,
      previewHash: await sha256(stablePayload(request)),
      requiresApproval: !request.dryRun,
    };
  }

  async execute(request: Request, approvalHash?: string): Promise<Record<string, unknown>> {
    const preview = await this.preview(request);
    const payloadHash = preview.previewHash;
    const prior = this.idempotency.get(request.idempotencyKey);

    if (prior && prior !== payloadHash) {
      throw new ToolError("idempotency_conflict", "key reused with different payload");
    }
    if (prior) {
      return { status: "reconciled", duplicateEffect: false, preview };
    }
    if (request.dryRun) {
      return { status: "preview", duplicateEffect: false, preview };
    }
    if (approvalHash !== payloadHash) {
      throw new ToolError("approval_error", "approval does not match current preview");
    }

    this.idempotency.set(request.idempotencyKey, payloadHash);
    this.effects.push({ action: request.action, recordId: request.recordId, label: request.label });
    return { status: "executed", duplicateEffect: false, preview };
  }

  effectCount(): number {
    return this.effects.length;
  }
}

async function selfTest(): Promise<void> {
  const tool = new SafeToolBoundary();
  const request: Request = {
    action: "label_record",
    recordId: "rec-001",
    scope: "training",
    label: "reviewed",
    idempotencyKey: "idem-0001",
    dryRun: false,
  };
  const preview = await tool.preview(request);
  const first = await tool.execute(request, preview.previewHash);
  const second = await tool.execute(request, preview.previewHash);
  if (first.status !== "executed" || second.status !== "reconciled" || tool.effectCount() !== 1) {
    throw new Error("self-test failed");
  }
  console.log("safe_tool_boundary.ts self-test passed: 0 duplicate effects");
}

void selfTest();
