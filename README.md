# api-contracts

Единое хранилище **HTTP API-контрактов** платформы (OpenAPI 3.1).

**GitHub:** https://github.com/couragegang/api-contracts

**ADR:** [`cursor-context/docs/adr-001-api-contracts-openapi.md`](../../cursor-context/docs/adr-001-api-contracts-openapi.md)  
**Модель данных (отдельно):** [`cursor-context/docs/erd-and-bounded-contexts.md`](../../cursor-context/docs/erd-and-bounded-contexts.md)  
**UI → API:** [`cursor-context/docs/ui-api-scenarios.md`](../../cursor-context/docs/ui-api-scenarios.md)

## Структура

| Путь | Сервис | Префикс runtime | Статус |
|------|--------|-------------------|--------|
| [`iam/openapi.yaml`](iam/openapi.yaml) | iam-service | `/v1/iam` | **канон** (V4 groups) |
| [`config/openapi.yaml`](config/openapi.yaml) | config-service | `/v1/config` | черновик |
| [`mcp/openapi.yaml`](mcp/openapi.yaml) | mcp-gateway | `/v1/mcp` | черновик |
| [`ai/openapi.yaml`](ai/openapi.yaml) | ai-runtime | `/v1/ai` | черновик |
| [`bff/openapi.yaml`](bff/openapi.yaml) | bff-gateway | `/v1/bff` | черновик |
| [`policy/openapi.yaml`](policy/openapi.yaml) | policy-service | `/v1/policy` | черновик |
| [`audit/openapi.yaml`](audit/openapi.yaml) | audit-service | `/v1/audit` | черновик |
| [`billing/openapi.yaml`](billing/openapi.yaml) | billing-service | `/v1/billing` | черновик |
| [`common/`](common/) | — | — | общие схемы |

## Правила

1. **Канон контракта** — файлы в этом репозитории; в сервисах — копия или CI diff (см. ADR).
2. **ERD не генерируется из OpenAPI** — только DTO и пути.
3. **Версионирование** — semver в `info.version` каждого spec; breaking changes — отдельный PR + oasdiff.
4. **Internal paths** — tag `internal`, не включать в BFF bundle для браузера.

## Локальная проверка

```bash
# Redocly (опционально: npm i -g @redocly/cli)
redocly lint iam/openapi.yaml
redocly bundle iam/openapi.yaml -o dist/iam-bundled.yaml
```

Скрипт-обёртка: [`scripts/lint.ps1`](scripts/lint.ps1).

## Связь с `iam-service`

Спека IAM перенесена сюда и дополнена **V4** (groups, `accessScope`, invite `groupId`).  
В `iam-service/openapi/openapi.yaml` — синхронизировать при следующем изменении API (или submodule).
