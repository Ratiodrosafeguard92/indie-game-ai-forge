"""Stable content hashing so re-runs can skip unchanged output."""
from __future__ import annotations

import hashlib
from pathlib import Path


def hash_text(text: str) -> str:
    return hashlib.blake2b(text.encode("utf-8"), digest_size=12).hexdigest()


def hash_file(path: Path) -> str:
    return hashlib.blake2b(path.read_bytes(), digest_size=12).hexdigest()