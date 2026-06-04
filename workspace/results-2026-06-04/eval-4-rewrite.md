# Configure the compute environment

Seqera Platform stores your credentials and compute environments per workspace. The executor — the system that runs pipeline tasks, such as AWS Batch or Kubernetes — runs the Nextflow tasks and coordinates with the scheduler. Each task runs on its own node.

## Prerequisites

- Credentials for your cloud provider, with permission to create and manage instances, storage, and networking.
- A value for `TOWER_ACCESS_TOKEN`. Without a token, you cannot launch a run.

## Sign in and launch a run

1. Use the sign-in form to authenticate, for example with your email.
2. Set `TOWER_ACCESS_TOKEN` to authenticate.
3. Select **Launch** to submit the run.

Seqera Platform submits the job to AWS Batch. This release reduces run-submission p99 latency from 12s to 4s and adds support for Google Cloud Batch, joining AWS Batch and Azure Batch.

## Notes

This section is reference material for configuring a compute environment.

- Several custom settings for project integrations are available. Configure these early.
- To handle launch failures, control the retry logic.
- Generate a new access token, then run the migration before you perform the upgrade.
- If a pipeline fails to launch from the **Launchpad**, open the **Data Explorer**, check the executions in the **Runs** tab, and view the MultiQC report. Set the `--profile` flag and open `nextflow.config`.
- For testing, use the token `<your_access_token>` and the email `admin@example.com`.
