## Token handling

The access token expires after 1 hour. Refresh it before a run. Keep tokens short-lived.

The schema is cached. After you change the schema, restart to pick up the changes.

## Retry behavior

Failed tasks retry automatically up to 3 times, with exponential backoff starting at 30 seconds.

A run fails when the account hits its vCPU quota. The platform checks the quota before submitting jobs and queues the run if the quota is exceeded.

## Run characteristics

- Runs start in under 30 seconds on a warm environment.
- Failed tasks retry automatically up to 3 times.
- Credentials are encrypted at rest.

## Configure a run

1. Set the `--profile` flag.
2. Set the region, work directory, and max CPUs.
3. Enable retries.
