# ores-supabase

Git-backed Supabase provider overlays for [`oresoftware`](https://supabase.com/dashboard/org/zmkmcdyrryxxhleytdho), mapped to [`ORESoftware`](https://github.com/ORESoftware).

`ORESoftware` is a GitHub user namespace rather than a GitHub Organization. It is the explicit owner-namespace exception for this otherwise organization-oriented mapping.

## Project inventory

Live provider read-back on 2026-09-11 found two `ACTIVE_HEALTHY` projects in the configured Supabase organization. Existence and schema inventory are verified; Git integration, production deployment, and repository baselines remain deliberately unverified until their stronger gates complete.

| Project ref | Local slug | Canonical | Provider status | Contract source | Git integration | Baseline |
|---|---|---:|---|---|---|---|
| `szzbuljocwprjhaqnbvb` | `ores-shared-auth` | no | active | `shared-auth/shared-auth-lib-core` (partial) | planned | pending |
| `sznvdzulwlaghrrpiebd` | `multi-app-3fa-app` | yes | active | `3FA-app/3fa-lib-core` (partial) | planned | pending |

The auth role is supported by read-only schema evidence: `szzbuljocwprjhaqnbvb` has a dedicated `shared_auth` schema. The canonical designation identifies the current non-auth project in this two-project shared-organization model; it does **not** mean its Git integration, migration baseline, contract source, or production deployment is verified.

Both projects returned zero Supabase security-advisor findings during the same read-only audit. That is security evidence, not permission to skip baseline, RLS/grant, migration, or Git-integration verification.

The catalog is `catalog.json`; each hosted project has a machine-readable `target.json`. Project refs and organization refs are public routing identifiers, not credentials. Database passwords, connection URLs, tokens, keys, data, and dumps never belong in this repository.

## Authority

- Cross-database persistence contracts: the target's `contractSource`, preferring `*-lib-core`.
- Supabase-only provider overlays: this repository.
- Explicit convergence and drift analysis: [`declarative-migrations/declarative-postgres-migrate.rs`](https://github.com/declarative-migrations/declarative-postgres-migrate.rs).
- Fleet target registry and verification: [`ORESoftware/k8s-libs-and-shared-defs`](https://github.com/ORESoftware/k8s-libs-and-shared-defs).
- API, authentication, and synchronization dependencies remain owned by [`ORESoftware/api-docs`](https://github.com/ORESoftware/api-docs), [`shared-auth`](https://github.com/shared-auth), and [`opto-sync`](https://github.com/opto-sync).

Supabase and AWS RDS Postgres may be intentionally out of step. No automated job treats catalog equality as an invariant.

## Current gate

All discovered targets begin with Git integration `planned` and baseline `pending`. Production deployment is disabled until a reviewed baseline, contract-source readiness, migration/RLS/grant tests, branch protection, exact repository/working-directory verification, provider preview, and production read-back are recorded.

Current Supabase guidance separates local `[api].schemas` configuration from hosted Data API grants/default privileges. This repository therefore constrains exposed schemas in `supabase/config.toml`, while hosted grants/default privileges remain an explicit provider verification item; it does not invent a non-standard `auto_expose_new_tables` TOML field.

Run:

```sh
just validate
```

See `docs/architecture.md`, `docs/schema-authority.md`, and `docs/github-integration.md`.
