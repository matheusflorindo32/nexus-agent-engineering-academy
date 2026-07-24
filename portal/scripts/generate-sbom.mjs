import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const lockPath = path.join(root, 'package-lock.json');
const outDir = path.join(root, 'evidence', 'sbom');
const outPath = path.join(outDir, 'portal-sbom.cdx.json');
const digestPath = path.join(outDir, 'portal-sbom.sha256');

const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const lockText = await readFile(lockPath, 'utf8');
const lock = JSON.parse(lockText);
const packages = lock.packages ?? {};

const components = Object.entries(packages)
  .filter(([name, meta]) => name && meta?.version)
  .map(([name, meta]) => {
    const packageName = name.replace(/^node_modules\//, '');
    return {
      type: 'library',
      name: packageName,
      version: String(meta.version),
      purl: `pkg:npm/${encodeURIComponent(packageName)}@${encodeURIComponent(String(meta.version))}`,
      hashes: meta.integrity ? [{ alg: 'SHA-512', content: String(meta.integrity).replace(/^sha512-/, '') }] : undefined,
      licenses: meta.license ? [{ license: { id: String(meta.license) } }] : undefined,
      properties: [
        { name: 'nexus:dev', value: String(Boolean(meta.dev)) },
        { name: 'nexus:optional', value: String(Boolean(meta.optional)) }
      ]
    };
  })
  .sort((a, b) => `${a.name}@${a.version}`.localeCompare(`${b.name}@${b.version}`));

const serialSeed = sha256(lockText);
const sbom = {
  bomFormat: 'CycloneDX',
  specVersion: '1.5',
  serialNumber: `urn:uuid:${serialSeed.slice(0,8)}-${serialSeed.slice(8,12)}-${serialSeed.slice(12,16)}-${serialSeed.slice(16,20)}-${serialSeed.slice(20,32)}`,
  version: 1,
  metadata: {
    component: { type: 'application', name: 'nexus-agent-engineering-academy-portal' },
    properties: [
      { name: 'nexus:source-lockfile', value: 'package-lock.json' },
      { name: 'nexus:lockfile-sha256', value: serialSeed },
      { name: 'nexus:generated-by', value: 'portal/scripts/generate-sbom.mjs' }
    ]
  },
  components
};

const canonical = `${JSON.stringify(sbom, null, 2)}\n`;
await mkdir(outDir, { recursive: true });
await writeFile(outPath, canonical, 'utf8');
await writeFile(digestPath, `${sha256(canonical)}  portal-sbom.cdx.json\n`, 'utf8');
console.log(JSON.stringify({ componentCount: components.length, lockfileSha256: serialSeed, sbomSha256: sha256(canonical) }));
