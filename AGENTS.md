<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

⚠️ Сначала прочитайте [корневой AGENTS.md](/int/AGENTS.md).

# AGENTS — Leonid public site

## Allowed scope

- личный сайт, публичные материалы, резюме, docs/lab/edu/archive контент;
- презентационные и контентные изменения внутри этого repo;
- public-facing assets и repo-level docs, относящиеся только к сайту владельца.

## Source-of-truth ownership

- `/int/leonid` владеет только personal/public content владельца;
- не является source-of-truth для family backend-core, product contracts или machine-wide tooling;
- не подменяет ownership других top-level repos в `/int`.

## What not to mutate

- не переносить сюда product-core семейства;
- не смешивать личный сайт и operational/runtime state других проектов;
- не хранить здесь machine-wide tooling как source-of-truth.

## Integration expectations

- сайт может ссылаться на публичные материалы и проекты владельца, но не владеет их runtime;
- любые product/runtime интеграции остаются внешними ссылками, а не ownership-переносом;
- repo остаётся вне архитектуры canonical `intdata core`.

## Escalation triggers

- попытка разместить здесь product-core или ops-runtime других проектов;
- смешение personal/public content и internal process tooling;
- решения, которые делают repo зависимым owner-контуром family backend.
