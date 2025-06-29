#!/usr/bin/env python3
"""Simple setup validation for Dear Diary backend.

Checks that OPENROUTER_API_KEY and Spotify credentials are defined in
the `.env` file.
"""
from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"

missing = []

if not ENV_PATH.exists():
    missing.append(f"Missing {ENV_PATH}")
else:
    env_vars = {}
    for line in ENV_PATH.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip()
    if not env_vars.get("OPENROUTER_API_KEY"):
        missing.append("OPENROUTER_API_KEY not set in .env")
    if not env_vars.get("SPOTIFY_CLIENT_ID") or not env_vars.get("SPOTIFY_CLIENT_SECRET"):
        missing.append("SPOTIFY_CLIENT_ID/SPOTIFY_CLIENT_SECRET not set in .env")

if missing:
    for m in missing:
        print(m, file=sys.stderr)
    sys.exit(1)

print("Environment looks good!")
