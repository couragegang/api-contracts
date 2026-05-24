# Шаблон нового MCP-коннектора

1. Скопировать `connectors/notion/openapi.yaml` → `connectors/{connectorKey}/openapi.yaml`.
2. Обновить `servers.url` (порт из [`docs/connector-ports.md`](../docs/connector-ports.md)).
3. Добавить connector-specific paths в `components`.
4. Добавить запись в [`contracts-sync.json`](../../contracts-sync.json) → `mirrors[]` (id `mcp-{key}`).
5. Обновить `docs/connector-ports.md` и [`redocly.yaml`](../../redocly.yaml).
6. Создать репозиторий `couragegang/mcp-{connectorKey}` и зеркало `openapi/openapi.yaml`.

Shared runtime paths — `$ref` на [`runtime/openapi.yaml`](../../runtime/openapi.yaml).
