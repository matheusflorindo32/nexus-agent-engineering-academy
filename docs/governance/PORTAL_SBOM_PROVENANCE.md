---
title: Portal SBOM and Provenance Protocol
status: review
owner: NEXUS Academy
last_reviewed: 2026-07-23
---

# Portal SBOM and Provenance Protocol

## Purpose

Define a reproducible evidence gate for the portal software supply chain without representing the result as a signed attestation or external certification.

## Scope

The workflow generates a CycloneDX 1.5 SBOM from the committed `portal/package-lock.json`, validates its structure and digest, repeats generation to test determinism, and records repository/workflow provenance metadata.

## Hard gates

The workflow fails when:

- reproducible installation fails;
- the lockfile cannot be parsed;
- the SBOM is empty;
- the CycloneDX envelope is invalid;
- duplicate package URLs are found;
- the recorded SHA-256 differs from the SBOM bytes;
- a second generation differs from the first;
- the evidence bundle is missing.

## Evidence

The retained evidence bundle contains:

- `portal-sbom.cdx.json`;
- `portal-sbom.sha256`;
- generation and validation reports;
- `provenance.json` with repository, commit, pull request, workflow run and limitations.

## Interpretation

A green result supports the limited claims that:

1. the SBOM was derived from the committed npm lockfile;
2. each listed component has a deterministic package URL and version;
3. the generated SBOM bytes match the recorded SHA-256;
4. repeated generation in the same workflow environment produced identical output.

## Explicit limitations

This control does not prove:

- that every runtime component is represented beyond what the npm lockfile records;
- absence of vulnerabilities, malicious packages or license conflicts;
- Sigstore, SLSA, in-toto or third-party attestation compliance;
- identity of a human signer;
- integrity after artifact upload, CDN delivery or browser execution;
- approval to merge, deploy or release.

CI success remains technical evidence only. Human review and explicit approval remain mandatory.
