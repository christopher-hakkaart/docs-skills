# Documentation skills

A collection of Claude skills for technical documentation work. Each skill lives under `skills/<name>/` with its own `SKILL.md`, reference material, and eval suite.

## Available skills

| Skill | Description |
| --- | --- |
| [deslop](skills/deslop/) | Rewrites technical product documentation to strip AI slop and conform to the CTRT topic-type model (Concept, Task, Reference, Troubleshooting, plus Tutorial). |

## Folder layout

```
.
├── skills/                  # Skill sources, one directory per skill
│   ├── deslop/              # The deslop skill
│   │   ├── SKILL.md         # Skill definition: trigger description + rewrite workflow
│   │   ├── references/      # Rule catalogs loaded on demand (phrases, structures,
│   │   │                    # style-guide, terminology, clarity, topic-types, examples)
│   │   └── evals/           # Eval suite
│   │       ├── evals.json   # 5 eval cases (schema and tiers below)
│   │       └── test-inputs/ # Salted input docs for file-based testing
│   └── deslop.skill         # Packaged skill (zip of deslop/, minus evals) for claude.ai
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

## deslop

Rewrites technical product documentation to strip AI slop and conform to the CTRT topic-type model (Concept, Task, Reference, Troubleshooting, plus Tutorial).

### Run the skill

Invoke it in a session, either explicitly:

```
/deslop docs/getting-started.md
```

or implicitly — the skill triggers on phrases like "deslop this", "make this doc less AI-sounding", "tighten my draft", or "rewrite this in CTRT", with pasted text or a file path (`.md`, `.mdx`, `.rst`, `.adoc`, `.txt`, `.docx`).

#### Scope

Technical documentation only: concept/task/reference/troubleshooting pages, runbooks, tutorials, release notes, product READMEs. The skill refuses marketing copy, blog posts, and social posts by design.

### Run the evals

Each case in `skills/deslop/evals/evals.json` has an `id`, a `name`, the exact `prompt` handed to the skill (a salted doc plus the real facts the rewrite needs, so the model never invents technical content), an `expected_output` that names every rule a good rewrite satisfies, and `files` for file-based inputs (paths relative to `skills/deslop/evals/`).

The suite is two tiers:

- **Tier 1 — integrated scenario (eval 1, `file-release-notes`)**: an end-to-end deslop that mixes rule families and is the only case exercising file read/write — it reads `test-inputs/release-notes.md` and writes a `.deslopped` copy.
- **Tier 2 — rule-family coverage (evals 2–5)**: one salted document per reference file (or pair) — `phrases` (2), `structures` (3), `style-terminology-clarity` (4), `topic-types` (5). Collectively they cover every rule in `references/`, so the suite stays cheap to run.

`test-inputs/` also holds standalone salted docs covering each topic type (concept, task, CLI reference, troubleshooting, tutorial, runbook), usable for ad-hoc runs ("deslop this file") or for new file-based cases.

#### Quick manual run (any environment)

For a single case: open `evals.json`, copy a case's `prompt` into a session where the skill is installed, and compare the output against the case's `expected_output` — it names every rule the rewrite should satisfy.

For the file-based case (eval 1) and ad-hoc testing, point the skill at a salted doc:

```
/deslop skills/deslop/evals/test-inputs/troubleshooting.md
```

#### Full run (Claude Code, subagent fan-out)

Run each case in a fresh subagent so cases don't contaminate each other:

1. For each eval, spawn an agent with the case's `prompt` (file paths in `files` are relative to `skills/deslop/evals/`) and instructions to read `skills/deslop/SKILL.md` first and follow it.
2. Optionally run a **without-skill** twin of each case (same prompt, no SKILL.md) to measure the skill's lift over the base model.
3. Collect each rewrite + change summary into a `workspace/results-<date>/` directory as `results.json` (a list of `{id, name, rewrite, summary}` entries).
4. Grade with `workspace/grade.py` (substring/structure assertions), or review manually against `expected_output`.

#### Self-test the eval suite

`workspace/verify_evals.py` checks that the assertions themselves are sound: for every eval, a known-good rewrite (from the recorded passing run) passes 100%, and the original slop fed back as the "rewrite" fails. Run it after editing assertions:

```sh
python3 workspace/verify_evals.py
```

`grade.py` covers all 5 evals and grades the flat run layout: point its `ITERATION`
constant at a `workspace/results-<date>/` directory containing `results.json` (a list
of `{id, name, rewrite, summary}` entries) and run it. It prints a per-eval and overall
scorecard and writes `grading.json` into the run directory. Originals for the pasted
evals are extracted from the fenced block in each prompt in `evals.json`; eval 1
reads its test-input file. Run entries with no matching assertion set are skipped.