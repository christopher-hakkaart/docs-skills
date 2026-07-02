# Seqera Platform v24.1 release notes

Seqera Platform 24.1 reduces run-submission latency, adds single sign-on and role-based access control, and changes two CLI defaults.
This release includes breaking changes. See [Breaking changes](#breaking-changes) before you upgrade.

## Performance

- **Run submission**: p99 latency to AWS Batch compute environments dropped from 12s to 4s (#1842).
- **Launchpad**: The pipeline list now loads through a paginated query, about 3x faster for workspaces with more than 1000 pipelines (#1856).
- **Data Explorer**: Bucket listing batches storage API calls instead of issuing them sequentially (#1871).

## Security

- Single sign-on with Security Assertion Markup Language (SAML) 2.0 and OpenID Connect (OIDC).
- Role-based access control (RBAC) with 5 built-in roles, plus custom roles.
- Audit log writes to Amazon S3, with optional write-once-read-many (WORM) retention.

## Breaking changes

Review the [migration guide](https://docs.seqera.io/platform-cloud/migrate/24.1) before you upgrade.

- The deprecated `tw --token` flag is removed. Set `TOWER_ACCESS_TOKEN` instead.
- The CLI default output format is now `table` (was JSON). Set the format with `--output`.
