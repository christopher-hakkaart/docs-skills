## Sign in

Use the form to sign in, for example with your email.
Because the token is missing, you cannot launch a run.
Set `TOWER_ACCESS_TOKEN` to authenticate, then select **Launch** to start.

Seqera Platform submits the job to AWS Batch and generates a new access token.
Run the migration before you upgrade.
This release reduces run-submission p99 latency from 12s to 4s and adds support for Google Cloud Batch, joining AWS Batch and Azure Batch.
Runs use high-performance computing (HPC) or Google Cloud Platform (GCP) backends.

## Configure the compute environment

Seqera Platform stores your credentials and compute environments per workspace.
The executor — the system that runs pipeline tasks, such as AWS Batch or Kubernetes — runs the Nextflow pipeline tasks automatically.
When you configure a compute environment, make sure your credentials have the right permissions for the cloud provider.
The credentials need permission to create and manage instances, storage, and networking.
The executor and the scheduler then coordinate.

## Review the run

The pipeline failed to launch from the **Launchpad**.
Open **Data Explorer**, then check the runs in the **Runs** tab and view the MultiQC report.
Set the `--profile` flag and open `nextflow.config`.
Each task runs on its own node.

## Notes

Several custom settings for project integrations are available.
Configure these settings early.
When a run fails, control the retry logic.
Use these settings later.

For testing, use the token `<your_access_token>` and the email address alex@example.com.
