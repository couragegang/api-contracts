# Реестр портов MCP connector BC (local / docker compose)

Канон в **`api-contracts/mcp-connectors/docs/connector-ports.md`**.  
План: [`cursor-context/docs/plan-mcp-connectors-n8n-orchestration.md`](../../../../cursor-context/docs/plan-mcp-connectors-n8n-orchestration.md).

## Platform services (справка)

| Сервис | Порт | Примечание |
|--------|------|------------|
| mcp-gateway | 8081 | control plane (`api-contracts/mcp`) |
| ai-runtime | 8083 | чат |
| policy-service | 8085 | HITL |
| knowledge-service | 8088 | RAG |
| n8n | 5678 | оркестрация (фаза 2+) |

## Connector runtime (data plane)

| connectorKey | Сервис (compose) | Host port | `runtime_base_url` (docker network) | Репозиторий |
|--------------|------------------|-----------|----------------------------------------|-------------|
| `notion` | `mcp-notion` | **8091** | `http://mcp-notion:8091/v1/notion` | `couragegang/mcp-notion` |
| `trello` | `mcp-trello` | **8092** | `http://mcp-trello:8092/v1/trello` | `couragegang/mcp-trello` |
| *(резерв)* | — | **8093–8099** | — | следующие коннекторы |

## Правила выделения портов

1. Диапазон **8091–8099** — MCP connectors в локальном compose.
2. `context-path` = `/v1/{connectorKey}`.
3. При новом коннекторе: обновить таблицу, `contracts-sync.json`, seed каталога в `mcp-gateway`.
