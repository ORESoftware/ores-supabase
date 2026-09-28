# Provider-overlay ownership boundary

`ORESoftware/ores-supabase` is a fleet/provider inventory and read-back repository. It is **not** the deployment or persistence authority for individual products.

## Long-term ownership

This repository keeps reviewed Supabase project inventory, public routing identifiers, provider read-back/baseline status, fleet-level RLS/grant/security-advisor evidence, and provider-specific drift metadata. It may temporarily retain compatibility overlay files while a product's `*-infra` migration is explicit and frozen.

Product-owned Supabase migrations, Edge Function implementations, seeds, deployment orchestration, and integration wiring belong in the owning product's `*-infra` repository. For the currently inventoried projects those owners are:

- `3FA-app/3fa-infra` for project `sznvdzulwlaghrrpiebd`;
- `shared-auth/shared-auth-infra` for project `szzbuljocwprjhaqnbvb`.

The existing project trees are frozen to `target.json`, `supabase/config.toml`, and placeholder README files under `functions/` and `migrations/`. New product code or migration files are rejected here by `scripts/validate-ownership.py`.

## Composition without duplicate authority

- `ORESoftware/k8s-libs-and-shared-defs` owns genuinely shared infrastructure invariants/templates, not product database state.
- Product `*-interfaces` / `*-lib-core` own cross-database persistence contracts.
- Product `*-infra` owns concrete Supabase/Neon/provider deployment bindings and environment-specific migrations.
- `declarative-migrations/declarative-postgres-migrate.rs` performs explicit Postgres convergence/drift analysis.
- `ORESoftware/ores-supabase` records Supabase account/project inventory and fleet-level provider evidence.

Supabase and Neon may legitimately differ at a point in time. Equality between providers is not an authority rule; reviewed convergence and product contracts are.

## Secret boundary

Credentials, database passwords, service-role keys, tokens, connection URLs containing passwords, private keys, dumps, backups, and private application data never belong here. The ownership validator rejects common credential-bearing filenames and content patterns in the project overlay tree.

## Migration compatibility

Existing overlay files may be narrowed or removed as product `*-infra` takes ownership. Do not add new product-owned files here to ease migration. Consumers that still read `target.json` or provider evidence may continue doing so; deployment consumers should move to their product `*-infra` repository.
