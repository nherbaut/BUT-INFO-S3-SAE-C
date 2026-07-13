#!/usr/bin/env python3
import html
import json
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "cours"
EXERCISES = ROOT / "exercices"
BUILD = ROOT / "build" / "supports"
PLAYER_SRC = ROOT / "web" / "player"
PLAYER_DST = BUILD / "player"
VENDOR_SRC = ROOT / "web" / "vendor"
VENDOR_DST = BUILD / "vendor"
PDF_DST = BUILD / "assets" / "pdf"
TSCC_RUNTIME = PLAYER_DST / "tscc" / "tscc-runtime.js"
PUBLIC_REPO = "https://github.com/nherbaut/BUT-INFO-S3-SAE-C"
COURSE_INDEX = "index-cours.html"
FULL_PDF = "assets/pdf/but-info-s3-sae-c.pdf"
DIRECTIVE = re.compile(r"^\{\{\s*(c_demo|c_exercise)\s*:\s*([^}]+?)\s*\}\}\s*$")
BODY_RE = re.compile(r"<body[^>]*>(?P<body>.*)</body>", re.S)
HEAD_RE = re.compile(r"<h([12]) id=\"([^\"]+)\">(.*?)</h\1>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
TITLE_BLOCK_RE = re.compile(r"<header id=\"title-block-header\">.*?</header>", re.S)


def read_text(path):
    return path.read_text(encoding="utf-8")


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def strip_tags(value):
    return html.unescape(TAG_RE.sub("", value)).strip()


def course_infos():
    infos = []
    for course in sorted(COURSES.glob("*.md")):
        source = read_text(course)
        title_match = re.search(r"^#\s+(.+)$", source, re.M)
        title = title_match.group(1) if title_match else course.stem
        infos.append(
            {
                "path": course,
                "title": title,
                "stem": course.stem,
                "html": f"{course.stem}.html",
                "pdf": f"assets/pdf/{course.stem}.pdf",
            }
        )
    return infos


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


def all_exercises():
    exercises = []
    for meta_path in sorted(EXERCISES.glob("seance-*/*/exercise.json")):
        exercises.append(load_exercise(str(meta_path.parent.relative_to(ROOT))))
    return exercises


def render_html_player(kind, path_text):
    exercise = load_exercise(path_text)
    readonly = "true" if kind == "c_demo" else "false"
    payload = html.escape(json.dumps(exercise, ensure_ascii=False), quote=True)
    first_file = exercise["files"][0]
    code = html.escape(first_file["content"])
    title = html.escape(exercise["title"])
    statement = html.escape(exercise.get("statement", ""))
    local_path = html.escape(exercise["path"])
    command = html.escape(exercise["local"]["run"])
    label = "Demonstration executable" if kind == "c_demo" else "Exercice interactif"
    return f"""
<details class="embedded-exercise card my-4">
<summary class="card-header h5">{label} - {title}</summary>
<div class="card-body">
<p class="card-text">{statement}</p>
<p class="exercise-local card-text text-body-secondary">Version locale : <code>cd {local_path}</code>, puis <code>{command}</code>.</p>
<pre><code class="language-c">{code}</code></pre>
<c-player data-readonly="{readonly}" data-exercise="{payload}"></c-player>
</div>
</details>
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
            output.append(render_html_player(kind, path_text) if html_mode else render_pdf_block(kind, path_text))
        else:
            output.append(line)
    return "\n".join(output) + "\n"


def run_pandoc(markdown, output_path, html_mode, title=None):
    tmp = output_path.with_suffix(".tmp.md")
    write_text(tmp, markdown)
    if html_mode:
        command = [
            "pandoc",
            "-s",
            str(tmp),
            "--metadata",
            f"title={title or output_path.stem}",
            "--css",
            "vendor/bootstrap/bootstrap.min.css",
            "--css",
            "player/c-player.css",
        ]
        if TSCC_RUNTIME.exists():
            command.extend(["--include-after-body", str(TSCC_RUNTIME)])
        command.extend(["--include-after-body", str(PLAYER_DST / "c-player.js"), "-o", str(output_path)])
        subprocess.run(command, check=True, cwd=BUILD)
    else:
        subprocess.run(["pandoc", str(tmp), "-o", str(output_path)], check=True)
    tmp.unlink()


def extract_body(document):
    match = BODY_RE.search(document)
    if not match:
        return document
    return match.group("body").strip()


def replace_body(document, body):
    return BODY_RE.sub(f"<body>\n{body}\n</body>", document)


def page_headings(body):
    headings = []
    for level, heading_id, content in HEAD_RE.findall(body):
        headings.append({"level": int(level), "id": heading_id, "title": strip_tags(content)})
    return headings


def main_nav(active):
    items = [
        ("index.html", "Accueil", active == "home"),
        (COURSE_INDEX, "Cours", active == "course"),
        ("exercices.html", "Exercices", active == "exercises"),
        (FULL_PDF, "PDF", False),
        (PUBLIC_REPO, "Depot", False),
    ]
    links = []
    for href, label, is_active in items:
        active_class = " active" if is_active else ""
        aria = ' aria-current="page"' if is_active else ""
        links.append(f'<li class="nav-item"><a class="nav-link{active_class}"{aria} href="{href}">{label}</a></li>')
    return f"""
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
  <div class="container-fluid">
    <a class="navbar-brand" href="index.html">BUT INFO S3 SAE-C</a>
    <div class="navbar-nav-scroll">
      <ul class="navbar-nav flex-row gap-3">
        {''.join(links)}
      </ul>
    </div>
  </div>
</nav>
"""


def left_sidebar(courses, current):
    links = []
    for course in courses:
        active = " active" if course["html"] == current else ""
        links.append(
            f'<li class="nav-item"><a class="nav-link{active}" href="{course["html"]}">{html.escape(course["title"])}</a></li>'
        )
    return f"""
<aside class="course-sidebar-left col-lg-2">
  <nav class="position-sticky pt-3">
    <div class="fw-semibold text-uppercase small text-body-secondary mb-2">Seances</div>
    <ul class="nav nav-pills flex-column">
      {''.join(links)}
    </ul>
  </nav>
</aside>
"""


def right_sidebar(headings):
    links = []
    for heading in headings:
        indent = " ps-3" if heading["level"] == 2 else ""
        links.append(
            f'<li class="nav-item"><a class="nav-link py-1{indent}" href="#{heading["id"]}">{html.escape(heading["title"])}</a></li>'
        )
    return f"""
<aside class="course-sidebar-right col-lg-2">
  <nav class="position-sticky pt-3">
    <div class="fw-semibold text-uppercase small text-body-secondary mb-2">Dans cette page</div>
    <ul class="nav nav-pills flex-column small">
      {''.join(links)}
    </ul>
  </nav>
</aside>
"""


def doc_layout(body, courses, current, active, pdf_href=None):
    headings = page_headings(body)
    pdf_link = ""
    if pdf_href:
        pdf_link = f'<p><a class="btn btn-outline-secondary btn-sm" href="{pdf_href}" download>Telecharger le PDF de cette page</a></p>'
    return f"""
{main_nav(active)}
<div class="container-fluid">
  <div class="row">
    {left_sidebar(courses, current)}
    <main class="course-content col-lg-8 py-4">
      {pdf_link}
      {body}
    </main>
    {right_sidebar(headings)}
  </div>
</div>
"""


def postprocess_doc_page(output_path, courses, current, active, pdf_href=None):
    document = read_text(output_path)
    body = TITLE_BLOCK_RE.sub("", extract_body(document)).strip()
    write_text(output_path, replace_body(document, doc_layout(body, courses, current, active, pdf_href)))


def landing_page():
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BUT INFO S3 SAE-C</title>
  <link rel="stylesheet" href="vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="player/c-player.css">
</head>
<body class="landing-page">
{main_nav("home")}
<main class="landing-hero">
  <section class="container py-5">
    <div class="row align-items-center min-vh-75">
      <div class="col-lg-9">
        <p class="text-uppercase text-body-secondary fw-semibold">Programmation C</p>
        <h1 class="display-3 fw-bold">BUT INFO S3 SAE-C</h1>
        <p class="lead mt-3">Supports HTML interactifs, exercices executables dans le navigateur et PDF de cours.</p>
        <div class="d-flex flex-wrap gap-3 mt-4">
          <a class="btn btn-primary btn-lg" href="{PUBLIC_REPO}">Cloner le depot</a>
          <a class="btn btn-primary btn-lg" href="{COURSE_INDEX}">Documentation en ligne</a>
          <a class="btn btn-secondary btn-lg" href="{FULL_PDF}" download>Telecharger le PDF</a>
        </div>
      </div>
    </div>
  </section>
</main>
</body>
</html>
"""


def course_index_markdown(courses):
    lines = ["# Documentation en ligne", ""]
    lines.append("Supports de cours et exercices interactifs pour BUT INFO S3 SAE-C.")
    lines.append("")
    for course in courses:
        lines.append(f"- [{course['title']}]({course['html']})")
    lines.append("")
    lines.append(f"[Telecharger le PDF complet]({FULL_PDF})")
    return "\n".join(lines) + "\n"


def exercises_markdown():
    lines = ["# Exercices", ""]
    lines.append("Tous les exercices interactifs du support.")
    lines.append("")
    for exercise in all_exercises():
        rel_path = exercise["path"]
        lines.append(f"## {exercise['title']}")
        lines.append("")
        lines.append(f"{{{{ c_exercise: {rel_path} }}}}")
        lines.append("")
    return "\n".join(lines)


def build_full_pdf(courses):
    blocks = ["# BUT INFO S3 SAE-C", ""]
    for course in courses:
        blocks.append(expand_markdown(read_text(course["path"]), html_mode=False))
        blocks.append("\\newpage")
        blocks.append("")
    run_pandoc("\n".join(blocks), BUILD / FULL_PDF, html_mode=False)


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    PDF_DST.mkdir(parents=True, exist_ok=True)
    if PLAYER_DST.exists():
        shutil.rmtree(PLAYER_DST)
    shutil.copytree(PLAYER_SRC, PLAYER_DST)
    if VENDOR_DST.exists():
        shutil.rmtree(VENDOR_DST)
    shutil.copytree(VENDOR_SRC, VENDOR_DST)

    courses = course_infos()
    write_text(BUILD / "index.html", landing_page())

    run_pandoc(course_index_markdown(courses), BUILD / COURSE_INDEX, True, "Documentation en ligne")
    postprocess_doc_page(BUILD / COURSE_INDEX, courses, COURSE_INDEX, "course", FULL_PDF)

    run_pandoc(expand_markdown(exercises_markdown(), html_mode=True), BUILD / "exercices.html", True, "Exercices")
    postprocess_doc_page(BUILD / "exercices.html", courses, "exercices.html", "exercises", None)

    for course in courses:
        source = read_text(course["path"])
        run_pandoc(expand_markdown(source, html_mode=True), BUILD / course["html"], True, course["title"])
        postprocess_doc_page(BUILD / course["html"], courses, course["html"], "course", course["pdf"])
        run_pandoc(expand_markdown(source, html_mode=False), BUILD / course["pdf"], False)

    build_full_pdf(courses)


if __name__ == "__main__":
    main()
