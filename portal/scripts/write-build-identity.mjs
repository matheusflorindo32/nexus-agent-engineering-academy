import {createHash} from 'node:crypto';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const lockPath = path.join(root, 'package-lock.json');
const outputDir = path.join(root, 'static', '.well-known');
const outputPath = path.join(outputDir, 'nexus-build.json');

const lock = await readFile(lockPath);
const sha256 = createHash('sha256').update(lock).digest('hex');
const sourceSha = process.env.VERCEL_GIT_COMMIT_SHA || process.env.GITHUB_SHA || 'local-unverified';
const provider = process.env.VERCEL ? 'vercel' : process.env.GITHUB_ACTIONS ? 'github-actions' : 'local';

const identity = {
  schemaVersion: 1,
  sourceSha,
  lockfileSha256: sha256,
  provider,
  status: 'review',
  generatedAt: new Date().toISOString(),
};

await mkdir(outputDir, {recursive: true});
await writeFile(outputPath, `${JSON.stringify(identity, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(identity));
