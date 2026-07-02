The source mixed four unrelated topics under one file. Split into typed topics below: a Concept, a Task, a Reference, a Tutorial, and a Troubleshooting entry that moves off-page (step 6). Each would normally be its own page.

# Workspaces

A workspace groups the pipelines, compute environments, and credentials that a team shares.

# Create a workspace

Create a workspace to group the pipelines, compute environments, and credentials for a team.

:::info[**Prerequisites**]

You need the following:

- An organization.

:::

To create a workspace:

1. Go to the organization.
2. Select **New**.
3. Enter a name.
4. Select **Add**.

# Compute environment settings

| Setting   | Type    | Default | Description                |
| --------- | ------- | ------- | -------------------------- |
| `region`  | string  | —       | AWS region.                |
| `workDir` | string  | —       | Work directory for runs.   |
| `maxCpus` | integer | `256`   | Maximum number of CPUs.    |

# Launch problems

For access-denied errors when launching a run, see [AWS troubleshooting](../troubleshooting_and_faqs/aws_troubleshooting).

<!--
Moved off this page per the docs-structure troubleshooting convention. The entry
below belongs on platform-cloud/docs/troubleshooting_and_faqs/aws_troubleshooting.md
(an S3 AccessDenied failure for AWS Batch compute environment credentials).

## Error: `AccessDenied (Service: S3, Status Code: 403)` when launching a run

This error occurs when the compute environment credentials lack write access to the work-directory bucket.

To resolve:

1. Grant the credentials `s3:PutObject` on the work-directory bucket.
2. Relaunch the run.
-->

# Tutorial: Run nf-core/rnaseq on AWS Batch

Set up an AWS Batch compute environment, launch the nf-core/rnaseq pipeline, and review the results. By the end, you have a completed rnaseq run.

:::info[**Prerequisites**]

You need the following:

- A Seqera Platform account and workspace.
- AWS credentials.
- An S3 bucket for the work directory.

:::

## Set up the compute environment

Create an AWS Batch compute environment in your workspace.

## Launch the pipeline

Launch the nf-core/rnaseq pipeline on the AWS Batch compute environment.

## Review the run

When the run completes, review the results in the **Runs** tab.

## Related topics

- [Create a workspace](#)
