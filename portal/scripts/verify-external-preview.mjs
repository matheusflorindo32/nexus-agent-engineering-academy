const baseUrl = process.argv[2];
const expectedSha = process.argv[3];

if (!baseUrl || !expectedSha) {
  console.error('Uso: node verify-external-preview.mjs <url> <expected-sha>');
  process.exit(2);
}

const routes = [
  ['/', 'Engenharia de agentes'],
  ['/curso', 'Curso'],
  ['/laboratorios', 'Laboratórios'],
  ['/projetos', 'Projetos'],
  ['/curso/modules/orientation', 'Orientação'],
  ['/projetos/capstone', 'Capstone'],
];

const requiredHeaders = {
  'x-content-type-options': 'nosniff',
  'x-frame-options': 'DENY',
  'referrer-policy': 'strict-origin-when-cross-origin',
  'cross-origin-opener-policy': 'same-origin',
};

const results = [];
for (const [route, marker] of routes) {
  const response = await fetch(new URL(route, baseUrl), {redirect: 'error'});
  const body = await response.text();
  const ok = response.status === 200 && body.includes(marker);
  results.push({route, status: response.status, bytes: Buffer.byteLength(body), marker, ok});
  if (!ok) throw new Error(`Falha em ${route}: status=${response.status}, marker=${marker}`);
}

const identityResponse = await fetch(new URL('/.well-known/nexus-build.json', baseUrl), {redirect: 'error'});
if (identityResponse.status !== 200) throw new Error('Identidade do build indisponível');
const identity = await identityResponse.json();
if (identity.sourceSha !== expectedSha) {
  throw new Error(`SHA publicado divergente: esperado=${expectedSha}, observado=${identity.sourceSha}`);
}
if (identity.status !== 'review' || identity.schemaVersion !== 1) {
  throw new Error('Contrato de identidade inválido');
}

const rootResponse = await fetch(new URL('/', baseUrl), {redirect: 'error'});
for (const [name, expected] of Object.entries(requiredHeaders)) {
  const observed = rootResponse.headers.get(name);
  if (observed !== expected) throw new Error(`Header ${name} divergente: ${observed}`);
}
const csp = rootResponse.headers.get('content-security-policy') || '';
for (const directive of ["default-src 'self'", "object-src 'none'", "frame-ancestors 'none'"]) {
  if (!csp.includes(directive)) throw new Error(`CSP sem ${directive}`);
}

console.log(JSON.stringify({baseUrl, expectedSha, identity, routes: results, decision: 'pass'}, null, 2));
