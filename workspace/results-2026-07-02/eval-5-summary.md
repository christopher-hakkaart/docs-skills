# Change summary

- **Seqera Platform** (detected from content vocabulary: workspace, compute environment, nf-core/rnaseq, **Runs** tab). The single file mixed four topics; split and re-typed into five topics: **Concept** (`Workspaces`), **Task** (`Create a workspace`), **Reference** (`Compute environment settings`), **Troubleshooting reference** (the launch error), and **Tutorial** (`Tutorial: Run nf-core/rnaseq on AWS Batch`).

- **Concept** — retitled `Overview` to the noun `Workspaces` (avoids the banned `Overview` title). Replaced the vague "Workspaces organize your work" plus self-referential "This overview will help you understand them" with the direct definition from the facts. Removed the embedded numbered steps (moved to the Task) and cut the `## Summary` / "That's how workspaces work!" section.

- **Task** — created `Create a workspace` (active verb + noun). Converted "You should make sure you have an organization" prose into a `:::info[**Prerequisites**]` admonition with a `You need the following:` lead-in and a noun-phrase bullet (docs-structure prerequisites convention). Rewrote the inline "1) you navigate... 2) you should click New... 3) you can enter a name" into imperative numbered steps (`Go to`, `Select`, `Enter`); added the missing `Select **Add**` step from the facts; click -> select; `New`/`Add` bolded as UI labels.

- **Reference** — converted the three prose setting lines into a `Setting | Type | Default | Description` table (one row per setting). Cut the prose narrative between rows ("It's really important to choose this carefully...", "As mentioned, this matters for cost"). Added the `maxCpus` default of `256`; marked `region` and `workDir` as having no default (—). Settings placed in backticks.

- **Troubleshooting** — retitled `Launch problems` and moved the entry off the feature page per step 6 (docs-structure troubleshooting placement): destination is `platform-cloud/docs/troubleshooting_and_faqs/aws_troubleshooting.md` (S3 AccessDenied on AWS Batch credentials), with a one-line pointer left on the source page. Reformatted the entry with an `Error:` prefix and the real message in backticks (`AccessDenied (Service: S3, Status Code: 403)`), dropped the chatty opener ("Don't worry!"), replaced the hedge "a variety of factors" with the single named cause, and structured the body as symptom -> cause -> numbered resolution using "To resolve".

- **Tutorial** — retitled the hyphen-separated, title-cased `Pipeline Walkthrough - A Complete And Exhaustive End To End Guide To Everything` to `Tutorial: Run nf-core/rnaseq on AWS Batch` (Tutorial: prefix, active verb, sentence case, under 70 chars, no hyphen separator). Cut the hype/journey opener ("In today's fast-paced world, let's embark on an exciting journey..."). Opened with a one-sentence goal and stated outcome. Converted prerequisites to the `:::info[**Prerequisites**]` admonition (account and workspace, AWS credentials, S3 bucket). Turned "First... Then... Finally" prose into active-verb task sections (`Set up the compute environment`, `Launch the pipeline`, `Review the run`); results reviewed in the **Runs** tab. Folded the one-line `## More info` / "See the other page" stub into a `## Related topics` link instead of its own topic.

## Step 6 (docs-structure handoff)

- Applied both docs-structure conventions inline (pasted-text eval, no repo file to move into; read both `references/prerequisites.md` and `references/troubleshooting.md`): prerequisites reformatted into `:::info[**Prerequisites**]` admonitions on the Task and Tutorial; the troubleshooting entry moved off-page with a pointer left behind.

## Renamed-heading anchor flags (inbound links may break)

- `#overview` -> `#workspaces`
- `#settings` -> `#compute-environment-settings`
- `#launch-problems` -> troubleshooting content moved to `aws_troubleshooting.md#error-accessdenied-service-s3-status-code-403-when-launching-a-run`
- `#pipeline-walkthrough...` -> `#tutorial-run-nf-corernaseq-on-aws-batch`

## Flagged for review

- The Tutorial's `## Related topics` link target is unknown — the original said only "See the other page." Confirm and repoint the link; it is currently a placeholder.
- The Reference `Type` column (string/integer) is inferred from the setting semantics, not supplied in the facts. Confirm before publishing.
