#!/usr/bin/env python3
"""Self-test for the deslop eval suite.

For every eval in grade.EVALS, this checks two things without needing a run:
  1. Satisfiability — a curated *ideal* desloped rewrite passes 100% of the assertions.
     (Catches contradictory assertions and substring traps, e.g. asserting absence of a
     string that legitimately appears in good output.)
  2. Discrimination — feeding the original *slop* back as the "rewrite" does NOT pass,
     proving the assertions actually detect slop rather than passing anything.

The ideal rewrites and change summaries below were curated from a known-good graded run
(eval 2's summary is hand-tuned to carry per-bullet counts). Originals come from the
fenced block in each eval's prompt in evals.json; eval 1 reads its test-input file.

Run: python3 verify_evals.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade  # noqa: E402

IDEALS = {
    "eval-1-file-release-notes": (
"""# Seqera Platform v24.1 release notes

## Performance

- Reduced run submission p99 latency to AWS Batch compute environments from 12s to 4s (#1842)
- Loaded the Launchpad pipeline list through a paginated query, ~3x faster for workspaces with more than 1000 pipelines (#1856)
- Batched Data Explorer storage API calls for bucket listings instead of issuing them sequentially (#1871)

## Security

- Added SAML 2.0 and OIDC single sign-on
- Added role-based access control (RBAC) with 5 built-in roles plus custom roles
- Added audit logging to S3, with optional WORM retention

## Breaking changes

- Removed the deprecated `tw --token` flag. Set `TOWER_ACCESS_TOKEN` instead.
- Changed the `tw` default output format from JSON to `table`. Set the format with `--output`.

See the [migration guide](https://docs.seqera.io/platform-cloud/migrate/24.1) before upgrading.""",
"""- Classified as **Reference** (release notes; each entry is a typed lookup item). Formatted entries as bulleted lists with change + magnitude + issue number, not tables, per the release-note rule.
- Cut the entire marketing opener, the "What's New" pep talk, and the "Conclusion" section ("absolutely thrilled", "quantum leap", "fundamentally transform", "blazing fast", "we'd love to hear your feedback").
- Cut ~12 marketing/puffery words and sales-deck verbs (powerful, robust, comprehensive, seamlessly, leverage, harness, empower, cutting-edge, etc.) and slop transitions ("It's worth noting that", "Last but not least", "In conclusion", "Let's dive into").
- Replaced vague bold-first bullets ("Run submission has been significantly improved") with the specific change, magnitude, and issue number using realistic stand-in facts (#1842, #1856, #1871).
- Expanded the vague Security section into 3 concrete entries (SAML 2.0/OIDC SSO, RBAC with 5 built-in + custom roles, S3 audit logging with optional WORM).
- Surfaced the breaking changes as a named section with the two concrete changes (removed `tw --token`, default output now `table`) plus a single migration-guide link; dropped the contentless "Developer Experience" section that stated no actual change.
- Renamed heading from `# Seqera Platform v24.1 Release Notes` to sentence case `# Seqera Platform v24.1 release notes`; replaced `What's New` / `Performance Improvements` / `Enhanced Security` / `Conclusion` headings with `Performance` / `Security` / `Breaking changes` (anchor links to the old headings will break and need updating).
- Reduced length roughly 70% (~340 → ~110 words). Saved to test-inputs/release-notes.deslopped.md."""),
    "eval-2-phrases-rule-family": (
"""# Compute environments

A compute environment defines where your pipeline runs: the execution backend (AWS Batch, Azure Batch, Google Cloud Batch, Kubernetes, or an HPC scheduler), the credentials used to access it, and the work directory for pipeline runs. A workspace can hold multiple compute environments.

This release adds run-level cost reporting and a bulk relaunch action for compute environments.

Configure credentials before you create a compute environment. Seqera Platform supports AWS, Azure, and Google Cloud. Validating credentials before a run surfaces permission errors at setup instead of at launch.

Stored credentials connect Seqera Platform to cloud storage. Validation checks the stored values before any run. Unset optional fields fall back to placeholder values. Seqera Platform reads only from buckets on the storage allowlist. Pipelines track the main branch of their repository by default.

For credential fields and validation behavior, see the [credentials reference](#).""",
"""- Classified as **Concept** (`Compute environments`, noun title kept)
- Cut 6 throat-clearing/meta openers (here's the thing, it's worth noting, keep in mind, in this section, let's dive in, in conclusion)
- Cut 13 marketing/jargon terms (powerful, comprehensive, best-in-class, cutting-edge, game-changer, cornerstone, ecosystem, democratize, delve, tapestry, streamline, supercharge, empowers) and replaced the hype with the 2 real release changes (run-level cost reporting, bulk relaunch)
- Fixed 5 padding/nominalization phrases (in order to, due to the fact that, basically, perform the configuration of, and so on)
- Cut 4 vague attributions/declaratives (experts argue, industry reports suggest, it is widely believed, the implications are significant)
- Rewrote 3 product-as-subject phrasings (allows you to, enables you to, gives you the ability to) to direct statements
- Replaced 4 non-inclusive terms (sanity check -> check, dummy value -> placeholder value, whitelist -> allowlist, master branch -> main branch), keeping the sentences as conceptual statements
- Replaced "click here" with a descriptive link to the credentials reference"""),
    "eval-3-structures-rule-family": (
"""## Token and schema handling

Failed tasks retry automatically up to 3 times, using exponential backoff that starts at 30 seconds. This keeps pipelines resilient when individual runs fail.

A run fails when the account hits its vCPU quota. The platform checks the quota before submitting jobs and queues the run if the quota is exceeded.

The access token expires after 1 hour. Refresh it before a run. The schema is cached, so changes to it require a restart. Keep tokens short-lived.

## Platform characteristics

- Performance: runs start in under 30 seconds on a warm environment.
- Reliability: failed tasks retry automatically up to 3 times.
- Security: credentials are encrypted at rest.

## Configuration

Set the following:

- The `--profile` flag.
- The region, work directory, and maximum CPUs.
- Retries (enabled).""",
"""- Classified as a mixed page: a **Concept** (token, retry, and quota behavior) plus a **Reference** (the three-item characteristics list and the configuration settings); split the mashed-together content into typed sections.
- Removed formulaic AI structures: 2 binary contrasts ("This isn't a bug. It's a design decision."), a negative listing ("Not slow. Not broken. Just misunderstood."), 2 self-posed rhetorical questions ("Why does retry behavior matter?", "The result?"), anaphora ("It retries fast. It retries quietly..."), dramatic fragmentation ("That's it. That's the feature."), a "Despite these challenges" beat, a listicle-in-prose ("The first wall... second... third"), a "conductor" dead metaphor, historical-analogy stacking ("AWS didn't solve this..."), the invented label "observability gap," and the participle "underscoring its role as a critical component."
- Fixed sentence joins: removed the ", so" / "which means" join in the token paragraph (kept one short causal "so" for the cached-schema aside per the rule's exception) and split the run-on token/schema sentence.
- Fixed punctuation: removed mid-sentence colons used for drama ("There's one rule:", "The result?"), the semicolon clause-join, the `→` arrow in the bullet, and curly quotes around `--profile`; added the Oxford comma in "region, work directory, and maximum CPUs."
- Removed fractal summaries and one-point dilution: cut "In this section, we'll cover three benefits," "As discussed in this section...," and the "Fast runs save time / Quick runs / Speedy runs" tricolon restatement; dropped the "So performance is fast. Now reliability is high. But security is strong." So/Now/But openers.
- Removed bold-first bullet leads (Performance/Reliability/Security) since each bullet is a full sentence; applied the supplied facts (3 retries with exponential backoff starting at 30s; quota-check-then-queue behavior; 1-hour token expiry; schema restart) and put code in backticks.
- Renamed the heading from `Token handling.` (trailing period) to sentence-case `Token and schema handling`; flag for inbound-link review since the anchor changes."""),
    "eval-4-style-terminology-clarity-rule-family": (
"""## Step 1: Sign in

Use the form to sign in with your email. You cannot launch a run until you provide an access token. Set `TOWER_ACCESS_TOKEN` to authenticate. To start, select **Launch**.

Seqera Platform submits the job to AWS Batch. Seqera Platform generates a new access token. Run the migration before you upgrade. The new release reduces run-submission p99 latency from 12s to 4s and adds support for Google Cloud Batch, joining AWS Batch and Azure Batch. Pipeline runs use high-performance computing (HPC) or Google Cloud Platform (GCP) backends.

Seqera Platform stores your credentials and compute environments per workspace. The executor — the system that runs pipeline tasks, such as AWS Batch or Kubernetes — runs the Nextflow pipeline tasks automatically. When you configure a compute environment, make sure your credentials have the right cloud-provider permissions. These usually cover instances, storage, and networking. The executor and the scheduler then coordinate.

The pipeline failed to launch from the **Launchpad**. Open the **Data Explorer**, then check the run in the **Runs** tab and view the MultiQC report. Set the `--profile` flag and open `nextflow.config`. Each task ran on its own node.

### Notes

Configure the custom settings for project integrations early. Several are available, and you will use them later. To handle a failed integration, control the retry logic.

For testing, use the token `<your_access_token>` and the email `admin@example.com`.""",
"""- Classified as **Task** (page title supplies the H1). Renamed the supplied title from `Configuring The Compute Environment` to `Configure the compute environment` (active verb + noun, sentence case, no `-ing` form) and removed the body H1 so the body starts at H2.
- Style, headings: renamed `Step 1: Log In` to `Step 1: Sign in` (sentence case; "sign in" not "log in", no bold) and demoted `#### Notes` to `### Notes` to fix the skipped heading level. Renaming these headings changes their anchors (`#step-1-log-in` and `#notes`) and will break inbound or in-page links.
- Style, voice and tense: converted 4 passive constructions to active voice ("The job is submitted to AWS Batch by Tower" -> "Seqera Platform submits the job to AWS Batch"; "A new access token will be generated" -> "Seqera Platform generates a new access token"; "the migration should be run before the upgrade is performed" -> "Run the migration before you upgrade") and replaced the vague release claims with the supplied facts ("significantly faster" -> "reduces run-submission p99 latency from 12s to 4s"; "various providers" -> "Google Cloud Batch, joining AWS Batch and Azure Batch").
- Style, localization and fake info: fixed 2 subject-hiding constructions ("There are several...", "It is recommended that..."), replaced the ambiguous "it", broke the noun string "project integration custom settings", replaced "controlling the retry logic helps" with "control the retry logic", cut the idiom ("don't sweat it — it's not rocket science"), kept long forms in the reference-style Notes, and replaced the fake credentials with placeholders (`sk-1a2b3c-...` -> `<your_access_token>`, `admin@acme-corp.com` -> `admin@example.com`). Swapped "Utilize" -> "Use".
- Terminology, product/tool names: Tower -> Seqera Platform; the platform -> Seqera Platform; NextFlow -> Nextflow; multiQC -> MultiQC (4 fixes); lowercased 3 feature nouns (Credentials, Compute Environments, Workspace); put `TOWER_ACCESS_TOKEN` in backticks; expanded HPC and GCP on first use.
- Terminology, precision and formatting: "The workflow failed to launch" -> "The pipeline failed to launch" (Platform item, per facts); "the executions" -> "the run"; "Each job ran on its own node" -> "Each task ran on its own node" (3 fixes); corrected 3 UI names (Launch Pad -> **Launchpad**, data explorer -> **Data Explorer**, runs tab -> **Runs** tab); `Launch` button -> **Launch** (bold UI, not backticks); backticked `--profile` and `nextflow.config`.
- Clarity: defined "executor" on first use using the supplied fact (the system that runs pipeline tasks, such as AWS Batch or Kubernetes); split the 47-word credentials sentence into two and pulled the trailing list (instances, storage, networking) into a short follow-up sentence; flagged the recurring "executor" as a glossary candidate."""),
    "eval-5-topic-types-rule-family": (
"""# Workspaces

A workspace groups the pipelines, compute environments, and credentials a team shares. Use a workspace to give a team a single place to launch and manage their work.

## Create a workspace

Create a workspace to give a team a shared place for its pipelines, compute environments, and credentials.

:::info[**Prerequisites**]

You need the following:

- An organization.

:::

1. Go to the organization.
2. Select **New**.
3. Enter a name.
4. Select **Add**.

# Workspace settings

| Setting    | Type    | Default | Description                                                  |
| ---------- | ------- | ------- | ------------------------------------------------------------ |
| `region`   | string  | —       | AWS region where the compute environment runs.               |
| `workDir`  | string  | —       | Work directory for pipeline scratch and intermediate files.  |
| `maxCpus`  | integer | `256`   | Maximum vCPUs the compute environment provisions.            |

# Error: `AccessDenied (Service: S3, Status Code: 403)` when launching a run

This error occurs when the compute environment credentials lack write access to the work-directory bucket.

To resolve:

1. Grant the credentials `s3:PutObject` on the work-directory bucket.
2. Relaunch the run.

# Tutorial: Run nf-core/rnaseq on AWS Batch

In this tutorial, you set up an AWS Batch compute environment, launch the nf-core/rnaseq pipeline, and review the results. By the end, you have a completed rnaseq run.

:::info[**Prerequisites**]

You need the following:

- A Seqera Platform account and workspace.
- AWS credentials.
- An S3 bucket for the work directory.

:::

## Set up the compute environment

Create an AWS Batch compute environment in your workspace.

## Launch nf-core/rnaseq

Launch the nf-core/rnaseq pipeline against the AWS Batch compute environment.

## Review the results

Open the **Runs** tab to review the completed run.""",
"""- Split into four typed topics: **Concept** + **Task** (`Workspaces` / `Create a workspace`), **Reference** (`Workspace settings`), **Troubleshooting reference** (`Error: AccessDenied...`), and **Tutorial** (`Tutorial: Run nf-core/rnaseq on AWS Batch`).
- Concept: renamed `Overview` to `Workspaces` (noun, per concept rules); replaced the vague "organize your work" definition with a specific one; cut the self-referential opener ("This overview will help you understand them") and the restating `## Summary` section.
- Task: lifted the embedded numbered steps out of the concept into a `Create a workspace` task (active verb + noun); converted "You should make sure you have an organization" into a `:::info[**Prerequisites**]` admonition (the docs-structure Platform convention); rewrote "you navigate / you should click / you can enter" as imperative steps and added the missing final step `Select Add`; bolded the **New** and **Add** UI buttons.
- Reference: renamed `Settings` to `Workspace settings`; converted prose rows into a four-column table; cut the editorializing ("really important to choose this carefully", "As mentioned, this matters for cost"); added defaults (region/workDir none, maxCpus `256`).
- Troubleshooting: renamed `Launch problems` to the exact error message with an `Error:` prefix and backticks; cut "Don't worry!" and the hedge "a variety of factors"; restructured as symptom → cause → numbered resolution with the concrete `s3:PutObject` fix.
- Tutorial: renamed the title to `Tutorial:` + active verb (was a hyphen-separated title-case marketing string); cut the "fast-paced world / exciting journey" opener and inflated stakes; added a goal sentence with the stated outcome; converted prerequisite prose into a `:::info[**Prerequisites**]` admonition (docs-structure Platform convention); made each phase a `##` task section; cut the orphan `## More info` link-only section.
- Renamed every heading — flag for inbound anchor/TOC link updates.
- Flagged for review: the troubleshooting and tutorial both involve AWS/S3 specifics but the source doc didn't confirm the exact **Compute Envs** tab flow; UI labels beyond **New**, **Add**, and **Runs** were not invented."""),
    "eval-9-leave-inline-nextflow": (
"""# Run Nextflow pipelines

Nextflow is a workflow engine for running pipelines at scale. This page explains how to run and resume a pipeline.

To launch a pipeline, use `nextflow run`. Set the input samplesheet with `--input` (a pipeline parameter — two dashes), resume a previous run with `-resume`, and select a config profile with `-profile` (core options take a single dash).

The `workflow` block wires your processes together with channels.

## Troubleshooting

### Error: `Unable to acquire lock on session`

This error occurs when another Nextflow run is using the same session directory (the `.nextflow` directory).

To resolve, ensure no other run uses that directory, then re-run with `-resume`.""",
"""- Detected product **Nextflow** (open-source docs); classified as a **Task** (run/resume) with an inline **Troubleshooting** entry.
- Cut 8 slop items: marketing (powerful, cutting-edge), the sales verb (empowers), seamlessly, the self-referential opener, the "It's worth noting" hedge, "utilize" -> use, and the chatty troubleshooting opener ("Sometimes things go wrong", "don't worry", "a variety of factors").
- Applied Nextflow rules (`products/nextflow.md`): NextFlow -> Nextflow; fixed 3 flags to the correct dash count and backticked them (`--input` parameter, `-resume`/`-profile` core options); backticked `nextflow run` and the `workflow` DSL keyword; corrected "pipeline block" to the `workflow` block.
- Left the troubleshooting **inline**: Nextflow has no troubleshooting destination in this repo, so the section was NOT moved off-page and no destination path was invented. Reformatted the entry per the core rules (Error: heading with the message in backticks, symptom -> cause -> resolution).
- Reduced length ~15%."""),
    "eval-10-leave-inline-multiqc": (
"""# MultiQC reports

MultiQC aggregates results from many bioinformatics tools into a single report.

To generate a report, run `multiqc <analysis_directory>`. MultiQC scans the directory for recognized log files and builds the report.

## Troubleshooting

### Error: `No analysis results found`

This error occurs when MultiQC finds no recognized log files in the search path.

To resolve, point `multiqc` at the directory containing your tool outputs, confirm the tools are supported, then re-run.""",
"""- Detected product **MultiQC**; classified as a **Task** (generate a report) with an inline **Troubleshooting** entry.
- Cut 6 slop items: "comprehensive", "seamlessly", the self-referential opener, 2 filler adverbs (simply, basically), and the chatty troubleshooting opener ("don't worry", "a variety of factors").
- Applied MultiQC rules (`products/multiqc.md`): corrected the product name to **MultiQC** in prose (from "multiqc"/"multiQC") and kept the command `multiqc` lowercase in backticks.
- Left the troubleshooting **inline**: MultiQC has no troubleshooting destination in this repo, so the section was NOT moved off-page and no destination path was invented. Reformatted the entry per the core rules (Error: heading with the message in backticks, symptom -> cause -> resolution).
- Reduced length ~15%."""),
}

missing = set(grade.EVALS) - set(IDEALS)
if missing:
    raise SystemExit(f"No ideal output embedded for: {sorted(missing)}")

originals = grade.load_originals()
failures = 0
for key, (rewrite, summary) in IDEALS.items():
    conf = grade.EVALS[key]
    slop = grade.read(grade.INPUT_FILES[key]) if key in grade.INPUT_FILES else originals.get(key, "")
    if not slop:
        raise SystemExit(f"{key}: no original found (input file or evals.json fenced block)")
    original = slop  # gives shorter_than_original a realistic baseline

    # 1. Satisfiability: the ideal rewrite should pass everything.
    g = grade.grade_run(rewrite, summary, original, conf)
    s = g["summary"]
    print(f"\n{key}")
    print(f"  ideal rewrite: {s['passed']}/{s['total']} assertions pass")
    for e in g["expectations"]:
        if not e["passed"]:
            failures += 1
            print(f"    IDEAL FAIL: {e['text']}  ->  {e['evidence']}")

    # 2. Discrimination: the raw slop (empty summary) must NOT pass everything.
    gb = grade.grade_run(slop, "", original, conf)
    sb = gb["summary"]
    if sb["pass_rate"] >= 1.0:
        failures += 1
        print(f"    DISCRIMINATION FAIL: raw slop passed all {sb['total']} assertions")
    else:
        print(f"  raw slop: {sb['passed']}/{sb['total']} pass (correctly detects slop)")

print("\n" + ("ALL GOOD — every eval is satisfiable and discriminating"
              if failures == 0 else f"{failures} FAILURE(S)"))
sys.exit(1 if failures else 0)
