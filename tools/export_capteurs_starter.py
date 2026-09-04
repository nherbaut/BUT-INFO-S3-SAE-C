#!/usr/bin/env python3
"""Build the distributable student archive of the capteurs project."""

import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SOLUTION_PROJECT = ROOT / "projet" / "capteurs-corrige"
STUDENT_SUBJECT = ROOT / "projet" / "capteurs-starter" / "SUJET.md"
OUTPUT = ROOT / "dist" / "capteurs-starter.tar.gz"
STUDENT_DEFINE = "STUDENT_VERSION"
INCLUDE_DIRECTIVE = re.compile(r"^(\s*#\s*include\s+[^\n]+)$", re.MULTILINE)
STUDENT_TARBALL_TARGET = re.compile(
    r"\nstudent-tarball:\n\tpython3 ../../tools/export_capteurs_starter\.py\n",
    re.MULTILINE,
)


def student_source(source_path):
    source = source_path.read_text(encoding="utf-8")
    includes = []

    def protect_include(match):
        marker = f"SAE_C_INCLUDE_DIRECTIVE_{len(includes)}"
        includes.append(match.group(1))
        return marker

    protected = INCLUDE_DIRECTIVE.sub(protect_include, source)
    result = subprocess.run(
        ["cc", "-E", "-P", "-CC", "-undef", "-nostdinc", f"-D{STUDENT_DEFINE}", "-x", "c", "-"],
        check=True,
        input=protected,
        capture_output=True,
        encoding="utf-8",
    )
    output = result.stdout
    for index, include in enumerate(includes):
        output = output.replace(f"SAE_C_INCLUDE_DIRECTIVE_{index}", include)
    return output


def prepare_student_makefile(makefile_path):
    source = makefile_path.read_text(encoding="utf-8")
    source = source.replace(" student-tarball", "")
    source = STUDENT_TARBALL_TARGET.sub("\n", source)
    makefile_path.write_text(source, encoding="utf-8")


def main():
    if not SOLUTION_PROJECT.is_dir():
        raise FileNotFoundError(
            f"Correction privee absente : {SOLUTION_PROJECT}. "
            "Creez-la localement avant de generer l'archive etudiante."
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="capteurs-starter-") as temporary:
        archive_root = Path(temporary) / "capteurs-starter"
        shutil.copytree(
            SOLUTION_PROJECT,
            archive_root,
            ignore=shutil.ignore_patterns("build", "dist", "__pycache__"),
        )
        teacher_readme = archive_root / "README.md"
        if teacher_readme.exists():
            teacher_readme.unlink()
        shutil.copy2(STUDENT_SUBJECT, archive_root / "SUJET.md")
        prepare_student_makefile(archive_root / "Makefile")
        for source_path in (archive_root / "src").glob("*.c"):
            source_path.write_text(student_source(source_path), encoding="utf-8")
        with tarfile.open(OUTPUT, "w:gz") as archive:
            archive.add(archive_root, arcname="capteurs-starter")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
