#!/usr/bin/env node
/**
 * Проверяет, что локальные копии OpenAPI в сервисах совпадают с каноном в api-contracts.
 * SERVICES_ROOT — каталог с репозиториями сервисов (по умолчанию родитель api-contracts).
 */
import { createHash } from "crypto";
import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const manifest = JSON.parse(
  readFileSync(join(root, "contracts-sync.json"), "utf8")
);
const servicesRoot =
  process.env.SERVICES_ROOT?.trim() || join(root, "..");
const requireAll =
  process.env.REQUIRE_SYNC_CHECK === "1" || process.env.GITHUB_ACTIONS === "true";

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

let failed = false;

for (const m of manifest.mirrors) {
  const canon = join(root, m.canonical);
  const copy = join(servicesRoot, m.serviceDir, m.serviceCopy);

  if (!existsSync(canon)) {
    console.error(`MISSING canonical: ${canon}`);
    failed = true;
    continue;
  }
  if (!existsSync(copy)) {
    const msg = `SKIP (no mirror): ${m.id} -> ${copy}`;
    if (requireAll) {
      console.error(`MISSING mirror (required in CI): ${copy}`);
      console.error(`  Clone ${m.serviceRepo} under ${servicesRoot}/${m.serviceDir}`);
      failed = true;
    } else {
      console.warn(msg);
    }
    continue;
  }

  const canonHash = sha256(canon);
  const copyHash = sha256(copy);
  if (canonHash !== copyHash) {
    console.error(`DRIFT: ${m.id}`);
    console.error(`  canonical: ${canon}`);
    console.error(`  mirror:    ${copy}`);
    console.error(`  fix: run scripts/sync-${m.id}-openapi.* or copy canonical -> mirror`);
    failed = true;
  } else {
    console.log(`OK sync: ${m.id}`);
  }
}

if (failed) {
  process.exit(1);
}
