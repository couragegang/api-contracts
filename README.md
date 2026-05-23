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

## Локальная проверка и CI

**Quality gate** (GitHub Actions [`.github/workflows/quality.yml`](.github/workflows/quality.yml)):

| Job | Назначение |
|-----|------------|
| **contract-freshness** | Канон совпадает с зеркалами в сервисах ([`contracts-sync.json`](contracts-sync.json)); в CI клонируются `iam-service`, `config-service`, `mcp-gateway` |
| **redocly-lint** | `redocly lint` по [`redocly.yaml`](redocly.yaml) |

```bash
cd services/api-contracts
npm run quality          # актуальность зеркал (monorepo: SERVICES_ROOT=.. по умолчанию)
npm ci && npm run quality:full   # + Redocly lint
npm run lint             # только Redocly
```

PowerShell: [`scripts/verify-quality.ps1`](scripts/verify-quality.ps1). Устаревший пофайловый lint: [`scripts/lint.ps1`](scripts/lint.ps1).

## Зеркала OpenAPI в сервисах

Канон — файлы в этом репозитории. Копии для codegen/доков — см. [`contracts-sync.json`](contracts-sync.json).

После правок контракта синхронизировать зеркало:

```bash
./scripts/sync-openapi-mirror.sh iam    # или config, mcp
./scripts/sync-iam-openapi.sh           # alias для iam
```

```powershell
.\scripts\sync-openapi-mirror.ps1 -Id iam
```
