# Documentation skills

A collection of Claude skills for technical documentation work. Each skill lives under `skills/<name>/` with its own `SKILL.md`, reference material, and eval suite.

## Available skills

| Skill | Description |
| --- | --- |
| [docs-deslop](skills/docs-deslop/) | Rewrites technical product documentation to strip AI slop and conform to the CTRT topic-type model (Concept, Task, Reference, Troubleshooting, plus Tutorial). |
| [docs-structure](skills/docs-structure/) | Applies Seqera docs house structural conventions to a page or selection. Each structural area (prerequisites, troubleshooting placement, …) has its own reference file. |

## Folder layout

```
.
├── skills/                  # Skill sources, one directory per skill
│   ├── docs-deslop/         # The docs-deslop skill
│   │   ├── SKILL.md         # Skill definition: trigger description + rewrite workflow
│   │   ├── references/
│   │   │   ├── core/        # Core rule catalogs, loaded on demand (phrases, structures,
│   │   │   │                # style-guide, clarity, terminology, topic-types, examples)
│   │   │   └── products/    # Exclusive per-product rules (platform, nextflow, wave,
│   │   │                    # fusion, multiqc); detected doc's file layers on top of core
│   │   └── evals/           # Eval suite
│   │       ├── evals.json   # 10 eval cases (schema and tiers below)
│   │       └── test-inputs/ # Salted input docs for file-based testing
│   ├── docs-deslop.skill    # Packaged skill (zip of docs-deslop/, minus evals) for claude.ai
│   ├── docs-structure/      # The docs-structure skill
│   │   ├── SKILL.md         # Skill definition: trigger + structural-area index
│   │   └── references/
│   │       ├── core/        # Universal conventions (prerequisites, troubleshooting identify+format)
│   │       └── products/    # Per-product troubleshooting placement (platform, fusion, wave, …)
│   └── docs-structure.skill # Packaged skill (zip of docs-structure/) for claude.ai
├── workspace/               # Eval harness and run artifacts
│   ├── grade.py             # Substring/structure assertions for grading eval output
│   ├── verify_evals.py      # Self-test: ideal rewrites pass, original slop fails
│   └── results-<date>/      # Created per eval run (results.json + grading.json)
└── README.md                # This file
```

## Install a skill

### In Claude Code

Copy a skill into your skills directory:

```sh
# Personal (all projects)
cp -R skills/<name> ~/.claude/skills/<name>

# Or per-project
cp -R skills/<name> <project>/.claude/skills/<name>
```

### On claude.ai

Upload the packaged `skills/<name>.skill` file under **Settings → Capabilities → Skills**.

A `.skill` package is a snapshot of the skill's `SKILL.md` + `references/`. If you edit the skill source, repackage it:

```sh
cd skills
zip -r <name>.skill <name> -x "<name>/evals/*" "*/.DS_Store"
```

## docs-deslop

Rewrites technical product documentation to strip AI slop and conform to the CTRT topic-type model (Concept, Task, Reference, Troubleshooting, plus Tutorial).

### Run the skill

Invoke it in a session, either explicitly:

```
/docs-deslop docs/getting-started.md
```

or implicitly — the skill triggers on phrases like "deslop this", "make this doc less AI-sounding", "tighten my draft", or "rewrite this in CTRT", with pasted text or a file path (`.md`, `.mdx`, `.rst`, `.adoc`, `.txt`, `.docx`).

#### Scope

Technical documentation only: concept/task/reference/troubleshooting pages, runbooks, tutorials, release notes, product READMEs. The skill refuses marketing copy, blog posts, and social posts by design.

### Core and product references

The rewrite rules split into two layers. **Core references** (`references/core/*.md`: phrases, structures, style-guide, clarity, topic-types, examples, and `terminology.md`) apply to every doc — the anti-slop rules are fully product-agnostic, and `terminology.md` holds the shared Seqera terminology and formatting (product/tool names, feature-noun casing, pipeline vs workflow, bold vs backticks, UI names, env vars). **Product references** (`references/products/*.md`, one file per product) hold only the rules **exclusive** to each product — what isn't already in core `terminology.md`. They're additive: applied *on top of* the core set, never instead of it. Product files may reference other products.

As step 2 of its workflow, the skill **detects the product** — from the file path (`platform-cloud/`, `fusion_docs/`, `wave_docs/`, `multiqc_docs/`, a Nextflow repo, …), the user's statement, or the doc's vocabulary — and loads that product's exclusive file on top of core `terminology.md`. If no product is detected, it applies the core references only. Because core `terminology.md` is already Platform-centric, `platform.md` is intentionally near-empty (a placeholder for Platform-exclusive extras); `nextflow.md` holds Nextflow's exclusive DSL/config rules; `wave.md`, `fusion.md`, and `multiqc.md` are scaffolds to grow from each product's docs. To add a product, add a file under `references/products/` and a row to the detection table in `SKILL.md`.

### Modes

deslop runs as an aggressive in-place heavy rewrite by default. Two optional modes adjust that, and they combine:

- **Passive mode** — light-touch. Applies only word- and sentence-level fixes (slop phrases, marketing language, voice, tense, punctuation, terminology) and leaves structure alone: no splitting topics, renaming titles, moving troubleshooting, or reshaping tables. Structural changes a full rewrite would make are instead listed in the change summary under a `Recommend (full mode):` block. Trigger with "passive", "light-touch", "words only", or "don't restructure".
- **Verbose mode** — changes only the change summary, not what gets edited. Each significant edit is shown as a `before → after` pair grouped by the rule that triggered it, instead of grouped category counts. Trigger with "verbose", "explain each change", or "show before/after".

The active mode is named on the first line of the change summary (`Mode: passive`, `Mode: verbose`, or `Mode: passive + verbose`). For the full spec, see the "Modes" section of [`skills/docs-deslop/SKILL.md`](skills/docs-deslop/SKILL.md).

### Run the evals

Each case in `skills/docs-deslop/evals/evals.json` has an `id`, a `name`, the exact `prompt` handed to the skill (a salted doc plus the real facts the rewrite needs, so the model never invents technical content), an `expected_output` that names every rule a good rewrite satisfies, and `files` for file-based inputs (paths relative to `skills/docs-deslop/evals/`).

The suite is four tiers:

- **Tier 1 — integrated scenario (eval 1, `file-release-notes`)**: an end-to-end deslop that mixes rule families and is the only case exercising file read/write — it reads `test-inputs/release-notes.md` and writes a `.deslopped` copy.
- **Tier 2 — rule-family coverage (evals 2–5)**: one salted document per core reference file (or pair) — `phrases` (2), `structures` (3), `style-terminology-clarity` (4), `topic-types` (5). Collectively they cover every rule in `references/core/`, so the suite stays cheap to run.
- **Tier 3 — mode coverage (evals 6–8)**: one case per mode behavior — `passive-mode-light-touch` (6) checks that word-level fixes apply while structural changes are flagged not made, `verbose-mode-before-after-summary` (7) checks the per-edit before/after summary format, and `passive-plus-verbose-combined` (8) checks the two modes compose (see [Modes](#modes)). These are graded manually against `expected_output`.
- **Tier 4 — product coverage (evals 9–10)**: non-Platform products that guard product detection and the product-gated troubleshooting rule. `leave-inline-nextflow` (9) checks Nextflow detection, the `products/nextflow.md` DSL/dash rules, and that troubleshooting is **left inline** (Nextflow has no destination); `leave-inline-multiqc` (10) checks the same leave-inline behavior for MultiQC. Both guard the regression where troubleshooting would be moved off a page with nowhere to go.

`grade.py`'s assertions cover evals 1–5 and 9–10; the mode cases (6–8) are reviewed manually against `expected_output`.

`test-inputs/` also holds standalone salted docs covering each topic type (concept, task, CLI reference, troubleshooting, tutorial, runbook), usable for ad-hoc runs ("deslop this file") or for new file-based cases.

#### Quick manual run (any environment)

For a single case: open `evals.json`, copy a case's `prompt` into a session where the skill is installed, and compare the output against the case's `expected_output` — it names every rule the rewrite should satisfy.

For the file-based case (eval 1) and ad-hoc testing, point the skill at a salted doc:

```
/docs-deslop skills/docs-deslop/evals/test-inputs/troubleshooting.md
```

#### Full run (Claude Code, subagent fan-out)

Run each case in a fresh subagent so cases don't contaminate each other:

1. For each eval, spawn an agent with the case's `prompt` (file paths in `files` are relative to `skills/docs-deslop/evals/`) and instructions to read `skills/docs-deslop/SKILL.md` first and follow it.
2. Optionally run a **without-skill** twin of each case (same prompt, no SKILL.md) to measure the skill's lift over the base model.
3. Collect each rewrite + change summary into a `workspace/results-<date>/` directory as `results.json` (a list of `{id, name, rewrite, summary}` entries).
4. Grade with `workspace/grade.py` (substring/structure assertions), or review manually against `expected_output`.

#### Self-test the eval suite

`workspace/verify_evals.py` checks that the assertions themselves are sound: for every eval, a known-good rewrite (from the recorded passing run) passes 100%, and the original slop fed back as the "rewrite" fails. Run it after editing assertions:

```sh
python3 workspace/verify_evals.py
```

`grade.py` covers evals 1–5 and 9–10 (the integrated, rule-family, and product-coverage cases) and grades the flat run layout: point its `ITERATION`
constant at a `workspace/results-<date>/` directory containing `results.json` (a list
of `{id, name, rewrite, summary}` entries) and run it. It prints a per-eval and overall
scorecard and writes `grading.json` into the run directory. Originals for the pasted
evals are extracted from the fenced block in each prompt in `evals.json`; eval 1
reads its test-input file. Run entries with no matching assertion set are skipped.

## docs-structure

Applies Seqera docs house structural conventions to a page or a selected region — the structural, repeatable parts of a page, kept consistent across the docs. It is about structure, not prose; for wording and slop, use `docs-deslop`. The two compose: when `docs-deslop` runs on a Seqera page with prerequisites, it hands off to `docs-structure`.

### Run the skill

Invoke it explicitly:

```
/docs-structure docs/getting-started.md
```

or implicitly — the skill triggers on requests to format, clean up, standardize, or fix the structure of a docs page, or when writing a new guide/tutorial that must follow house format.

### Structural areas

References split into `core/` (universal — every product) and `products/` (per-product), mirroring `docs-deslop`. The skill reads the `core/` reference for the area in scope, plus the detected product's `products/` file for anything product-specific.

| Area | Reference | Covers |
| --- | --- | --- |
| Prerequisites | `references/core/prerequisites.md` | Universal. The `:::info[**Prerequisites**]` admonition, `You need the following:` lead-in, noun-phrase bullets. |
| Troubleshooting (identify + format) | `references/core/troubleshooting.md` | Universal. What counts as troubleshooting content, how to format an entry, the move process. |
| Troubleshooting placement | `references/products/<product>.md` | Product-specific. **Where** troubleshooting goes (destination, page-naming, existing-vs-new) — or that the product has none (MultiQC, Nextflow), so it stays inline. |

Prerequisites is a house-wide convention (all products); troubleshooting placement is product-specific — its destination differs per product, and MultiQC/Nextflow have none. When `docs-deslop` invokes `docs-structure`, it passes the product it already detected.

Add a row here and a reference file when you codify a new convention.