import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const evidenceDir = path.join(root, 'evidence', 'security');
const baselinePath = path.join(root, 'security', 'npm-audit-baseline.json');
await mkdir(evidenceDir, { recursive: true });

const tracked = execFileSync('git', ['ls-files', '-z'], { encoding: 'utf8' })
  .split('\0')
  .filter(Boolean)
  .filter((file) => !file.startsWith('node_modules/'))
  .filter((file) => !file.startsWith('build/'))
  .filter((file) => !file.includes('/evidence/'));

const rules = [
  { id: 'private-key', severity: 'critical', regex: /-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----/g },
  { id: 'github-token', severity: 'critical', regex: /\bgh[pousr]_[A-Za-z0-9]{30,255}\b/g },
  { id: 'openai-key', severity: 'critical', regex: /\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b/g },
  { id: 'aws-access-key', severity: 'high', regex: /\bAKIA[0-9A-Z]{16}\b/g },
  { id: 'generic-secret-assignment', severity: 'high', regex: /\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*["'][^"'\n]{12,}["']/gi }
];

const allowlisted = [
  /example/i,
  /placeholder/i,
  /dummy/i,
  /changeme/i,
  /your[_-]/i,
  /process\.env/i,
  /\$\{\{/,
  /<[^>]+>/
];

const findings = [];
for (const file of tracked) {
  const fullPath = path.join(root, file);
  let text;
  try {
    text = await readFile(fullPath, 'utf8');
  } catch {
    continue;
  }

  for (const rule of rules) {
    rule.regex.lastIndex = 0;
    for (const match of text.matchAll(rule.regex)) {
      const value = match[0];
      if (allowlisted.some((pattern) => pattern.test(value))) continue;
      const line = text.slice(0, match.index).split('\n').length;
      findings.push({ file, line, rule: rule.id, severity: rule.severity });
    }
  }
}

let audit;
try {
  audit = JSON.parse(execFileSync('npm', ['audit', '--json'], { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 }));
} catch (error) {
  const stdout = error?.stdout?.toString?.() ?? '';
  audit = stdout ? JSON.parse(stdout) : { error: 'npm audit did not return JSON' };
}

const baseline = JSON.parse(await readFile(baselinePath, 'utf8'));
const vulnerabilities = audit.metadata?.vulnerabilities ?? {};
const currentCounts = {
  critical: Number(vulnerabilities.critical ?? 0),
  high: Number(vulnerabilities.high ?? 0),
  moderate: Number(vulnerabilities.moderate ?? 0)
};

const advisorySources = [...new Set(
  Object.values(audit.vulnerabilities ?? {})
    .flatMap((item) => Array.isArray(item.via) ? item.via : [])
    .filter((via) => typeof via === 'object' && via !== null && Number.isInteger(via.source))
    .map((via) => via.source)
)].sort((a, b) => a - b);

const knownSources = new Set(baseline.knownAdvisorySources ?? []);
const newAdvisorySources = advisorySources.filter((source) => !knownSources.has(source));
const countRegressions = Object.entries(currentCounts)
  .filter(([severity, count]) => count > Number(baseline.maximumAllowed?.[severity] ?? 0))
  .map(([severity, count]) => ({ severity, count, allowed: Number(baseline.maximumAllowed?.[severity] ?? 0) }));
const baselineExpired = Date.now() > new Date(`${baseline.reviewBy}T23:59:59Z`).getTime();
const blockingSecrets = findings.filter((item) => item.severity === 'high' || item.severity === 'critical').length;

const report = {
  schemaVersion: 2,
  generatedAt: new Date().toISOString(),
  trackedFilesScanned: tracked.length,
  secretFindings: findings,
  npmAuditSummary: vulnerabilities,
  advisorySources,
  baseline: {
    status: baseline.status,
    recordedAt: baseline.recordedAt,
    reviewBy: baseline.reviewBy,
    expired: baselineExpired,
    maximumAllowed: baseline.maximumAllowed,
    knownAdvisorySources: baseline.knownAdvisorySources
  },
  regressions: {
    countRegressions,
    newAdvisorySources,
    criticalVulnerabilities: currentCounts.critical
  },
  blocking: {
    highOrCriticalSecrets: blockingSecrets,
    baselineExpired,
    countRegressions: countRegressions.length,
    newAdvisorySources: newAdvisorySources.length,
    criticalVulnerabilities: currentCounts.critical
  },
  limitations: [
    'Pattern scanning can produce false positives and false negatives.',
    'The npm baseline is temporary regression control and does not mean known advisories were remediated or accepted as safe.',
    'npm audit covers npm advisory data only and does not replace SAST, DAST, CodeQL, OSV, Trivy or human review.',
    'A passing result does not prove absence of vulnerabilities or exposed secrets.'
  ]
};

await writeFile(path.join(evidenceDir, 'security-baseline-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
await writeFile(path.join(evidenceDir, 'npm-audit.json'), `${JSON.stringify(audit, null, 2)}\n`, 'utf8');
await writeFile(path.join(evidenceDir, 'npm-audit-baseline-used.json'), `${JSON.stringify(baseline, null, 2)}\n`, 'utf8');

const shouldFail =
  blockingSecrets > 0 ||
  baselineExpired ||
  countRegressions.length > 0 ||
  newAdvisorySources.length > 0 ||
  currentCounts.critical > 0;

if (shouldFail) {
  console.error(JSON.stringify(report, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({
  passed: true,
  trackedFilesScanned: tracked.length,
  currentCounts,
  knownAdvisorySources: advisorySources.length,
  secretFindings: findings.length,
  baselineReviewBy: baseline.reviewBy
}));
