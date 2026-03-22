# Intelligent Data ERP

`/int/erp` — standalone ERP contour семейства Intelligent Data.

## Target Role

`/int/erp` — `standalone-product`: ERP runtime и deploy/docs слой, работающий независимо от canonical backend-core.

## Canonical Ownership

- `/int/erp` владеет Odoo/ERPNext compose, vendor integration code и ERP-specific configs;
- canonical backend-core живёт в [`/int/data`](../data/README.md);
- machine-wide tooling и shared backend ownership сюда не переносятся.

## What Lives Here

- `docker-compose.yaml` и ERP-specific configuration;
- Keycloak/OIDC integration helpers;
- ERP-specific docs и deploy scripts.

## What Must Not Live Here

- canonical backend schema/functions/contracts;
- machine-wide tooling;
- реальные `.env`, секреты и mutable runtime-state.

## Integration Expectations

- ERP runtime интегрируется с canonical core и control-plane через внешние APIs/contracts;
- repo остаётся owner-репозиторием ERP deploy/docs слоя;
- ERP-specific vendor adapters живут здесь, а не в shared backend-core.
