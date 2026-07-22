import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

const tracks = [
  {
    title: 'NEXUS Start',
    text: 'Do zero ao primeiro agente local, somente leitura e sem chave de API.',
    href: '/curso/modules/00-orientation/',
  },
  {
    title: 'NEXUS Builder',
    text: 'Contexto, tools, loops, memória e coordenação com contratos explícitos.',
    href: '/curso/modules/03-tool-engineering/',
  },
  {
    title: 'NEXUS Engineer',
    text: 'Avaliação, segurança, produção, observabilidade e automação confiável.',
    href: '/curso/modules/07-evaluation-engineering/',
  },
  {
    title: 'NEXUS Elite',
    text: 'Capstone auditável com game day, reprodução independente e defesa técnica.',
    href: '/projetos/capstone/',
  },
];

function TrackCard({title, text, href}) {
  return (
    <article className={styles.card}>
      <Heading as="h3">{title}</Heading>
      <p>{text}</p>
      <Link className={styles.cardLink} to={href}>
        Abrir trilha<span className="sr-only"> {title}</span>
      </Link>
    </article>
  );
}

export default function Home() {
  return (
    <Layout
      title="Academia open source de engenharia de agentes"
      description="Aprenda a construir agentes de IA que você consegue explicar, testar, proteger, observar e parar.">
      <main>
        <section className={styles.hero} aria-labelledby="hero-title">
          <div className="container">
            <p className={styles.eyebrow}>OPEN SOURCE · PT-BR CANÔNICO · STATUS REVIEW</p>
            <Heading as="h1" id="hero-title" className={styles.heroTitle}>
              Engenharia de agentes com contratos, controle e evidência.
            </Heading>
            <p className={styles.heroText}>
              Aprenda a construir agentes de IA que você consegue explicar, testar,
              proteger, observar e parar — sem depender de um fornecedor específico.
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/curso/">
                Começar pelo curso
              </Link>
              <Link className="button button--secondary button--lg" to="/laboratorios/">
                Explorar laboratórios
              </Link>
            </div>
            <p className={styles.disclaimer}>
              O conteúdo permanece em revisão. CI verde não equivale a prontidão de produção,
              segurança absoluta ou eficácia pedagógica comprovada.
            </p>
          </div>
        </section>

        <section className={styles.section} aria-labelledby="tracks-title">
          <div className="container">
            <Heading as="h2" id="tracks-title">Trilhas progressivas</Heading>
            <p className={styles.sectionIntro}>
              Entre pelo nível adequado e avance somente quando conseguir reproduzir as evidências.
            </p>
            <div className={styles.grid}>
              {tracks.map((track) => <TrackCard key={track.title} {...track} />)}
            </div>
          </div>
        </section>

        <section className={styles.sectionAlt} aria-labelledby="principles-title">
          <div className="container">
            <Heading as="h2" id="principles-title">O que torna a NEXUS diferente</Heading>
            <div className={styles.principles}>
              <div><strong>Baseline antes do agente.</strong><span> IA só entra onde a incerteza justifica.</span></div>
              <div><strong>Hard gates antes da média.</strong><span> Falhas críticas bloqueiam promoção.</span></div>
              <div><strong>Evidência antes da afirmação.</strong><span> Resultados precisam ser reproduzíveis.</span></div>
              <div><strong>Controle antes da autonomia.</strong><span> Autoridade e budgets ficam fora do modelo.</span></div>
            </div>
          </div>
        </section>

        <section className={styles.section} aria-labelledby="next-title">
          <div className="container">
            <Heading as="h2" id="next-title">Primeiro resultado em até 10 minutos</Heading>
            <p className={styles.sectionIntro}>
              O quickstart local não exige chave de API, conta externa nem dados reais.
            </p>
            <a
              className="button button--primary"
              href="https://github.com/matheusflorindo32/nexus-agent-engineering-academy/blob/main/QUICKSTART.md">
              Abrir quickstart no GitHub
            </a>
          </div>
        </section>
      </main>
    </Layout>
  );
}
