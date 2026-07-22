const {themes: prismThemes} = require('prism-react-renderer');
const remarkCrossDocLinks = require('./plugins/remark-cross-doc-links');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NEXUS Agent Engineering Academy',
  tagline: 'Agentes que você consegue explicar, testar, proteger, observar e parar.',
  favicon: 'img/favicon.svg',
  url: 'https://nexus-agent-engineering-academy.vercel.app',
  baseUrl: '/',
  organizationName: 'matheusflorindo32',
  projectName: 'nexus-agent-engineering-academy',
  trailingSlash: false,
  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },
  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          id: 'course',
          path: '../course',
          routeBasePath: 'curso',
          sidebarPath: require.resolve('./sidebars.course.js'),
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
          beforeDefaultRemarkPlugins: [remarkCrossDocLinks],
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'labs',
        path: '../labs',
        routeBasePath: 'laboratorios',
        sidebarPath: require.resolve('./sidebars.labs.js'),
        showLastUpdateAuthor: true,
        showLastUpdateTime: true,
        beforeDefaultRemarkPlugins: [remarkCrossDocLinks],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'projects',
        path: '../projects',
        routeBasePath: 'projetos',
        sidebarPath: require.resolve('./sidebars.projects.js'),
        showLastUpdateAuthor: true,
        showLastUpdateTime: true,
        beforeDefaultRemarkPlugins: [remarkCrossDocLinks],
      },
    ],
  ],
  themeConfig: {
    image: 'img/nexus-social-card.png',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'NEXUS',
      items: [
        {to: '/curso/', label: 'Curso', position: 'left'},
        {to: '/laboratorios/', label: 'Laboratórios', position: 'left'},
        {to: '/projetos/', label: 'Projetos', position: 'left'},
        {
          href: 'https://github.com/matheusflorindo32/nexus-agent-engineering-academy',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Aprender',
          items: [
            {label: 'Quickstart', href: 'https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/QUICKSTART.md'},
            {label: 'Curso', to: '/curso/'},
            {label: 'Laboratórios', to: '/laboratorios/'},
          ],
        },
        {
          title: 'Governança',
          items: [
            {label: 'Contribuir', href: 'https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/CONTRIBUTING.md'},
            {label: 'Segurança', href: 'https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/SECURITY.md'},
            {label: 'Licenciamento', href: 'https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/LICENSING.md'},
          ],
        },
      ],
      copyright: `NEXUS Agent Engineering Academy — conteúdo em revisão. ${new Date().getFullYear()}.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'yaml', 'python', 'typescript'],
    },
    metadata: [
      {name: 'robots', content: 'index,follow'},
      {name: 'referrer', content: 'strict-origin-when-cross-origin'},
    ],
  },
};

module.exports = config;
