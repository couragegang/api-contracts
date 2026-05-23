#!/usr/bin/env bash
# Quality gate: Redocly lint + зеркала OpenAPI в сервисах (contracts-sync.json).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Redocly lint ==="
npx --no-install redocly lint

echo "=== Contract mirrors (canonical vs service copies) ==="
export REQUIRE_SYNC_CHECK="${REQUIRE_SYNC_CHECK:-${GITHUB_ACTIONS:-}}"
node scripts/verify-sync.mjs

echo "=== Quality gate passed ==="
