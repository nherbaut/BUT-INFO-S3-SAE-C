#!/usr/bin/env python3
"""Build the distributable student archive of the capteurs project."""

import shutil
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projet" / "capteurs-starter"
OUTPUT = ROOT / "dist" / "capteurs-starter.tar.gz"


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="capteurs-starter-") as temporary:
        archive_root = Path(temporary) / "capteurs-starter"
        shutil.copytree(
            PROJECT,
            archive_root,
            ignore=shutil.ignore_patterns("build", "dist", "__pycache__"),
        )
        with tarfile.open(OUTPUT, "w:gz") as archive:
            archive.add(archive_root, arcname="capteurs-starter")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
