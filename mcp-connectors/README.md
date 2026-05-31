# MCP connector runtime contracts

OpenAPI для **data plane** MCP-коннекторов (`mcp-notion`, …).  
Control plane — [`../mcp/openapi.yaml`](../mcp/openapi.yaml) (`mcp-gateway`).

| Путь | Назначение |
|------|------------|
| [`runtime/openapi.yaml`](runtime/openapi.yaml) | Общие internal: invoke, health, normalize-config |
| [`connectors/notion/openapi.yaml`](connectors/notion/openapi.yaml) | Notion + discover |
| [`connectors/trello/openapi.yaml`](connectors/trello/openapi.yaml) | Trello + discover |
| [`docs/connector-ports.md`](docs/connector-ports.md) | Порты 8091+ |
| **Новый коннектор** | [`cursor-context/docs/how-to-add-mcp-connector.md`](../../../cursor-context/docs/how-to-add-mcp-connector.md) |
| ADR | [`cursor-context/docs/adr-002-mcp-connector-runtime-http.md`](../../../cursor-context/docs/adr-002-mcp-connector-runtime-http.md) |

Синхронизация зеркала в BC:

```powershell
.\scripts\sync-openapi-mirror.ps1 -Id mcp-notion
```
