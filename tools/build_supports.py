#!/usr/bin/env python3
import html
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "cours"
BUILD = ROOT / "build" / "supports"
PLAYER_SRC = ROOT / "web" / "player"
PLAYER_DST = BUILD / "player"
VENDOR_SRC = ROOT / "web" / "vendor"
VENDOR_DST = BUILD / "vendor"
LAYOUT_SRC = ROOT / "web" / "layout"
TSCC_RUNTIME = PLAYER_DST / "tscc" / "tscc-runtime.js"
DIRECTIVE = re.compile(r"^\{\{\s*(c_demo|c_exercise)\s*:\s*([^}]+?)\s*\}\}\s*$")


def read_text(path):
    return path.read_text(encoding="utf-8")


def load_exercise(path_text):
    exercise_dir = (ROOT / path_text.strip()).resolve()
    meta_path = exercise_dir / "exercise.json"
    meta = json.loads(read_text(meta_path))
    files = []
    for source in meta["sources"]:
        source_path = exercise_dir / source
        files.append({"name": source, "content": read_text(source_path)})
    meta["path"] = str(exercise_dir.relative_to(ROOT))
    meta["files"] = files
    return meta


def render_html_player(kind, path_text):
    exercise = load_exercise(path_text)
    readonly = "true" if kind == "c_demo" else "false"
    payload = html.escape(json.dumps(exercise, ensure_ascii=False), quote=True)
    first_file = exercise["files"][0]
    code = html.escape(first_file["content"])
    title = html.escape(exercise["title"])
    local_path = html.escape(exercise["path"])
    command = html.escape(exercise["local"]["run"])
    label = "Demonstration executable" if kind == "c_demo" else "Exercice interactif"
    return f"""
<section class="embedded-exercise card my-4">
<div class="card-body">
<h3 class="card-title h5">{label} - {title}</h3>
<p class="exercise-local card-text text-body-secondary">Version locale : <code>cd {local_path}</code>, puis <code>{command}</code>.</p>
<pre><code class="language-c">{code}</code></pre>
<c-player data-readonly="{readonly}" data-exercise="{payload}"></c-player>
</div>
</section>
"""


def render_pdf_block(kind, path_text):
    exercise = load_exercise(path_text)
    label = "Demonstration" if kind == "c_demo" else "Exercice"
    blocks = [f"### {label} - {exercise['title']}", ""]
    blocks.append(exercise.get("statement", ""))
    blocks.append("")
    for file in exercise["files"]:
        blocks.append(f"#### `{file['name']}`")
        blocks.append("")
        blocks.append("```c")
        blocks.append(file["content"].rstrip())
        blocks.append("```")
        blocks.append("")
    blocks.append("Commandes locales :")
    blocks.append("")
    blocks.append("```bash")
    blocks.append(f"cd {exercise['path']}")
    blocks.append(exercise["local"]["build"])
    blocks.append(exercise["local"]["run"])
    blocks.append(exercise["local"]["test"])
    blocks.append("```")
    blocks.append("")
    if exercise.get("stdin"):
        blocks.append("Entree standard proposee :")
        blocks.append("")
        blocks.append("```text")
        blocks.append(exercise["stdin"].rstrip())
        blocks.append("```")
        blocks.append("")
    if exercise.get("expected_stdout"):
        blocks.append("Sortie attendue :")
        blocks.append("")
        blocks.append("```text")
        blocks.append(exercise["expected_stdout"].rstrip())
        blocks.append("```")
        blocks.append("")
    return "\n".join(blocks)


def expand_markdown(source, html_mode):
    output = []
    for line in source.splitlines():
        match = DIRECTIVE.match(line)
        if match:
            kind = match.group(1)
            path_text = match.group(2)
            if html_mode:
                output.append(render_html_player(kind, path_text))
            else:
                output.append(render_pdf_block(kind, path_text))
        else:
            output.append(line)
    return "\n".join(output) + "\n"


def run_pandoc(markdown, output_path, html_mode):
    tmp = output_path.with_suffix(".tmp.md")
    tmp.write_text(markdown, encoding="utf-8")
    if html_mode:
        command = [
            "pandoc",
            "-s",
            str(tmp),
            "--css",
            "vendor/bootstrap/bootstrap.min.css",
            "--css",
            "player/c-player.css",
            "--include-before-body",
            str(LAYOUT_SRC / "before-body.html"),
            "--include-after-body",
            str(LAYOUT_SRC / "after-body.html"),
        ]
        if TSCC_RUNTIME.exists():
            command.extend(["--include-after-body", str(TSCC_RUNTIME)])
        command.extend(
            [
                "--include-after-body",
                str(PLAYER_DST / "c-player.js"),
                "-o",
                str(output_path),
            ]
        )
        subprocess.run(command, check=True, cwd=BUILD)
    else:
        subprocess.run(["pandoc", str(tmp), "-o", str(output_path)], check=True)
    tmp.unlink()


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    if PLAYER_DST.exists():
        shutil.rmtree(PLAYER_DST)
    shutil.copytree(PLAYER_SRC, PLAYER_DST)
    if VENDOR_DST.exists():
        shutil.rmtree(VENDOR_DST)
    shutil.copytree(VENDOR_SRC, VENDOR_DST)

    for course in sorted(COURSES.glob("*.md")):
        source = read_text(course)
        base = course.stem
        run_pandoc(expand_markdown(source, html_mode=True), BUILD / f"{base}.html", True)
        run_pandoc(expand_markdown(source, html_mode=False), BUILD / f"{base}.pdf", False)


if __name__ == "__main__":
    main()
