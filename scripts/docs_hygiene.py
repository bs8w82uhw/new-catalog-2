#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "knowledge-registry.json"
REPORT = ROOT / "docs-hygiene-report.md"


def main() -> int:
    today = date.today().isoformat()
    docs = sorted([str(p.relative_to(ROOT)) for p in ROOT.glob("*.md")])
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    items = {x["path"]: x for x in data.get("items", [])}

    missing = [p for p in docs if p not in items]
    orphan = [p for p in items if p not in docs]
    invalid = []
    expired = []

    for path in docs:
        item = items.get(path)
        if not item:
            continue
        probs = []
        if not item.get("owner"):
            probs.append("missing owner")
        if item.get("status") not in {"draft", "active", "deprecated"}:
            probs.append("invalid status")
        if item.get("risk_level") not in {"low", "medium", "high"}:
            probs.append("invalid risk_level")
        if not isinstance(item.get("agent_ready"), bool):
            probs.append("agent_ready must be boolean")
        if probs:
            invalid.append((path, probs))
        nra = item.get("next_review_at", "")
        if isinstance(nra, str) and len(nra) == 10 and nra < today:
            expired.append((path, nra))

    lines = [
        "# Docs Hygiene Report",
        "",
        f"- Generated at: {today}",
        f"- Docs scanned: {len(docs)}",
        "",
        "## Summary",
        "",
        f"- Missing registry entries: {len(missing)}",
        f"- Orphan registry entries: {len(orphan)}",
        f"- Invalid metadata entries: {len(invalid)}",
        f"- Expired review dates: {len(expired)}",
        "",
    ]

    if missing:
        lines += ["## Missing Registry Entries", ""]
        lines += [f"- {x}" for x in missing]
        lines += [""]
    if orphan:
        lines += ["## Orphan Registry Entries", ""]
        lines += [f"- {x}" for x in orphan]
        lines += [""]
    if invalid:
        lines += ["## Invalid Metadata", ""]
        lines += [f"- {p}: {', '.join(probs)}" for p, probs in invalid]
        lines += [""]
    if expired:
        lines += ["## Expired Reviews", ""]
        lines += [f"- {p} (next_review_at: {d})" for p, d in expired]
        lines += [""]

    if not any([missing, orphan, invalid, expired]):
        lines += ["## Result", "", "- All checks passed.", ""]

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {REPORT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
