import {createHash} from 'node:crypto';
import {readdir, readFile, stat, writeFile} from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const [mode = 'generate', rootArg = 'build', manifestArg = 'artifact-integrity.json'] = process.argv.slice(2);
const root = path.resolve(process.cwd(), rootArg);
const manifestPath = path.resolve(process.cwd(), manifestArg);

async function walk(dir) {
  const entries = await readdir(dir, {withFileTypes: true});
  const files = [];
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile()) files.push(full);
  }
  return files;
}

async function sha256(file) {
  const content = await readFile(file);
  return createHash('sha256').update(content).digest('hex');
}

async function buildManifest() {
  const files = await walk(root);
  const records = [];
  for (const file of files) {
    const info = await stat(file);
    records.push({
      path: path.relative(root, file).split(path.sep).join('/'),
      bytes: info.size,
      sha256: await sha256(file),
    });
  }
  const canonical = JSON.stringify(records);
  return {
    schemaVersion: 1,
    algorithm: 'sha256',
    root: path.basename(root),
    fileCount: records.length,
    totalBytes: records.reduce((sum, item) => sum + item.bytes, 0),
    records,
    recordsDigest: createHash('sha256').update(canonical).digest('hex'),
  };
}

if (mode === 'generate') {
  const manifest = await buildManifest();
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
  process.stdout.write(`${JSON.stringify({decision: 'generated', manifestPath, ...manifest}, null, 2)}\n`);
} else if (mode === 'verify') {
  const expected = JSON.parse(await readFile(manifestPath, 'utf8'));
  const actual = await buildManifest();
  const expectedCanonical = JSON.stringify(expected.records);
  const expectedDigest = createHash('sha256').update(expectedCanonical).digest('hex');
  const errors = [];

  if (expected.schemaVersion !== 1) errors.push('unsupported schemaVersion');
  if (expected.algorithm !== 'sha256') errors.push('unsupported algorithm');
  if (expected.recordsDigest !== expectedDigest) errors.push('manifest recordsDigest is invalid');
  if (expected.fileCount !== actual.fileCount) errors.push(`fileCount mismatch: expected ${expected.fileCount}, actual ${actual.fileCount}`);
  if (expected.totalBytes !== actual.totalBytes) errors.push(`totalBytes mismatch: expected ${expected.totalBytes}, actual ${actual.totalBytes}`);
  if (JSON.stringify(expected.records) !== JSON.stringify(actual.records)) errors.push('artifact records differ');

  const report = {
    decision: errors.length === 0 ? 'pass' : 'fail',
    manifestPath,
    expectedRecordsDigest: expected.recordsDigest,
    actualRecordsDigest: actual.recordsDigest,
    errors,
  };
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (errors.length) process.exit(1);
} else {
  throw new Error(`Unknown mode: ${mode}. Use generate or verify.`);
}
