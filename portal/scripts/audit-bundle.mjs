import {createHash} from 'node:crypto';
import {readFile, readdir, stat} from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const buildDir = path.resolve(process.argv[2] ?? 'build');
const maxFileBytes = 8 * 1024 * 1024;
const textExtensions = new Set(['.html', '.js', '.css', '.json', '.xml', '.txt', '.svg', '.map']);
const prohibitedPatterns = [
  {name: 'OpenAI key', regex: /sk-(?:proj-)?[A-Za-z0-9_-]{20,}/g},
  {name: 'GitHub token', regex: /gh[pousr]_[A-Za-z0-9]{20,}/g},
  {name: 'AWS access key', regex: /AKIA[0-9A-Z]{16}/g},
  {name: 'private key', regex: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g},
  {name: 'generic bearer token', regex: /Bearer\s+[A-Za-z0-9._~+\/-]{30,}/g},
];

async function walk(directory) {
  const entries = await readdir(directory, {withFileTypes: true});
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(fullPath));
    else if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

const files = (await walk(buildDir)).sort();
const findings = [];
const manifest = [];

for (const file of files) {
  const metadata = await stat(file);
  const relativePath = path.relative(buildDir, file).split(path.sep).join('/');
  const bytes = await readFile(file);
  const digest = createHash('sha256').update(bytes).digest('hex');
  manifest.push({path: relativePath, bytes: metadata.size, sha256: digest});

  if (metadata.size > maxFileBytes) {
    findings.push({severity: 'high', type: 'oversized_file', path: relativePath, bytes: metadata.size});
  }

  if (relativePath.endsWith('.map')) {
    findings.push({severity: 'medium', type: 'source_map_published', path: relativePath});
  }

  if (textExtensions.has(path.extname(file).toLowerCase()) && metadata.size <= maxFileBytes) {
    const text = bytes.toString('utf8');
    for (const pattern of prohibitedPatterns) {
      const matches = [...text.matchAll(pattern.regex)];
      if (matches.length > 0) {
        findings.push({severity: 'critical', type: 'secret_pattern', pattern: pattern.name, path: relativePath, matches: matches.length});
      }
    }
  }
}

const criticalOrHigh = findings.filter((finding) => ['critical', 'high'].includes(finding.severity));
const report = {
  buildDir,
  generatedAt: new Date().toISOString(),
  files: manifest.length,
  totalBytes: manifest.reduce((sum, item) => sum + item.bytes, 0),
  findings,
  manifest,
  decision: criticalOrHigh.length === 0 ? 'pass' : 'block',
};

process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
if (criticalOrHigh.length > 0) process.exit(1);
