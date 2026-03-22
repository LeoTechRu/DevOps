# Intelligent Data ITSM

`/int/itsm` — standalone ITSM/Flowable service layer семейства Intelligent Data.

## Target Role

`/int/itsm` — `standalone-product`: tickets/workflows runtime contour, который интегрируется с canonical core извне.

## Canonical Ownership

- `/int/itsm` владеет ITSM service code, BPMN/migrations и deploy helpers;
- canonical backend-core живёт в [`/int/data`](../data/README.md);
- shared schema/functions/contracts и machine-wide tooling сюда не переносятся.

## What Lives Here

- ITSM domain code;
- BPMN, migrations и Flowable client layer;
- ITSM docs и deploy helpers.

## What Must Not Live Here

- canonical shared backend schema/functions/contracts;
- machine-wide ops/process mirrors;
- runtime-state и рабочие секреты.

## Integration Expectations

- repo интегрируется с `/int/data` как с внешним backend/data-core;
- workflow и ticketing integrations оформляются через публичные APIs/contracts;
- `/int/itsm` остаётся owner-репозиторием своего runtime/deploy слоя.
