import { readdir, readFile, stat, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const buildDir = path.join(root, 'build');
const evidenceDir = path.join(root, 'evidence', 'accessibility-performance');
await mkdir(evidenceDir, { recursive: true });

async function walk(dir) {
  const out = [];
  for (const name of await readdir(dir)) {
    const full = path.join(dir, name);
    const info = await stat(full);
    if (info.isDirectory()) out.push(...await walk(full)); else out.push(full);
  }
  return out;
}

const files = await walk(buildDir);
const htmlFiles = files.filter((f) => f.endsWith('.html'));
const findings = [];
let totalBytes = 0;
let largestAsset = { file: '', bytes: 0 };

for (const file of files) {
  const info = await stat(file);
  totalBytes += info.size;
  if (info.size > largestAsset.bytes) largestAsset = { file: path.relative(buildDir, file), bytes: info.size };
}

for (const file of htmlFiles) {
  const html = await readFile(file, 'utf8');
  const rel = path.relative(buildDir, file);
  const check = (ok, rule, severity = 'high') => { if (!ok) findings.push({ file: rel, rule, severity }); };
  check(/<html[^>]+lang=["'][^"']+["']/i.test(html), 'html-lang');
  check(/<title>[^<]+<\/title>/i.test(html), 'document-title');
  check(/<main\b/i.test(html) || /main-wrapper/i.test(html), 'main-landmark');
  check(/<h1\b/i.test(html), 'page-h1');
  check(!/<img\b(?![^>]*\balt=)[^>]*>/i.test(html), 'image-alt');
  check(!/<button\b[^>]*>\s*<\/button>/i.test(html), 'empty-button-name');
}

const budgets = {
  totalBuildBytes: 12 * 1024 * 1024,
  largestAssetBytes: 2 * 1024 * 1024,
  maximumHtmlPagesWithoutH1: 0
};
const budgetFailures = [];
if (totalBytes > budgets.totalBuildBytes) budgetFailures.push({ rule: 'total-build-budget', actual: totalBytes, limit: budgets.totalBuildBytes });
if (largestAsset.bytes > budgets.largestAssetBytes) budgetFailures.push({ rule: 'largest-asset-budget', actual: largestAsset.bytes, limit: budgets.largestAssetBytes, file: largestAsset.file });

const report = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  htmlPagesChecked: htmlFiles.length,
  totalFiles: files.length,
  totalBuildBytes: totalBytes,
  largestAsset,
  findings,
  budgetFailures,
  passed: findings.length === 0 && budgetFailures.length === 0,
  limitations: [
    'Static HTML checks do not replace axe-core, Lighthouse, keyboard testing, screen readers or testing with people with disabilities.',
    'Build-size budgets are proxy controls and do not measure Core Web Vitals or real-user performance.'
  ]
};
await writeFile(path.join(evidenceDir, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);
if (!report.passed) {
  console.error(JSON.stringify(report, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({ passed: true, htmlPagesChecked: htmlFiles.length, totalBuildBytes: totalBytes, largestAsset }));
