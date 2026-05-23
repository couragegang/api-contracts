#!/usr/bin/env bash
# Копирует канон OpenAPI в зеркало сервиса (см. contracts-sync.json, поле id).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IDS="$(node -e "const m=require('${ROOT}/contracts-sync.json');console.log(m.mirrors.map(x=>x.id).join('|'))")"
ID="${1:?Usage: $0 <${IDS}>}"
node -e "
const fs = require('fs');
const path = require('path');
const { mirrors } = JSON.parse(fs.readFileSync(path.join('$ROOT', 'contracts-sync.json'), 'utf8'));
const m = mirrors.find(x => x.id === '$ID');
if (!m) { console.error('Unknown id: $ID'); process.exit(1); }
const src = path.join('$ROOT', m.canonical);
const dest = path.join('$ROOT', '..', m.serviceDir, m.serviceCopy);
fs.mkdirSync(path.dirname(dest), { recursive: true });
fs.copyFileSync(src, dest);
console.log('Synced', m.id, ':', src, '->', dest);
"
