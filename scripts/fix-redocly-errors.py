#!/usr/bin/env python3
"""Fix Redocly errors (not warnings) in OpenAPI 3.1 specs under api-contracts/."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
RESPONSE_LINE = re.compile(r"^(\s+)'(\d{3})':\s*$")
OPERATION_ID = re.compile(r"^(\s+)operationId:\s+(\S+)\s*$")
TYPE_LINE = re.compile(r"^(\s+)type:\s+(.+)\s*$")


def default_response_description(code: str) -> str:
    if code == "204":
        return "No content"
    if code.startswith("2"):
        return "OK"
    if code.startswith("4"):
        return "Client error"
    if code.startswith("5"):
        return "Server error"
    return "Response"


def operation_id_to_summary(operation_id: str) -> str:
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", operation_id)
    words = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", words)
    return words[:1].upper() + words[1:] if words else "Operation"


def fix_nullable(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "nullable: true":
            j = len(out) - 1
            type_idx = None
            type_indent = ""
            type_val = ""
            while j >= 0:
                prev = out[j]
                m = TYPE_LINE.match(prev)
                if m:
                    type_idx = j
                    type_indent, type_val = m.group(1), m.group(2).strip()
                    break
                if prev.strip() and not prev.strip().startswith("#"):
                    break
                j -= 1
            if type_idx is not None and not type_val.startswith("["):
                out[type_idx] = f"{type_indent}type: [{type_val}, 'null']\n"
            elif type_idx is not None and type_val.startswith("[") and "'null'" not in type_val:
                inner = type_val.rstrip("]")
                out[type_idx] = f"{type_indent}type: {inner}, 'null']\n"
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def fix_response_descriptions(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = RESPONSE_LINE.match(line)
        if m:
            indent, code = m.group(1), m.group(2)
            out.append(line)
            i += 1
            if i < len(lines):
                stripped = lines[i].strip()
                if stripped.startswith("content:"):
                    out.append(f"{indent}  description: {default_response_description(code)}\n")
                elif stripped.startswith("$ref:"):
                    pass
        else:
            out.append(line)
            i += 1
    return out


GENERIC_DESCRIPTIONS = {"OK", "Client error", "Server error", "No content", "Response"}


def remove_spurious_response_descriptions(lines: list[str]) -> list[str]:
    """Drop generic descriptions immediately before a $ref response."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (
            i + 1 < len(lines)
            and line.strip().startswith("description:")
            and lines[i + 1].strip().startswith("$ref:")
        ):
            desc = line.split(":", 1)[1].strip()
            if desc in GENERIC_DESCRIPTIONS:
                i += 1
                continue
        out.append(line)
        i += 1
    return out


def dedupe_operation_summaries(lines: list[str]) -> list[str]:
    """Keep one summary per operation (prefer existing Russian text)."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("operationId:"):
            pre: list[str] = []
            while out and out[-1].strip().startswith("summary:"):
                pre.insert(0, out.pop())
            op_line = line
            i += 1
            post: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("summary:"):
                post.append(lines[i])
                i += 1
            all_summaries = pre + post
            if len(all_summaries) > 1:
                cyrillic = [s for s in all_summaries if re.search(r"[а-яА-ЯёЁ]", s)]
                keep = cyrillic[0] if cyrillic else max(all_summaries, key=len)
                out.append(keep)
            elif all_summaries:
                out.extend(all_summaries)
            out.append(op_line)
            continue
        out.append(line)
        i += 1
    return out


def fix_operation_summaries(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    in_paths = False
    op_depth = None
    has_summary = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "paths:":
            in_paths = True
            out.append(line)
            i += 1
            continue

        if in_paths and stripped.startswith("components:"):
            in_paths = False
            op_depth = None

        if in_paths:
            indent = len(line) - len(line.lstrip())
            if stripped.endswith(":") and not stripped.startswith("/") and stripped.rstrip(":") in HTTP_METHODS:
                op_depth = indent
                has_summary = False
                out.append(line)
                i += 1
                continue

            if op_depth is not None and indent <= op_depth and stripped and not stripped.startswith("#"):
                if stripped.startswith("/") or (stripped.endswith(":") and stripped.rstrip(":") in HTTP_METHODS):
                    op_depth = None if not (
                        stripped.endswith(":") and stripped.rstrip(":") in HTTP_METHODS
                    ) else indent
                    if stripped.endswith(":") and stripped.rstrip(":") in HTTP_METHODS:
                        op_depth = indent
                        has_summary = False

            if op_depth is not None and indent > op_depth:
                if stripped.startswith("summary:"):
                    has_summary = True
                m = OPERATION_ID.match(line)
                if m and not has_summary:
                    out.append(f"{m.group(1)}summary: {operation_id_to_summary(m.group(2))}\n")
                    has_summary = True
                out.append(line)
                i += 1
                continue

        out.append(line)
        i += 1

    return out


def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    lines = fix_nullable(lines)
    lines = fix_response_descriptions(lines)
    lines = fix_operation_summaries(lines)
    lines = remove_spurious_response_descriptions(lines)
    lines = dedupe_operation_summaries(lines)
    updated = "".join(lines)
    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.glob("*/openapi.yaml")):
        if fix_file(path):
            changed.append(path.relative_to(ROOT))
    if changed:
        print("Updated:", ", ".join(str(p) for p in changed))
    else:
        print("No changes.")


if __name__ == "__main__":
    main()
