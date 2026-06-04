# Change summary

- Classified as **Reference** — each release note entry is a typed lookup item, so the page follows Reference rules. Kept the entries as bulleted lists (not tables), per the release-notes rule and Example 6.
- Surfaced **Breaking changes** near the top as a distinct section so they aren't buried, and replaced the vague "review the migration guide carefully" placeholder with the actual migration guide link.
- Replaced 3 vague performance bullets with the specific change + magnitude + issue number, using the supplied facts: run submission p99 12s → 4s (#1842), Launchpad ~3x faster via paginated query for >1000 pipelines (#1856), Data Explorer batched bucket-listing API calls (#1871).
- Filled in the 2 breaking changes from the supplied facts (the original "Breaking Changes" section had no content): removed `tw --token` flag (use `TOWER_ACCESS_TOKEN`), and changed the CLI default output from JSON to `table` (set with `--output`).
- Expanded the 3 vague security bullets into specific additions: SAML 2.0 / OIDC single sign-on, RBAC with five built-in roles plus custom roles, audit logging to S3 with optional WORM retention.
- Cut ~15 marketing/puffery terms and slop verbs/phrases (powerful, robust, comprehensive, blazing fast, cutting-edge, quantum leap, seamlessly, empowers, harness, leverages, paramount, worked tirelessly, It's worth noting, Let's dive into, but are not limited to).
- Cut the marketing opener, the "What's New" framing, the self-referential "Developer Experience" section (no specific supplied facts), and the "Conclusion" section (signposted wrap-ups are out for Reference).
- Applied terminology rules: kept `tw` and `TOWER_ACCESS_TOKEN` in backticks; bolded **Launchpad** and **Data Explorer** as UI names; sentence-case headings; present tense; active voice; spelled out SSO, OIDC, RBAC, and WORM on first use with the abbreviation in parentheses.
- Reduced length roughly 60% (about 320 → about 130 words).

Renamed headings (anchors changed — update inbound/TOC links): `What's New` removed; `Performance Improvements` → `Performance`; `Enhanced Security` → `Security`; `Developer Experience` removed; `Breaking Changes` → `Breaking changes` (sentence case); `Conclusion` removed.

Flagged for review: the original "Developer Experience" section claimed broad CLI/API/docs improvements with no specifics. The only concrete supplied fact (default output format change) is a breaking change, so the section was dropped rather than padded. Confirm there are no other developer-experience changes to list.
