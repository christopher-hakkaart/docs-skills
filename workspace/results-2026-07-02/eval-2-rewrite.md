# Compute environments

A compute environment defines where a pipeline runs: the execution backend, the credentials used to access it, and the work directory for pipeline runs. Supported backends are AWS Batch, Azure Batch, Google Cloud Batch, Kubernetes, and high-performance computing (HPC) schedulers. A workspace can hold multiple compute environments.

This release adds run-level cost reporting and a bulk relaunch action.

Configure your credentials before you create the compute environment. Seqera Platform connects to AWS, Azure, and Google Cloud. Validating credentials before a run surfaces permission errors at setup instead of at launch.

Stored credentials connect Seqera Platform to cloud storage. Validation checks the stored values before any run. Unset optional fields fall back to placeholder values. Seqera Platform reads only from buckets on the storage allowlist. Pipelines track the main branch of their repository by default.

For the credential settings, see the [credentials reference](#).
