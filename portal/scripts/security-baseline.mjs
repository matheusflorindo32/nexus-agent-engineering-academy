import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const evidenceDir = path.join(root, 'evidence', 'security');
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

const vulnerabilities = audit.metadata?.vulnerabilities ?? {};
const blockingVulnerabilities = Number(vulnerabilities.high ?? 0) + Number(vulnerabilities.critical ?? 0);
const blockingSecrets = findings.filter((item) => item.severity === 'high' || item.severity === 'critical').length;

const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  trackedFilesScanned: tracked.length,
  secretFindings: findings,
  npmAuditSummary: vulnerabilities,
  blocking: {
    highOrCriticalSecrets: blockingSecrets,
    highOrCriticalVulnerabilities: blockingVulnerabilities
  },
  limitations: [
    'Pattern scanning can produce false positives and false negatives.',
    'npm audit covers npm advisory data only and does not replace SAST, DAST, CodeQL, OSV, Trivy or human review.',
    'A passing result does not prove absence of vulnerabilities or exposed secrets.'
  ]
};

await writeFile(path.join(evidenceDir, 'security-baseline-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
await writeFile(path.join(evidenceDir, 'npm-audit.json'), `${JSON.stringify(audit, null, 2)}\n`, 'utf8');

if (blockingSecrets > 0 || blockingVulnerabilities > 0) {
  console.error(JSON.stringify(report, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ passed: true, trackedFilesScanned: tracked.length, vulnerabilities, secretFindings: findings.length }));
