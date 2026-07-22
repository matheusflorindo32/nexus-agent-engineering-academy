const path = require('node:path');

const ROUTES = new Map([
  ['course', 'curso'],
  ['labs', 'laboratorios'],
  ['projects', 'projetos'],
]);

function splitSuffix(url) {
  const match = url.match(/^([^?#]*)(.*)$/);
  return {pathname: match ? match[1] : url, suffix: match ? match[2] : ''};
}

function routeFor(relativePath) {
  const normalized = relativePath.split(path.sep).join('/');
  const [collection, ...rest] = normalized.split('/');
  const routeBase = ROUTES.get(collection);
  if (!routeBase) return null;

  let target = rest.join('/');
  target = target.replace(/\.mdx?$/i, '');
  target = target.replace(/(^|\/)README$/i, '');
  target = target.replace(/^\/+|\/+$/g, '');

  return target ? `/${routeBase}/${target}` : `/${routeBase}/`;
}

function visit(node, callback) {
  if (!node || typeof node !== 'object') return;
  callback(node);
  if (Array.isArray(node.children)) {
    for (const child of node.children) visit(child, callback);
  }
}

module.exports = function remarkCrossDocLinks() {
  return (tree, file) => {
    const sourcePath = file.history && file.history[0];
    if (!sourcePath) return;

    const repoRoot = path.resolve(process.cwd(), '..');
    const sourceDirectory = path.dirname(sourcePath);

    visit(tree, (node) => {
      if (node.type !== 'link' && node.type !== 'image') return;
      if (typeof node.url !== 'string') return;
      if (!node.url.endsWith('.md') && !node.url.includes('.md#') && !node.url.includes('.md?')) return;
      if (/^[a-z][a-z0-9+.-]*:/i.test(node.url) || node.url.startsWith('/')) return;

      const {pathname: rawPath, suffix} = splitSuffix(node.url);
      const absoluteTarget = path.resolve(sourceDirectory, rawPath);
      const relativeTarget = path.relative(repoRoot, absoluteTarget);

      if (relativeTarget.startsWith('..') || path.isAbsolute(relativeTarget)) return;

      const routed = routeFor(relativeTarget);
      if (routed) {
        node.url = `pathname://${routed}${suffix}`;
        return;
      }

      const githubPath = relativeTarget.split(path.sep).join('/');
      node.url = `https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/${githubPath}${suffix}`;
    });
  };
};
