# Supabase env/enc consumption

Driver: `ORESoftware/ores-docs#3`

This document is a bounded review contract for one slice of the driver issue. It is intentionally mergeable independently and does **not** claim the parent issue is fully implemented.

## Invariants

- Supabase URLs/keys are runtime configuration and never repository literals.
- Deployment environment (`dev|stage|prod`) stays orthogonal to execution profile.
- Only schema-authorized profile overrides may replace environment values.
- Decrypted material must stay out of Git, logs, artifacts, caches, and issue/PR text.

## Verification

- Review the exact PR head, not a synthetic or stale revision.
- Run the repository's normal format/lint/test/conformance gates that touch this boundary.
- Treat skipped or zero-step CI as missing evidence.
- Preserve existing public behavior unless the driver issue explicitly authorizes a breaking change.

## Non-goals

This slice does not add credentials, bypass branch protection, or declare the broader fleet rollout complete.
