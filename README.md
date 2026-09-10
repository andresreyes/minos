<h1 align="center">Minos</h1>

<p align="center">
  <em>The judge that weighs every delivery.</em><br>
  Agentic SDLC with separated roles, contracts between them, and verifiable gates.
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-1.7.0-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="roles" src="https://img.shields.io/badge/roles-8-orange">
  <img alt="gates" src="https://img.shields.io/badge/declared%20gates-23-lightgrey">
</p>

<p align="center">
  <a href="README.md">Español</a> · <strong>English</strong>
</p>

---

In myth, Minos judges every soul brought before him. Here it works the same way: an
**adversarial verifier** is interleaved after each role, receives only the claims and
the code — never the author's reasoning — and returns a verdict.

A standard framework for developing with agents inside a Coder workspace, with
separated roles, contracts between them, and verifiable gates.

Built for teams whose container can only reach GitHub: **everything lives in the
repository**, there is nothing to configure in the Coder console.

## What the package contains

```
minos/                    this repo — roles, gates, contracts, scripts
  docs/pdf/
    Framework-SDLC-Agentico-Guia.pdf      28 pp · implementing the framework
    Fundamentos-Trabajar-con-Agentes.pdf   7 pp · fundamentals, stands alone

minos-skills/             the catalog (submodule at .claude/skills)
  FOUNDATIONS.md   the fundamentals — read this first
  AUTHORING.md     how a skill is written
  CONTEXT.md       what information enters the window
  PRECISION.md     how to make its output checkable
  <role>/SKILL.md  the eight procedures
```

The catalog's four guides are mounted with the submodule, so the agent has them
available inside the workspace. `CLAUDE.md` and `AGENTS.md` reference them and pull
from `FOUNDATIONS.md` the three rules that apply to every role invocation: honest
output, grounding in sources, and a fresh chat on a foundational error.

## What it solves

An agent with no structure does all seven things at once: it designs, implements,
grades its own work, and deploys. Nobody can audit that. Here each role has an input,
an output, and a verifiable gate, and work moves from one to the next through a JSON
file.

## The seven roles

| Role | Produces | Does not do |
|---|---|---|
| Tech lead | Work order, closure | Design, implement |
| Architect | Design, contracts, impact matrix | Implement |
| Builder | Code, unit tests, package | Decide architecture, deploy |
| Testing | Certification with evidence | Fix defects |
| Security | Ruling and findings | Fix findings |
| SRE | Objectives, alerts, runbook, rollback criteria | Deploy |
| DevOps | Manual, closed order, execution | Design, fix |
| **Verifier** | **Verdicts on each role's claims** | **Fix the artifact** |

The verifier does not come last: it is interleaved **after every role**. It receives
only the claims file and the code, never the author's reasoning. See
`docs/05-verificacion-adversarial.md`.

## Installation

```bash
git clone https://github.com/<ORG>/minos.git
cd minos
./scripts/bootstrap.sh
```

> **A note on the skill catalog.** `minos-skills` is not published yet, so this repo
> does **not** declare the submodule: `.claude/skills/` ships a placeholder. Once the
> catalog is on GitHub, mount the submodule using the template in
> `docs/gitmodules.plantilla` and pin it by SHA:
>
> ```bash
> git submodule add -b main https://github.com/<ORG>/minos-skills.git .claude/skills
> ```

To integrate it into the Coder template, see `coder/main.tf` and
`docs/03-adopcion-coder.md`.

## Usage

```
/iniciar  I need to add retries to the event consumer
```

The tech lead scopes the request, declares impact, and issues the order. From there:
`/handoff` advances the chain, `/verificar` launches adversarial verification of the
role that just finished, and `/gate` shows what is still missing.

## Tuning

Only `contratos/gates.yaml` and `contratos/roles.yaml` are touched. See
`docs/04-personalizacion.md`. If you find yourself editing a `SKILL.md` to change a
threshold, the threshold was in the wrong place.

## Version

See `VERSION`. The skill catalog carries its own versioning and is pinned by
submodule SHA, so updating it is always an explicit commit in this repo.

## Research

- [Technical paper in English](docs/research/Agentic-SDLC-Paper-Andres-Reyes-EN-v1.1.pdf)
- [Editable paper](docs/research/Agentic-SDLC-Paper-Andres-Reyes-EN-v1.1.docx)
- [LinkedIn text](docs/research/linkedin-post.md)
- [Figure data and vector assets](docs/research/figures/)

## Evidence status

Static inspection identifies 23 declared gates, including 7 manual ones. Non-manual
declaration does not prove evaluator implementation. The advance-check script reads
declared handoff states and does not generally execute all checks described in the
YAML. The included paper documents these limits. No measured accuracy, productivity,
or cost gains are claimed.

Figure 1 is an intended evidence flow. Figure 2 counts verification types from the
package YAML. Regenerate them from `docs/research/build_figures.py` using the
dependencies in `requirements-figures.txt`; the chart is not a performance benchmark.

## Attribution and licensing

By Andrés Felipe Reyes Gallego. See [source credits](docs/09-creditos.md). This
repository is released under the [MIT License](LICENSE). Third-party notices in the
credits page are preserved; no third-party code is redistributed here.
