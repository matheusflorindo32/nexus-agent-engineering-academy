import { writeFile, mkdir } from 'node:fs/promises';

const baseUrl = process.env.PORTAL_BASE_URL ?? 'http://127.0.0.1:3000';
const evidenceDir = new URL('../evidence/http-e2e/', import.meta.url);
await mkdir(evidenceDir, { recursive: true });

const results = [];
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

async function check(path, expectedStatus, checks = []) {
  const started = Date.now();
  const response = await fetch(new URL(path, baseUrl), { redirect: 'manual' });
  const body = await response.text();
  const record = {
    path,
    status: response.status,
    expectedStatus,
    durationMs: Date.now() - started,
    contentType: response.headers.get('content-type'),
    bytes: Buffer.byteLength(body)
  };
  results.push(record);
  assert(response.status === expectedStatus, `${path}: expected ${expectedStatus}, received ${response.status}`);
  for (const checkFn of checks) checkFn(body, response, record);
  return { body, response };
}

const htmlCheck = (body, response, record) => {
  assert((response.headers.get('content-type') ?? '').includes('text/html'), `${record.path}: expected HTML`);
  assert(body.includes('<html'), `${record.path}: missing html element`);
  assert(body.includes('<main') || body.includes('main-wrapper'), `${record.path}: missing main content landmark`);
  assert(record.bytes > 500, `${record.path}: unexpectedly small response`);
};

const isNavigableInternalRoute = (href) => {
  if (!href.startsWith('/') || href.startsWith('//')) return false;
  const pathname = new URL(href, baseUrl).pathname;
  if (pathname.startsWith('/assets/') || pathname.startsWith('/img/')) return false;
  const lastSegment = pathname.split('/').filter(Boolean).at(-1) ?? '';
  return !lastSegment.includes('.');
};

let sampledInternalRoutes = [];
let failure = null;

try {
  const home = await check('/', 200, [htmlCheck]);
  sampledInternalRoutes = [...home.body.matchAll(/href=["']([^"'#?]+)["']/g)]
    .map((match) => match[1])
    .filter(isNavigableInternalRoute)
    .map((href) => new URL(href, baseUrl).pathname)
    .filter((href, index, all) => all.indexOf(href) === index)
    .slice(0, 8);

  assert(sampledInternalRoutes.length > 0, 'home page exposes no navigable internal routes for journey sampling');
  for (const href of sampledInternalRoutes) await check(href, 200, [htmlCheck]);
  await check('/__nexus_e2e_missing_route__', 404, [htmlCheck]);
} catch (error) {
  failure = error instanceof Error ? error.message : String(error);
}

const report = {
  schemaVersion: 1,
  baseUrl,
  executedAt: new Date().toISOString(),
  sampledInternalRoutes,
  totalChecks: results.length,
  passed: failure === null,
  failure,
  limitations: [
    'HTTP and rendered-static-contract validation only; this is not a real-browser Playwright test.',
    'It does not validate JavaScript interaction, screen readers, visual regressions or production infrastructure.'
  ],
  results
};

await writeFile(new URL('report.json', evidenceDir), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

if (failure) {
  console.error(JSON.stringify({ passed: false, failure, totalChecks: results.length, sampledInternalRoutes: sampledInternalRoutes.length }));
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ passed: true, totalChecks: results.length, sampledInternalRoutes: sampledInternalRoutes.length }));
}
