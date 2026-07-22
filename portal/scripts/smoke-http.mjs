import process from 'node:process';

const baseUrl = process.env.PORTAL_BASE_URL ?? 'http://127.0.0.1:3000';
const timeoutMs = Number(process.env.PORTAL_SMOKE_TIMEOUT_MS ?? 8000);

const routes = [
  '/',
  '/curso',
  '/laboratorios',
  '/projetos',
  '/curso/modules/orientation',
  '/curso/modules/tool-engineering',
  '/curso/modules/evaluation-engineering',
  '/projetos/capstone',
];

const expectedText = new Map([
  ['/', 'Engenharia de agentes com contratos, controle e evidência.'],
  ['/curso', 'NEXUS Agent Engineering Academy'],
  ['/laboratorios', 'Laboratórios'],
  ['/projetos', 'Projetos'],
]);

const evidence = [];
let failed = false;

for (const route of routes) {
  const url = new URL(route, baseUrl);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      redirect: 'manual',
      signal: controller.signal,
      headers: {'user-agent': 'nexus-portal-smoke/1.0'},
    });
    const body = await response.text();
    const marker = expectedText.get(route);
    const okStatus = response.status === 200;
    const okType = (response.headers.get('content-type') ?? '').includes('text/html');
    const okMarker = marker ? body.includes(marker) : body.includes('<!doctype html');
    const ok = okStatus && okType && okMarker;

    evidence.push({
      route,
      url: url.toString(),
      status: response.status,
      contentType: response.headers.get('content-type'),
      bytes: Buffer.byteLength(body),
      marker: marker ?? '<!doctype html',
      ok,
    });
    failed ||= !ok;
  } catch (error) {
    evidence.push({route, url: url.toString(), ok: false, error: String(error)});
    failed = true;
  } finally {
    clearTimeout(timer);
  }
}

process.stdout.write(`${JSON.stringify({baseUrl, checkedAt: new Date().toISOString(), evidence}, null, 2)}\n`);
if (failed) process.exit(1);
