# Minos — Agentic SDLC Framework

> *The judge that weighs every delivery.*

By Andrés Felipe Reyes Gallego.

In myth, Minos judges each soul that comes before him. Here, an **adversarial
verifier** is interleaved after every role: it receives only the claims and the
code — never the author's reasoning — and returns a verdict.

A repository-based design for software delivery with separated roles, structured handoffs and evidence-oriented verification. This publication contains the supplied framework version 1.7.0 and an English technical paper with two figures.

## Research

- [Technical paper in English](docs/research/Agentic-SDLC-Paper-Andres-Reyes-EN-v1.1.pdf)
- [Editable paper](docs/research/Agentic-SDLC-Paper-Andres-Reyes-EN-v1.1.docx)
- [LinkedIn text](docs/research/linkedin-post.md)
- [Figure data and vector assets](docs/research/figures/)
- [Original Spanish documentation](README.md)

## Structure

Seven delivery roles are complemented by a verifier. Procedures belong in the skill catalog, routing in `contratos/roles.yaml`, and acceptance criteria in `contratos/gates.yaml`.

The separate `minos-skills` repository is intended to be mounted at `.claude/skills`. That catalog is not published yet, so this repository declares no submodule: `.claude/skills/` ships a placeholder, and `docs/gitmodules.plantilla` holds the configuration to apply — pinned to a real commit — once the catalog exists.

## Evidence status

Static inspection identifies 23 declared gates, including 7 manual ones. Non-manual declaration does not prove evaluator implementation. The advance-check script reads declared handoff states and does not generally execute all checks described in the YAML. The included paper documents these limits. No measured accuracy, productivity or cost gains are claimed.

## Figures

Figure 1 is an intended evidence flow. Figure 2 counts verification types from the package YAML. Regenerate them from `docs/research/build_figures.py` using the dependencies in `requirements-figures.txt`; the chart is not a performance benchmark.

## Attribution and licensing

See [source credits](docs/09-creditos.md). This repository is released under the [MIT License](LICENSE) by its author. Third-party notices in the credits page are preserved; no third-party code is redistributed here.
