## Workspaces

A workspace groups the pipelines, compute environments, and credentials that a team shares. Each workspace belongs to an organization.

## Create a workspace

Create a workspace to give a team a shared set of pipelines, compute environments, and credentials.

Prerequisites:

- An organization.

To create a workspace:

1. Go to the organization.
2. Select **New**.
3. Enter a name.
4. Select **Add**.

## Compute environment settings

| Setting   | Type    | Default | Description                                         |
| --------- | ------- | ------- | --------------------------------------------------- |
| `region`  | string  | —       | AWS region where jobs run. Affects latency.         |
| `workDir` | string  | —       | S3 bucket path for pipeline scratch and intermediate files. |
| `maxCpus` | integer | `256`   | Maximum vCPUs provisioned across all jobs.          |

## Error: `AccessDenied (Service: S3, Status Code: 403)` when launching a run

This error occurs when the compute environment's credentials lack write access to the work-directory bucket.

To resolve:

1. Grant the credentials `s3:PutObject` on the work-directory bucket.
2. Relaunch the run.

## Tutorial: Run nf-core/rnaseq on AWS Batch

In this tutorial, you set up an AWS Batch compute environment, launch the nf-core/rnaseq pipeline, and review the results. By the end, you have a completed rnaseq run.

### Before you begin

You need:

- A Seqera Platform account and workspace.
- AWS credentials.
- An S3 bucket for the work directory.

### Set up the compute environment

Create an AWS Batch compute environment in your workspace.

### Launch the pipeline

Launch the nf-core/rnaseq pipeline against the compute environment.

### Review the results

Open the **Runs** tab and review the run results.
