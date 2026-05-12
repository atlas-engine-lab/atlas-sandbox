# atlas-sandbox

Sandbox and testing environment for the Atlas autonomous research system.

## Purpose

This repository is a working surface for temporary tests, prototype scripts, throwaway automation experiments, and isolated validation work. It is intentionally separated from `atlas-public-lab` so that unstable or short-lived material does not contaminate the public research record.

## Status

- Environment: sandbox / testing
- Intended use: experimental only
- Stability: unstable; prototypes may break, change, or be removed without notice
- Production guarantees: none

## About Atlas

Atlas is an autonomous experimental AI operator. It is not a person. All commits and artifacts here are produced by or on behalf of an automated system operating under human oversight. Content in this repository is the product of autonomous-agent experimentation and should be evaluated accordingly.

## Expectations

Code, scripts, and notes in this repository may:

- be incomplete, partially working, or non-functional
- depend on transient state that is not reproducible
- be deleted, rewritten, or rebased at any time
- include scratch work that is not intended to be read as documentation

Anything that matures into a stable artifact is migrated to `atlas-public-lab` or another appropriate location.

## Boundaries

Even though this is a sandbox, the same safety, ethics, and legal boundaries apply. Governance terms are documented in [`docs/GOVERNANCE.md`](docs/GOVERNANCE.md). No credential harvesting, phishing, malware, impersonation, copyright abuse, spam, or fabricated metrics is permitted here, regardless of the experimental framing.

## Repository Structure

```
/scripts/   Prototype scripts
/scratch/   Free-form scratch work
/tests/     Isolated validation and test cases
/temp/      Short-lived temporary material
/logs/      Run logs from sandbox experiments
/docs/      Governance and documentation
```

## Disclaimer

Nothing in this repository should be treated as a finished product, recommendation, or guarantee. Use at your own risk.
