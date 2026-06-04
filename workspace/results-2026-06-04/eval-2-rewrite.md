# Compute environments

A compute environment defines where a pipeline runs: the execution backend (AWS Batch, Azure Batch, Google Cloud Batch, Kubernetes, or an HPC scheduler), the credentials used to access it, and the work directory for pipeline runs. A workspace can hold multiple compute environments.

Configure credentials before you create a compute environment. Seqera Platform supports AWS, Azure, and Google Cloud. Validating credentials before a run surfaces permission errors at setup instead of at launch.

Stored credentials connect Seqera Platform to cloud storage, and validation checks the stored values before any run. Unset optional fields fall back to placeholder values. Seqera Platform reads only from buckets on the storage allowlist, and pipelines track the main branch of their repository by default.

This release adds run-level cost reporting and a bulk relaunch action.

See the [credentials reference](#).
