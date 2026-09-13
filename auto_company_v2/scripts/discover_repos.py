#!/usr/bin/env python3
"""Inspect locally cloned Shtenco repos and report probable integration surfaces.
No network access and no code execution are performed.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

MARKERS = {
    "python": ["pyproject.toml", "requirements.txt", "setup.py"],
    "node": ["package.json"],
    "docker": ["Dockerfile", "docker-compose.yml", "compose.yaml"],
    "mcp": ["mcp.json", ".mcp.json"],
    "api": ["openapi.json", "openapi.yaml", "openapi.yml"],
}


def inspect(root: Path) -> dict:
    found = {}
    names = {p.name for p in root.iterdir()} if root.is_dir() else set()
    for k, markers in MARKERS.items():
        found[k] = [m for m in markers if m in names]
    return {"name": root.name, "path": str(root), "surfaces": found}

base = Path(sys.argv[1] if len(sys.argv) > 1 else "../")
rows = [inspect(p) for p in sorted(base.iterdir()) if p.is_dir() and (p / ".git").exists()]
print(json.dumps(rows, ensure_ascii=False, indent=2))
