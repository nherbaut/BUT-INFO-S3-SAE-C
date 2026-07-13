#!/usr/bin/env python3
from pathlib import Path
import sys
import re


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "web" / "player" / "tscc"

required = [
    RUNTIME / "tscc-runtime.js",
    RUNTIME / "tscc-bundle.js",
    RUNTIME / "ORIGIN.md",
]

missing = [path for path in required if not path.exists()]

errors = []
if missing:
    errors.append("Fichiers manquants: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))

runtime_js = RUNTIME / "tscc-runtime.js"
if runtime_js.exists():
    runtime_text = runtime_js.read_text(encoding="utf-8")
    for src in re.findall(r'<script\s+src="player/tscc/([^"]+)"', runtime_text):
        dependency = RUNTIME / src
        if not dependency.exists():
            errors.append(f"Dependance JS referencee absente: web/player/tscc/{src}")

bundle_js = RUNTIME / "tscc-bundle.js"
if bundle_js.exists():
    bundle_text = bundle_js.read_text(encoding="utf-8", errors="ignore")
    if "CCompilerRuntime" not in bundle_text:
        errors.append("web/player/tscc/tscc-bundle.js ne declare pas CCompilerRuntime")

if errors:
    print("Runtime navigateur ts-c-compiler non installe.")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Runtime navigateur ts-c-compiler installe:")
for path in required:
    print(f"- {path.relative_to(ROOT)}")
