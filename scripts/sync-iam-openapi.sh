#!/usr/bin/env bash
# Копирует канон IAM OpenAPI в iam-service (ADR-001).
exec "$(dirname "$0")/sync-openapi-mirror.sh" iam
