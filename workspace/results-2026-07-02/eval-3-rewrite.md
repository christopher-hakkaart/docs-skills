## Token handling

Failed tasks retry automatically up to three times, with exponential backoff starting at 30 seconds. A run fails when the account reaches its vCPU quota. Seqera Platform checks the quota before submitting jobs and queues the run if the quota is exceeded.

Seqera Platform runs have the following characteristics:

- Runs start in under 30 seconds on a warm environment.
- Tasks retry automatically up to three times.
- Credentials are encrypted at rest.

The access token expires after one hour. Refresh it before a run and keep tokens short-lived. The schema cache requires a restart after any changes.

Set the following:

- the `--profile` flag
- region, work directory, and max CPUs
- enable retries
