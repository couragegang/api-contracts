# Шаблон OpenAPI для MCP-коннектора `{key}`

Полный чеклист (BC, gateway, compose, n8n, ai-runtime):  
[`cursor-context/docs/how-to-add-mcp-connector.md`](../../../../cursor-context/docs/how-to-add-mcp-connector.md).

## Только контракты (этот репозиторий)

1. Скопировать [`connectors/notion/openapi.yaml`](../notion/openapi.yaml) → `connectors/{key}/openapi.yaml`.
2. Обновить `servers.url` (порт из [`docs/connector-ports.md`](../../docs/connector-ports.md)).
3. Добавить connector-specific paths в `components` / `paths`.
4. Добавить запись в [`contracts-sync.json`](../../contracts-sync.json) → `mirrors[]`:

   ```json
   {
     "id": "mcp-{key}",
     "canonical": "mcp-connectors/connectors/{key}/openapi.yaml",
     "serviceRepo": "couragegang/mcp-{key}",
     "serviceDir": "mcp-{key}",
     "serviceCopy": "openapi/openapi.yaml"
   }
   ```

5. Обновить [`docs/connector-ports.md`](../../docs/connector-ports.md) и [`redocly.yaml`](../../redocly.yaml).
6. Создать репозиторий `couragegang/mcp-{key}` и зеркало `openapi/openapi.yaml`.
7. Синхронизация: `.\scripts\sync-openapi-mirror.ps1 -Id mcp-{key}`.

Общие runtime paths — `$ref` на [`runtime/openapi.yaml`](../../runtime/openapi.yaml) (invoke, health, normalize-config).
