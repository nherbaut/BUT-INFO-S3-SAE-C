#!/usr/bin/env python3
import html
import json
import re
import shutil
import subprocess
import base64
import zipfile
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
ZIP_DST = BUILD / "assets" / "zip"
PDF_FOOTER_TEX = BUILD / "pdf-footer.tex"
TSCC_RUNTIME = PLAYER_DST / "tscc" / "tscc-runtime.js"
PUBLIC_REPO = "https://github.com/nherbaut/BUT-INFO-S3-SAE-C"
CREDITS = "Crédits : Nicolas Herbaut, Romain Giot et Pierre Ramet"
COURSE_INDEX = "index-cours.html"
FULL_PDF = "assets/pdf/but-info-s3-sae-c.pdf"
FULL_ZIP = "assets/zip/but-info-s3-sae-c-starters.zip"
QUIZ_INDEX = "quiz.html"
QUIZ_PDF = "assets/pdf/but-info-s3-sae-c-quiz.pdf"
ADMIN_PAGE = "admin.html"
LIVE_CODE_PAGE = "live-code.html"
LIVE_QUIZ_PAGE = "live-quiz.html"
ADMIN_DIGEST = "$argon2id$v=19$m=65536,t=3,p=4$SDaf4HTJfRAO2wys9QIE7A$bLo2gTmVGol0ogx6vLCsYGPNZbIcqUNWS88ZuJZCgIo"
DIRECTIVE = re.compile(r"^\{\{\s*(c_demo|c_exercise)\s*:\s*([^}]+?)\s*\}\}\s*$")
CODE_FENCE_C = re.compile(r"^```\s*c\s*$", re.I)
CODE_FENCE_END = re.compile(r"^```\s*$")
QUIZ_START = re.compile(r"^:::\s+quiz(?:\s+\{#([A-Za-z0-9_-]+)\})?\s*$")
QUESTION_START = re.compile(r"^:::\s+question(?:\s+\{#([A-Za-z0-9_-]+)\})?\s*$")
DIV_END = re.compile(r"^:::\s*$")
OPTION_RE = re.compile(r"^\s*-\s+\[([ xX])\]\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^([A-Za-z_-]+):\s*(.*)$")
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


def site_footer():
    return f"""
<footer class="site-footer border-top">
  <div class="container-fluid py-3">
    <span>{html.escape(CREDITS)}</span>
  </div>
</footer>
"""


def write_pdf_footer():
    write_text(
        PDF_FOOTER_TEX,
        r"""
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\footnotesize Cr\'edits : Nicolas Herbaut, Romain Giot et Pierre Ramet}
\fancyfoot[R]{\footnotesize \thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.2pt}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyfoot[C]{\footnotesize Cr\'edits : Nicolas Herbaut, Romain Giot et Pierre Ramet}
  \fancyfoot[R]{\footnotesize \thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0.2pt}
}
""".lstrip(),
    )


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
    meta["browser_runnable"] = len(files) == 1
    return meta


def all_exercises():
    exercises = []
    for meta_path in sorted(EXERCISES.glob("seance-*/*/exercise.json")):
        exercises.append(load_exercise(str(meta_path.parent.relative_to(ROOT))))
    return exercises


def collect_div_block(lines, start_index):
    block = [lines[start_index]]
    depth = 1
    index = start_index + 1
    while index < len(lines):
        line = lines[index]
        if QUIZ_START.match(line) or QUESTION_START.match(line):
            depth += 1
        elif DIV_END.match(line):
            depth -= 1
        block.append(line)
        index += 1
        if depth == 0:
            return block, index
    raise ValueError("Bloc quiz non ferme")


def parse_quiz(block, fallback_id):
    start = QUIZ_START.match(block[0])
    quiz_id = start.group(1) if start and start.group(1) else fallback_id
    quiz = {"id": quiz_id, "title": quiz_id, "questions": []}
    index = 1
    while index < len(block) - 1:
        line = block[index]
        question_start = QUESTION_START.match(line)
        if question_start:
            question_block, new_index = collect_div_block(block, index)
            quiz["questions"].append(parse_question(question_block, f"{quiz_id}-q{len(quiz['questions']) + 1}"))
            index = new_index
            continue
        field = FIELD_RE.match(line)
        if field:
            key = field.group(1).strip().lower()
            if key in {"title", "description"}:
                quiz[key] = field.group(2).strip()
        index += 1
    if not quiz["questions"]:
        raise ValueError(f"Quiz {quiz_id} sans question")
    return quiz


def parse_question(block, fallback_id):
    start = QUESTION_START.match(block[0])
    question_id = start.group(1) if start and start.group(1) else fallback_id
    question = {"id": question_id, "title": question_id, "description": "", "options": []}
    current_option = None
    for line in block[1:-1]:
        option = OPTION_RE.match(line)
        if option:
            current_option = {
                "id": f"{question_id}-o{len(question['options']) + 1}",
                "text": option.group(2).strip(),
                "correct": option.group(1).lower() == "x",
                "hint": "",
            }
            question["options"].append(current_option)
            continue
        field = FIELD_RE.match(line.strip())
        if field:
            key = field.group(1).strip().lower()
            value = field.group(2).strip()
            if current_option and key == "hint":
                current_option["hint"] = value
            elif key in {"title", "description"}:
                question[key] = value
    if not question["options"]:
        raise ValueError(f"Question {question_id} sans option")
    if not any(option["correct"] for option in question["options"]):
        raise ValueError(f"Question {question_id} sans bonne reponse")
    return question


def quizzes_from_source(source, course):
    lines = source.splitlines()
    quizzes = []
    index = 0
    while index < len(lines):
        if QUIZ_START.match(lines[index]):
            block, index = collect_div_block(lines, index)
            quiz = parse_quiz(block, f"{course['stem']}-quiz-{len(quizzes) + 1}")
            quiz["course_title"] = course["title"]
            quiz["course_html"] = course["html"]
            quiz["course_stem"] = course["stem"]
            quizzes.append(quiz)
        else:
            index += 1
    return quizzes


def all_quizzes(courses):
    quizzes = []
    for course in courses:
        quizzes.extend(quizzes_from_source(read_text(course["path"]), course))
    return quizzes


def live_question_bank(courses):
    questions = []
    for quiz in all_quizzes(courses):
        for question in quiz["questions"]:
            questions.append(
                {
                    "id": f'{quiz["course_stem"]}:{quiz["id"]}:{question["id"]}',
                    "label": f'{quiz["course_title"]} - {quiz["title"]} - {question["title"]}',
                    "course_title": quiz["course_title"],
                    "quiz_title": quiz["title"],
                    "question": question,
                }
            )
    return questions


def admin_flow_items(course, source, raw_body):
    generated_headings = page_headings(raw_body)
    heading_index = 0
    items = []
    lines = source.splitlines()
    index = 0
    while index < len(lines):
        heading_match = re.match(r"^(#{1,2})\s+(.+)$", lines[index])
        if heading_match:
            level = len(heading_match.group(1))
            while heading_index < len(generated_headings) and generated_headings[heading_index]["level"] != level:
                heading_index += 1
            if heading_index < len(generated_headings):
                heading = generated_headings[heading_index]
                if heading["id"] != "ntfy-chat-group-title":
                    items.append(
                        {
                            "type": "section",
                            "course_title": course["title"],
                            "href": f'{course["html"]}#{heading["id"]}',
                            "level": heading["level"],
                            "title": heading["title"],
                        }
                    )
                heading_index += 1
        elif QUIZ_START.match(lines[index]):
            block, index = collect_div_block(lines, index)
            quiz = parse_quiz(block, f"{course['stem']}-flow-quiz-{len(items) + 1}")
            for question in quiz["questions"]:
                items.append(
                    {
                        "type": "question",
                        "id": f'{course["stem"]}:{quiz["id"]}:{question["id"]}',
                        "course_title": course["title"],
                        "quiz_title": quiz["title"],
                        "title": question["title"],
                        "question": question,
                    }
                )
            continue
        index += 1
    return items


def render_html_player(kind, path_text):
    exercise = load_exercise(path_text)
    readonly = "true" if kind == "c_demo" else "false"
    payload = base64.b64encode(json.dumps(exercise, ensure_ascii=False).encode("utf-8")).decode("ascii")
    title = html.escape(exercise["title"])
    statement = html.escape(exercise.get("statement", ""))
    local_path = html.escape(exercise["path"])
    command = html.escape(exercise["local"]["run"])
    label = "Demonstration executable" if kind == "c_demo" else "Exercice interactif"
    browser_label = "Executable dans le navigateur" if exercise["browser_runnable"] else "Local uniquement"
    browser_class = "text-bg-success" if exercise["browser_runnable"] else "text-bg-warning"
    return f"""
<details class="embedded-exercise card my-4">
<summary class="card-header h5">
  <span>{label} - {title}</span>
  <span class="badge {browser_class} ms-2">{browser_label}</span>
</summary>
<div class="card-body">
<p class="card-text">{statement}</p>
<p class="exercise-local card-text text-body-secondary">Version locale : <code>cd {local_path}</code>, puis <code>{command}</code>.</p>
<c-player data-readonly="{readonly}" data-exercise-b64="{payload}"></c-player>
</div>
</details>
"""


def encode_data(value):
    return base64.b64encode(json.dumps(value, ensure_ascii=False).encode("utf-8")).decode("ascii")


def render_html_code_example(source, index):
    runnable = "int main" in source
    payload = encode_data(
        {
            "id": f"code-example-{index}",
            "title": f"Exemple C {index}",
            "statement": "",
            "sources": ["main.c"],
            "main": "main.c",
            "stdin": "",
            "expected_stdout": "",
            "expected_stderr": "",
            "path": "",
            "files": [{"name": "main.c", "content": source}],
            "browser_runnable": runnable,
        }
    )
    return f'<c-player data-readonly="true" data-exercise-b64="{payload}"></c-player>'


def render_html_quiz(quiz, fold_validated=False):
    payload = encode_data(quiz)
    folded = ' data-fold-validated="true"' if fold_validated else ""
    return f'<quiz-player data-quiz-b64="{payload}"{folded}></quiz-player>'


def render_pdf_quiz(quiz, show_answers=True):
    blocks = [f"## {quiz['course_title']} - {quiz['title']}", ""]
    if quiz.get("description"):
        blocks.extend([quiz["description"], ""])
    for question in quiz["questions"]:
        blocks.append(f"### {question['title']}")
        blocks.append("")
        if question.get("description"):
            blocks.extend([question["description"], ""])
        for option in question["options"]:
            marker = "[x]" if option["correct"] and show_answers else "[ ]"
            blocks.append(f"- {marker} {option['text']}")
            if option.get("hint"):
                blocks.append(f"  - Indice : {option['hint']}")
        blocks.append("")
    return "\n".join(blocks)


def exercise_directives(source):
    paths = []
    for line in source.splitlines():
        match = DIRECTIVE.match(line)
        if match:
            paths.append(match.group(2).strip())
    return paths


def starter_zip_name(stem):
    return f"assets/zip/{stem}-starters.zip"


def write_starter_zip(output_path, exercises):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        common = EXERCISES / "common.mk"
        if common.exists():
            archive.write(common, common.relative_to(ROOT))
        for exercise in exercises:
            exercise_dir = ROOT / exercise["path"]
            entries = ["exercise.json", "Makefile", *exercise.get("sources", [])]
            for entry in entries:
                file_path = exercise_dir / entry
                if not file_path.exists() or not file_path.is_file():
                    continue
                arcname = str(file_path.relative_to(ROOT))
                if arcname in seen:
                    continue
                seen.add(arcname)
                archive.write(file_path, arcname)


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
    lines = source.splitlines()
    output = []
    index = 0
    quiz_count = 0
    code_example_count = 0
    while index < len(lines):
        line = lines[index]
        if html_mode and CODE_FENCE_C.match(line):
            index += 1
            code_lines = []
            while index < len(lines) and not CODE_FENCE_END.match(lines[index]):
                code_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("Bloc de code C non ferme")
            index += 1
            code_example_count += 1
            output.append(render_html_code_example("\n".join(code_lines) + "\n", code_example_count))
            continue
        if QUIZ_START.match(line):
            block, index = collect_div_block(lines, index)
            quiz_count += 1
            if html_mode:
                output.append(render_html_quiz(parse_quiz(block, f"quiz-{quiz_count}")))
            continue
        match = DIRECTIVE.match(line)
        if match:
            kind = match.group(1)
            path_text = match.group(2)
            output.append(render_html_player(kind, path_text) if html_mode else render_pdf_block(kind, path_text))
        else:
            output.append(line)
        index += 1
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
        command.extend(
            [
                "--include-after-body",
                str(PLAYER_DST / "c-player.js"),
                "--include-after-body",
                str(PLAYER_DST / "quiz-player.js"),
                "--include-after-body",
                str(PLAYER_DST / "site-theme.js"),
                "--include-after-body",
                str(PLAYER_DST / "ntfy-chat.js"),
                "-o",
                str(output_path),
            ]
        )
        subprocess.run(command, check=True, cwd=BUILD)
    else:
        command = ["pandoc", str(tmp)]
        if PDF_FOOTER_TEX.exists():
            command.extend(["--include-in-header", str(PDF_FOOTER_TEX)])
        command.extend(["-o", str(output_path)])
        subprocess.run(command, check=True)
    tmp.unlink()


def extract_body(document):
    match = BODY_RE.search(document)
    if not match:
        return document
    return match.group("body").strip()


def replace_body(document, body):
    return BODY_RE.sub(lambda _match: f"<body>\n{body}\n</body>", document)


def page_headings(body):
    headings = []
    for level, heading_id, content in HEAD_RE.findall(body):
        headings.append({"level": int(level), "id": heading_id, "title": strip_tags(content)})
    return headings


def main_nav(active, include_admin=False):
    items = [
        ("index.html", "Accueil", active == "home"),
        (COURSE_INDEX, "Cours", active == "course"),
        ("exercices.html", "Exercices", active == "exercises"),
        (QUIZ_INDEX, "Quiz", active == "quiz"),
        (FULL_PDF, "PDF", False),
        (PUBLIC_REPO, "Depot", False),
    ]
    links = []
    for href, label, is_active in items:
        active_class = " active" if is_active else ""
        aria = ' aria-current="page"' if is_active else ""
        links.append(f'<li class="nav-item"><a class="nav-link{active_class}"{aria} href="{href}">{label}</a></li>')
    if include_admin:
        active_class = " active" if active == "admin" else ""
        aria = ' aria-current="page"' if active == "admin" else ""
        links.append(f'<li class="nav-item"><a class="nav-link{active_class}"{aria} href="{ADMIN_PAGE}">Admin</a></li>')
    return f"""
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
  <div class="container-fluid">
    <a class="navbar-brand" href="index.html">BUT INFO S3 SAE-C</a>
    <div class="navbar-nav-scroll">
      <ul class="navbar-nav flex-row gap-3">
        {''.join(links)}
      </ul>
    </div>
    <button class="btn btn-outline-light btn-sm ms-auto" type="button" data-theme-toggle aria-pressed="false">Mode sombre</button>
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


def doc_layout(body, courses, current, active, pdf_href=None, zip_href=None):
    headings = page_headings(body)
    actions = []
    if pdf_href:
        actions.append(f'<a class="btn btn-outline-secondary btn-sm" href="{pdf_href}" download>Telecharger le PDF de cette page</a>')
    if zip_href:
        actions.append(f'<a class="btn btn-outline-secondary btn-sm" href="{zip_href}" download>Telecharger les starter codes</a>')
    action_block = ""
    if actions:
        action_block = f'<p class="page-actions">{"".join(actions)}</p>'
    return f"""
{main_nav(active)}
<div class="container-fluid">
  <div class="row">
    {left_sidebar(courses, current)}
    <main class="course-content col-lg-8 py-4">
      {action_block}
      {body}
    </main>
    {right_sidebar(headings)}
  </div>
</div>
{site_footer()}
"""


def postprocess_doc_page(output_path, courses, current, active, pdf_href=None, zip_href=None):
    document = read_text(output_path)
    body = TITLE_BLOCK_RE.sub("", extract_body(document)).strip()
    write_text(output_path, replace_body(document, doc_layout(body, courses, current, active, pdf_href, zip_href)))


def landing_page():
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BUT INFO S3 SAE-C</title>
  <link rel="stylesheet" href="vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="player/c-player.css">
  <script>
    document.documentElement.setAttribute("data-bs-theme", localStorage.getItem("sae-c.theme.v1") || "light");
  </script>
</head>
<body class="landing-page">
{main_nav("home")}
<main>
  <section class="landing-hero">
    <canvas class="landing-hero__canvas" id="landing-hero-canvas" aria-hidden="true"></canvas>
    <div class="container landing-hero__content">
      <p class="landing-hero__eyebrow">Programmation C pour la programmation systeme</p>
      <h1 class="landing-hero__title">BUT INFO S3 SAE-C</h1>
      <p class="landing-hero__lead">Supports de cours, exercices interactifs et PDF pour demarrer le C avant la programmation systeme.</p>
      <div class="d-flex flex-wrap gap-3 mt-4">
        <a class="btn btn-primary btn-lg" href="{COURSE_INDEX}">Ouvrir le site statique</a>
        <a class="btn btn-primary btn-lg" href="{PUBLIC_REPO}">Cloner le depot</a>
        <a class="btn btn-secondary btn-lg" href="{FULL_PDF}" download>Telecharger le PDF</a>
      </div>
    </div>
  </section>
  <section class="container landing-next py-4">
    <div class="row g-3">
      <div class="col-md-4"><a class="landing-next__item" href="{COURSE_INDEX}">Documentation en ligne</a></div>
      <div class="col-md-4"><a class="landing-next__item" href="exercices.html">Tous les exercices</a></div>
      <div class="col-md-4"><a class="landing-next__item" href="{QUIZ_INDEX}">Mini-quiz</a></div>
    </div>
  </section>
</main>
{site_footer()}
<script>
(() => {{
  const canvas = document.getElementById("landing-hero-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const snippets = [
    "int main(void) {{",
    "  printf(\\"SAE-C\\\\n\\");",
    "  return 0;",
    "}}",
    "gcc -Wall -Wextra main.c",
    "make test",
    "valgrind ./programme",
    "struct Etudiant {{ int note; }};",
    "int *p = &value;",
  ];
  let width = 0;
  let height = 0;
  const particles = Array.from({{ length: 56 }}, (_, index) => ({{
    x: Math.random(),
    y: Math.random(),
    speed: 0.12 + Math.random() * 0.28,
    text: snippets[index % snippets.length],
    color: ["#f2c94c", "#56c2a8", "#e06c5f", "#f8f9fa"][index % 4],
  }}));

  function resize() {{
    const ratio = window.devicePixelRatio || 1;
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  }}

  function draw() {{
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#10100f";
    ctx.fillRect(0, 0, width, height);
    ctx.globalAlpha = 0.18;
    ctx.strokeStyle = "#f8f9fa";
    for (let x = 0; x < width; x += 72) {{
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }}
    for (let y = 0; y < height; y += 72) {{
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }}
    ctx.globalAlpha = 0.82;
    ctx.font = "14px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";
    particles.forEach((particle, index) => {{
      particle.x -= particle.speed / Math.max(width, 1);
      if (particle.x < -0.35) {{
        particle.x = 1.05;
        particle.y = Math.random();
      }}
      ctx.fillStyle = particle.color;
      ctx.fillText(particle.text, particle.x * width, particle.y * height + (index % 5) * 6);
    }});
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }}

  resize();
  window.addEventListener("resize", resize);
  draw();
}})();
</script>
{read_text(PLAYER_SRC / "tscc" / "tscc-runtime.js")}
{read_text(PLAYER_SRC / "c-player.js")}
{read_text(PLAYER_SRC / "site-theme.js")}
{read_text(PLAYER_SRC / "ntfy-chat.js")}
</body>
</html>
"""


def live_code_page():
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Code live SAE-C</title>
  <link rel="stylesheet" href="vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="player/c-player.css">
  <script>
    document.documentElement.setAttribute("data-bs-theme", localStorage.getItem("sae-c.theme.v1") || "light");
  </script>
</head>
<body class="live-page">
{main_nav("course")}
<main class="container-fluid py-3 live-page__main">
  <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
    <div>
      <h1 class="h3 mb-0" data-live-title>Code live</h1>
      <p class="text-body-secondary mb-0">Code envoye par l'enseignant via ntfy.</p>
    </div>
    <a class="btn btn-outline-secondary" href="{COURSE_INDEX}">Retour au cours</a>
  </div>
  <div data-live-code-target></div>
</main>
{site_footer()}
{read_text(PLAYER_SRC / "tscc" / "tscc-runtime.js")}
{read_text(PLAYER_SRC / "c-player.js")}
{read_text(PLAYER_SRC / "site-theme.js")}
<script>
(() => {{
  const target = document.querySelector("[data-live-code-target]");
  const title = document.querySelector("[data-live-title]");
  function encodeData(value) {{
    const json = JSON.stringify(value);
    const bytes = new TextEncoder().encode(json);
    let binary = "";
    for (const byte of bytes) binary += String.fromCharCode(byte);
    return btoa(binary);
  }}
  function readPayload() {{
    try {{
      return JSON.parse(localStorage.getItem("sae-c.live.code") || sessionStorage.getItem("sae-c.live.code") || "null");
    }} catch (_error) {{
      return null;
    }}
  }}
  const payload = readPayload();
  if (!payload || typeof payload.source !== "string") {{
    target.innerHTML = '<div class="alert alert-warning">Aucun code live recu pour le moment.</div>';
    return;
  }}
  title.textContent = payload.title || "Code live";
  const exercise = {{
    id: `live-code-${{Date.now()}}`,
    title: payload.title || "Code live",
    statement: "",
    sources: ["main.c"],
    main: "main.c",
    stdin: "",
    expected_stdout: "",
    expected_stderr: "",
    path: "",
    files: [{{ name: "main.c", content: payload.source }}],
    browser_runnable: true,
  }};
  const player = document.createElement("c-player");
  player.dataset.readonly = "false";
  player.dataset.exerciseB64 = encodeData(exercise);
  player.classList.add("live-code-player");
  target.append(player);
}})();
</script>
</body>
</html>
"""


def live_quiz_page():
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Quiz live SAE-C</title>
  <link rel="stylesheet" href="vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="player/c-player.css">
  <script>
    document.documentElement.setAttribute("data-bs-theme", localStorage.getItem("sae-c.theme.v1") || "light");
  </script>
</head>
<body class="live-page">
{main_nav("quiz")}
<main class="container py-4 live-quiz-page">
  <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-4">
    <div>
      <h1 class="h3 mb-0" data-live-quiz-title>Quiz live</h1>
      <p class="text-body-secondary mb-0">Reponse envoyee directement a l'enseignant.</p>
    </div>
    <span class="badge text-bg-secondary" data-live-username></span>
  </div>
  <section class="card" data-live-quiz-target></section>
</main>
{site_footer()}
{read_text(PLAYER_SRC / "site-theme.js")}
<script>
(() => {{
  const groupKey = "sae-c.ntfy.group";
  const liveCodeKey = "sae-c.live.code";
  const liveQuizKey = "sae-c.live.quiz";
  const groups = {{
    S3A: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3A-SAE-C/sse",
    S3B: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3B-SAE-C/sse",
    S3C: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3C-SAE-C/sse",
  }};
  let source = null;
  const target = document.querySelector("[data-live-quiz-target]");
  const title = document.querySelector("[data-live-quiz-title]");
  const usernameBadge = document.querySelector("[data-live-username]");

  function escape(value) {{
    return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
  }}

  function readPayload() {{
    try {{
      return JSON.parse(localStorage.getItem("sae-c.live.quiz") || sessionStorage.getItem("sae-c.live.quiz") || "null");
    }} catch (_error) {{
      return null;
    }}
  }}

  function storedGroup() {{
    try {{
      const value = localStorage.getItem(groupKey);
      return groups[value] ? value : "";
    }} catch (_error) {{
      return "";
    }}
  }}

  function siteBasePath() {{
    const brand = document.querySelector(".navbar-brand");
    const baseUrl = brand ? new URL(brand.getAttribute("href") || ".", window.location.href) : new URL(".", window.location.href);
    return baseUrl.pathname.replace(/[^/]*$/, "");
  }}

  function siteHref(path) {{
    return new URL(path, new URL(siteBasePath(), window.location.href)).href;
  }}

  function localSiteUrl(message) {{
    const trimmed = String(message || "").trim();
    if (!/^https?:\\/\\/\\S+$/.test(trimmed)) return null;
    try {{
      const url = new URL(trimmed);
      if (url.origin !== window.location.origin) return null;
      if (!url.pathname.startsWith(siteBasePath())) return null;
      return url;
    }} catch (_error) {{
      return null;
    }}
  }}

  function storeJson(key, value) {{
    try {{
      localStorage.setItem(key, JSON.stringify(value));
    }} catch (_error) {{
      sessionStorage.setItem(key, JSON.stringify(value));
    }}
  }}

  function parseAction(message) {{
    try {{
      const value = JSON.parse(message);
      return value && value.saec === 1 && typeof value.type === "string" ? value : null;
    }} catch (_error) {{
      return null;
    }}
  }}

  function handleLiveMessage(rawMessage) {{
    const normalized = String(rawMessage || "").replaceAll("\\r", "");
    const action = parseAction(normalized);
    if (action?.type === "navigate" && action.url) {{
      const targetUrl = localSiteUrl(action.url);
      if (targetUrl) window.location.assign(targetUrl.href);
      return;
    }}
    if (action?.type === "code") {{
      storeJson(liveCodeKey, {{
        title: action.title || "Code live",
        source: action.source || "",
        receivedAt: new Date().toISOString(),
      }});
      window.location.assign(siteHref("live-code.html"));
      return;
    }}
    if (action?.type === "live_quiz" && action.question && action.responseTopic) {{
      storeJson(liveQuizKey, {{
        id: action.id || `live-quiz-${{Date.now()}}`,
        title: action.title || "Question live",
        question: action.question,
        responseTopic: action.responseTopic,
        username: usernameBadge.textContent || "anonyme",
        receivedAt: new Date().toISOString(),
      }});
      window.location.assign(siteHref("live-quiz.html"));
      return;
    }}
    const targetUrl = localSiteUrl(normalized);
    if (targetUrl) {{
      window.location.assign(targetUrl.href);
    }}
  }}

  function connectGroupTopic() {{
    const group = storedGroup();
    if (!group || !window.EventSource) return;
    source = new EventSource(groups[group]);
    source.onmessage = (event) => {{
      try {{
        const payload = JSON.parse(event.data);
        if (payload.event === "message") handleLiveMessage(payload.message);
      }} catch (_error) {{
        handleLiveMessage(event.data);
      }}
    }};
  }}

  function render(payload) {{
    const question = payload.question;
    title.textContent = payload.title || "Quiz live";
    usernameBadge.textContent = payload.username || "anonyme";
    target.innerHTML = `
      <div class="card-header fw-semibold">${{escape(question.title || "Question")}}</div>
      <div class="card-body">
        ${{question.description ? `<p class="text-body-secondary">${{escape(question.description)}}</p>` : ""}}
        <fieldset>
          <legend class="visually-hidden">${{escape(question.title || "Question")}}</legend>
          ${{(question.options || []).map((option) => `
            <label class="form-check live-quiz-option">
              <input class="form-check-input" type="checkbox" value="${{escape(option.id)}}">
              <span class="form-check-label">${{escape(option.text)}}</span>
            </label>
          `).join("")}}
        </fieldset>
        <button class="btn btn-primary mt-3" type="button" data-submit-live-quiz>Envoyer la reponse</button>
        <div class="mt-3" data-live-quiz-feedback></div>
      </div>
    `;
    target.querySelector("[data-submit-live-quiz]").addEventListener("click", () => submit(payload));
  }}

  async function submit(payload) {{
    const selected = Array.from(target.querySelectorAll("input:checked"), (input) => input.value);
    const feedback = target.querySelector("[data-live-quiz-feedback]");
    const response = {{
      saec: 1,
      type: "quiz_response",
      quizId: payload.id,
      username: payload.username || "anonyme",
      selected,
      answeredAt: new Date().toISOString(),
    }};
    try {{
      const result = await fetch(payload.responseTopic, {{
        method: "POST",
        body: JSON.stringify(response),
      }});
      if (!result.ok) throw new Error(`HTTP ${{result.status}}`);
      feedback.innerHTML = '<div class="alert alert-success mb-0">Reponse envoyee.</div>';
      target.querySelector("[data-submit-live-quiz]").disabled = true;
    }} catch (error) {{
      feedback.innerHTML = `<div class="alert alert-danger mb-0">Echec de l'envoi : ${{escape(error.message)}}</div>`;
    }}
  }}

  const payload = readPayload();
  if (!payload || !payload.question || !payload.responseTopic) {{
    target.innerHTML = '<div class="card-body"><div class="alert alert-warning mb-0">Aucune question live recue pour le moment.</div></div>';
    connectGroupTopic();
    return;
  }}
  render(payload);
  connectGroupTopic();
}})();
</script>
</body>
</html>
"""


def admin_page(flow_items, question_bank):
    section_rows = []
    for index, item in enumerate(flow_items):
        if item["type"] == "section":
            level_class = "admin-section__title--h2" if item["level"] == 2 else ""
            section_rows.append(
                f"""
<article class="admin-section list-group-item">
  <div>
    <div class="admin-section__course">{html.escape(item["course_title"])}</div>
    <div class="admin-section__title {level_class}">{html.escape(item["title"])}</div>
  </div>
  <button class="btn btn-primary btn-sm" type="button" data-flow-index="{index}">Envoyer</button>
</article>
"""
            )
        else:
            section_rows.append(
                f"""
<article class="admin-section admin-section--question list-group-item">
  <div>
    <div class="admin-section__course">{html.escape(item["course_title"])} - {html.escape(item["quiz_title"])}</div>
    <div class="admin-section__title admin-section__title--h2">Question - {html.escape(item["title"])}</div>
  </div>
  <button class="btn btn-secondary btn-sm" type="button" data-flow-index="{index}">Poser</button>
</article>
"""
            )
    question_bank_b64 = encode_data(question_bank)
    flow_b64 = encode_data(flow_items)
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Admin SAE-C</title>
  <link rel="stylesheet" href="vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="player/c-player.css">
  <script>
    document.documentElement.setAttribute("data-bs-theme", localStorage.getItem("sae-c.theme.v1") || "light");
  </script>
  <script src="https://cdn.jsdelivr.net/npm/argon2-browser@1.18.0/dist/argon2-bundled.min.js"></script>
</head>
<body>
{main_nav("admin", include_admin=True)}
<section class="container py-4 admin-auth" data-admin-auth>
  <div class="card mx-auto" style="max-width: 32rem;">
    <div class="card-header fw-semibold">Authentification admin</div>
    <div class="card-body">
      <label class="form-label" for="admin-password">Mot de passe</label>
      <input class="form-control" id="admin-password" type="password" data-admin-password autocomplete="current-password">
      <button class="btn btn-primary mt-3" type="button" data-admin-login>Entrer</button>
      <div class="mt-3" data-admin-auth-feedback></div>
    </div>
  </div>
</section>
<main class="container py-4 admin-page" data-admin-app hidden>
  <div class="d-flex flex-wrap align-items-end justify-content-between gap-3 mb-4">
    <div>
      <h1>Admin SAE-C</h1>
      <p class="text-body-secondary mb-0">Envoyer une navigation, du code C ou un message aux etudiants connectes.</p>
    </div>
    <label class="admin-group">
      <span class="form-label fw-semibold">Groupe</span>
      <select class="form-select" data-admin-group>
        <option value="S3A">A</option>
        <option value="S3B">B</option>
        <option value="S3C">C</option>
      </select>
    </label>
  </div>

  <section class="card mb-4">
    <div class="card-header fw-semibold">Message libre</div>
    <div class="card-body">
      <label class="form-label" for="admin-message">Texte ou code C</label>
      <textarea class="form-control admin-message" id="admin-message" data-admin-message rows="12"></textarea>
      <div class="d-flex flex-wrap gap-2 mt-3">
        <button class="btn btn-primary" type="button" data-send-text>Envoyer comme texte</button>
        <button class="btn btn-secondary" type="button" data-send-code>Envoyer comme code C plein ecran</button>
      </div>
    </div>
  </section>

  <section class="card mb-4">
    <div class="card-header fw-semibold">Quiz live</div>
    <div class="card-body">
      <label class="form-label" for="admin-question-bank">Question de la banque</label>
      <select class="form-select" id="admin-question-bank" data-question-bank></select>
      <label class="form-label mt-3" for="admin-question-json">Question JSON</label>
      <textarea class="form-control admin-message" id="admin-question-json" data-question-json rows="10"></textarea>
      <div class="d-flex flex-wrap gap-2 mt-3">
        <button class="btn btn-primary" type="button" data-send-bank-question>Envoyer la question selectionnee</button>
        <button class="btn btn-secondary" type="button" data-send-json-question>Envoyer la question JSON</button>
      </div>
    </div>
  </section>

  <section class="card mb-4">
    <div class="card-header fw-semibold">Statistiques live</div>
    <div class="card-body">
      <div class="row g-3">
        <div class="col-lg-6">
          <h2 class="h5">Session courante</h2>
          <div data-live-session-stats class="admin-stats-box text-body-secondary">Aucune question live envoyee.</div>
        </div>
        <div class="col-lg-6">
          <h2 class="h5">Leaderboard</h2>
          <div data-live-leaderboard class="admin-stats-box text-body-secondary">Aucune reponse recue.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="card">
    <div class="card-header fw-semibold">Sections du cours</div>
    <div class="list-group list-group-flush">
      {''.join(section_rows)}
    </div>
  </section>

  <div class="admin-status alert mt-4" data-admin-status hidden></div>
</main>
<div class="admin-results-modal" data-results-modal hidden>
  <div class="admin-results-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="admin-results-title">
    <div class="d-flex align-items-start justify-content-between gap-3 mb-3">
      <div>
        <h2 class="h4 mb-1" id="admin-results-title" data-results-title>Resultats</h2>
        <div class="text-body-secondary" data-results-subtitle></div>
      </div>
      <button class="btn btn-outline-secondary btn-sm" type="button" data-close-results>Fermer</button>
    </div>
    <div data-results-body></div>
    <div class="d-flex flex-wrap gap-2 justify-content-end mt-3" data-results-actions></div>
  </div>
</div>
{site_footer()}
{read_text(PLAYER_SRC / "site-theme.js")}
<script>
(() => {{
  const authDigest = "{ADMIN_DIGEST}";
  const authKey = "sae-c.admin.auth.v1";
  const statsKey = "sae-c.admin.liveStats.v1";
  const flowIndexKey = "sae-c.admin.activeFlowIndex.v1";
  const questionBank = JSON.parse(new TextDecoder("utf-8").decode(Uint8Array.from(atob("{question_bank_b64}"), (char) => char.charCodeAt(0))));
  const flowItems = JSON.parse(new TextDecoder("utf-8").decode(Uint8Array.from(atob("{flow_b64}"), (char) => char.charCodeAt(0))));
  const topics = {{
    S3A: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3A-SAE-C",
    S3B: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3B-SAE-C",
    S3C: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3C-SAE-C",
  }};
  const adminTopics = {{
    S3A: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3A-SAE-C-admin",
    S3B: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3B-SAE-C-admin",
    S3C: "https://ntfy.home.nextnet.top/BUT-INFO-S3-S3C-SAE-C-admin",
  }};
  let responseSource = null;
  let activeQuiz = readActiveQuiz();
  let activeFlowIndex = readActiveFlowIndex();
  const groupSelect = document.querySelector("[data-admin-group]");
  const messageInput = document.querySelector("[data-admin-message]");
  const questionSelect = document.querySelector("[data-question-bank]");
  const questionJson = document.querySelector("[data-question-json]");
  const status = document.querySelector("[data-admin-status]");
  const authPanel = document.querySelector("[data-admin-auth]");
  const appPanel = document.querySelector("[data-admin-app]");
  const authFeedback = document.querySelector("[data-admin-auth-feedback]");
  const resultsModal = document.querySelector("[data-results-modal]");
  const resultsTitle = document.querySelector("[data-results-title]");
  const resultsSubtitle = document.querySelector("[data-results-subtitle]");
  const resultsBody = document.querySelector("[data-results-body]");
  const resultsActions = document.querySelector("[data-results-actions]");

  function setStatus(kind, message) {{
    status.hidden = false;
    status.className = `admin-status alert mt-4 alert-${{kind}}`;
    status.textContent = message;
  }}

  function setAuthFeedback(kind, message) {{
    authFeedback.innerHTML = `<div class="alert alert-${{kind}} mb-0">${{escape(message)}}</div>`;
  }}

  function escape(value) {{
    return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
  }}

  function showApp() {{
    authPanel.hidden = true;
    appPanel.hidden = false;
    populateQuestions();
    connectResponses();
    renderStats();
  }}

  async function login() {{
    const password = document.querySelector("[data-admin-password]").value;
    if (!window.argon2?.verify) {{
      setAuthFeedback("danger", "Librairie Argon2 indisponible.");
      return;
    }}
    try {{
      await window.argon2.verify({{ pass: password, encoded: authDigest }});
      sessionStorage.setItem(authKey, "true");
      showApp();
    }} catch (_error) {{
      setAuthFeedback("danger", "Mot de passe incorrect.");
    }}
  }}

  document.querySelector("[data-admin-login]").addEventListener("click", login);
  document.querySelector("[data-admin-password]").addEventListener("keydown", (event) => {{
    if (event.key === "Enter") login();
  }});

  function currentTopic() {{
    return topics[groupSelect.value];
  }}

  function currentAdminTopic() {{
    return adminTopics[groupSelect.value];
  }}

  async function publish(message) {{
    const topic = currentTopic();
    if (!topic) {{
      setStatus("warning", "Choisir un groupe.");
      return;
    }}
    try {{
      const response = await fetch(topic, {{
        method: "POST",
        body: message,
      }});
      if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}}`);
      }}
      setStatus("success", `Notification envoyee au groupe ${{groupSelect.options[groupSelect.selectedIndex].text}}.`);
    }} catch (error) {{
      setStatus("danger", `Echec de l'envoi : ${{error.message}}`);
    }}
  }}

  function action(type, payload) {{
    return JSON.stringify({{ saec: 1, type, ...payload }});
  }}

  function selectedBankQuestion() {{
    return questionBank.find((question) => question.id === questionSelect.value) || questionBank[0];
  }}

  function populateQuestions() {{
    questionSelect.innerHTML = questionBank.map((question) => `<option value="${{escape(question.id)}}">${{escape(question.label)}}</option>`).join("");
    updateQuestionJson();
  }}

  function updateQuestionJson() {{
    const question = selectedBankQuestion();
    questionJson.value = JSON.stringify(question.question, null, 2);
  }}

  function studentQuestion(question) {{
    return {{
      id: question.id,
      title: question.title,
      description: question.description || "",
      options: question.options.map((option) => ({{ id: option.id, text: option.text }})),
    }};
  }}

  function normalizeQuestion(question) {{
    if (!question.id) question.id = `live-question-${{Date.now()}}`;
    if (!Array.isArray(question.options) || question.options.length === 0) {{
      throw new Error("La question doit contenir des options.");
    }}
    if (!question.options.some((option) => option.correct === true)) {{
      throw new Error("La question doit contenir au moins une bonne reponse.");
    }}
    question.options = question.options.map((option, index) => ({{
      id: option.id || `${{question.id}}-o${{index + 1}}`,
      text: option.text || "",
      correct: option.correct === true,
    }}));
    return question;
  }}

  function startLiveQuiz(question, flowIndex = null) {{
    const fullQuestion = normalizeQuestion(JSON.parse(JSON.stringify(question)));
    const quizId = `live-${{groupSelect.value}}-${{Date.now()}}`;
    if (flowIndex !== null) {{
      activeFlowIndex = flowIndex;
      localStorage.setItem(flowIndexKey, String(flowIndex));
    }}
    activeQuiz = {{
      id: quizId,
      group: groupSelect.value,
      title: fullQuestion.title || "Question live",
      question: fullQuestion,
      startedAt: new Date().toISOString(),
    }};
    localStorage.setItem("sae-c.admin.activeQuiz.v1", JSON.stringify(activeQuiz));
    ensureSession(activeQuiz);
    publish(action("live_quiz", {{
      id: quizId,
      title: activeQuiz.title,
      question: studentQuestion(fullQuestion),
      responseTopic: currentAdminTopic(),
    }}));
    renderStats();
    openResultsModal("responses");
  }}

  function readStats() {{
    try {{
      return JSON.parse(localStorage.getItem(statsKey) || '{{"sessions":{{}},"leaderboard":{{}}}}');
    }} catch (_error) {{
      return {{ sessions: {{}}, leaderboard: {{}} }};
    }}
  }}

  function writeStats(stats) {{
    localStorage.setItem(statsKey, JSON.stringify(stats));
  }}

  function readActiveQuiz() {{
    try {{
      return JSON.parse(localStorage.getItem("sae-c.admin.activeQuiz.v1") || "null");
    }} catch (_error) {{
      return null;
    }}
  }}

  function readActiveFlowIndex() {{
    const raw = localStorage.getItem(flowIndexKey);
    const value = Number.parseInt(raw || "-1", 10);
    return Number.isFinite(value) && value >= 0 ? value : null;
  }}

  function ensureSession(quiz) {{
    const stats = readStats();
    if (!stats.sessions[quiz.id]) {{
      stats.sessions[quiz.id] = {{
        id: quiz.id,
        title: quiz.title,
        group: quiz.group,
        startedAt: quiz.startedAt,
        answers: [],
      }};
      writeStats(stats);
    }}
  }}

  function sameSet(left, right) {{
    if (left.length !== right.length) return false;
    const values = new Set(left);
    return right.every((value) => values.has(value));
  }}

  function handleQuizResponse(response) {{
    if (!response || response.type !== "quiz_response" || !activeQuiz || response.quizId !== activeQuiz.id) return;
    const stats = readStats();
    const session = stats.sessions[activeQuiz.id] || {{
      id: activeQuiz.id,
      title: activeQuiz.title,
      group: activeQuiz.group,
      startedAt: activeQuiz.startedAt,
      answers: [],
    }};
    if (session.answers.some((answer) => answer.username === response.username)) {{
      return;
    }}
    const expected = activeQuiz.question.options.filter((option) => option.correct).map((option) => option.id);
    const selected = Array.isArray(response.selected) ? response.selected : [];
    const correct = sameSet(selected, expected);
    session.answers.push({{
      username: response.username || "anonyme",
      selected,
      correct,
      answeredAt: response.answeredAt || new Date().toISOString(),
    }});
    stats.sessions[activeQuiz.id] = session;
    const user = session.answers.at(-1).username;
    stats.leaderboard[user] = stats.leaderboard[user] || {{ username: user, score: 0, answers: 0 }};
    stats.leaderboard[user].answers += 1;
    if (correct) stats.leaderboard[user].score += 1;
    writeStats(stats);
    renderStats();
  }}

  function renderStats() {{
    const stats = readStats();
    const sessionBox = document.querySelector("[data-live-session-stats]");
    const leaderboardBox = document.querySelector("[data-live-leaderboard]");
    if (!activeQuiz || !stats.sessions[activeQuiz.id]) {{
      sessionBox.textContent = "Aucune question live envoyee.";
    }} else {{
      const session = stats.sessions[activeQuiz.id];
      const correctAnswers = session.answers.filter((answer) => answer.correct);
      const podium = correctAnswers.slice(0, 3).map((answer, index) => `<li>${{index + 1}}. ${{escape(answer.username)}} <span class="text-body-secondary">${{escape(answer.answeredAt)}}</span></li>`).join("");
      sessionBox.innerHTML = `
        <p class="mb-2"><strong>${{escape(session.title)}}</strong></p>
        <p class="mb-2">${{session.answers.length}} reponse(s), ${{correctAnswers.length}} correcte(s).</p>
        <ol class="mb-0">${{podium || "<li>Aucune bonne reponse.</li>"}}</ol>
      `;
    }}
    const leaders = Object.values(stats.leaderboard || {{}}).sort((a, b) => b.score - a.score || a.username.localeCompare(b.username)).slice(0, 10);
    leaderboardBox.innerHTML = leaders.length
      ? `<ol class="mb-0">${{leaders.map((user) => `<li>${{escape(user.username)}} : ${{user.score}} / ${{user.answers}}</li>`).join("")}}</ol>`
      : "Aucune reponse recue.";
    if (!resultsModal.hidden) {{
      openResultsModal(resultsModal.dataset.mode || "responses");
    }}
  }}

  function activeSession() {{
    if (!activeQuiz) return null;
    const stats = readStats();
    return stats.sessions[activeQuiz.id] || null;
  }}

  function correctOptionLabels() {{
    if (!activeQuiz) return [];
    return activeQuiz.question.options.filter((option) => option.correct).map((option) => option.text);
  }}

  function leaderboardHtml() {{
    const stats = readStats();
    const leaders = Object.values(stats.leaderboard || {{}}).sort((a, b) => b.score - a.score || a.username.localeCompare(b.username)).slice(0, 10);
    return leaders.length
      ? `<ol class="mb-0">${{leaders.map((user) => `<li>${{escape(user.username)}} : ${{user.score}} / ${{user.answers}}</li>`).join("")}}</ol>`
      : "<p class=\\"mb-0 text-body-secondary\\">Aucune reponse recue.</p>";
  }}

  function openResultsModal(mode) {{
    if (!activeQuiz) return;
    const session = activeSession() || {{ answers: [] }};
    const correctAnswers = session.answers.filter((answer) => answer.correct);
    resultsModal.hidden = false;
    resultsModal.dataset.mode = mode;
    resultsTitle.textContent = activeQuiz.title || "Question live";
    resultsSubtitle.textContent = `Groupe ${{activeQuiz.group}}`;
    if (mode === "responses") {{
      resultsBody.innerHTML = `
        <div class="admin-results-count">${{session.answers.length}}</div>
        <p class="text-body-secondary mb-0">reponse(s) envoyee(s)</p>
      `;
      resultsActions.innerHTML = '<button class="btn btn-primary" type="button" data-show-correction>Afficher la correction</button>';
      resultsActions.querySelector("[data-show-correction]").addEventListener("click", () => openResultsModal("correction"));
      return;
    }}
    const podium = correctAnswers.slice(0, 3).map((answer, index) => `<li>${{index + 1}}. ${{escape(answer.username)}} <span class="text-body-secondary">${{escape(answer.answeredAt)}}</span></li>`).join("");
    resultsBody.innerHTML = `
      <h3 class="h5">Bonne reponse</h3>
      <ul>${{correctOptionLabels().map((label) => `<li>${{escape(label)}}</li>`).join("")}}</ul>
      <p>${{correctAnswers.length}} bonne(s) reponse(s) sur ${{session.answers.length}} reponse(s).</p>
      <h3 class="h5">Podium</h3>
      <ol>${{podium || "<li>Aucune bonne reponse.</li>"}}</ol>
      <h3 class="h5">Leaderboard</h3>
      ${{leaderboardHtml()}}
    `;
    resultsActions.innerHTML = '<button class="btn btn-primary" type="button" data-send-next>Passer a la suite</button>';
    resultsActions.querySelector("[data-send-next]").addEventListener("click", sendNextFlowItem);
  }}

  function closeResultsModal() {{
    resultsModal.hidden = true;
  }}

  function sendFlowItem(index) {{
    const item = flowItems[index];
    if (!item) {{
      setStatus("warning", "Aucun element suivant dans le parcours.");
      return;
    }}
    activeFlowIndex = index;
    localStorage.setItem(flowIndexKey, String(index));
    if (item.type === "section") {{
      const url = new URL(item.href, window.location.href);
      publish(url.href);
      closeResultsModal();
      return;
    }}
    if (item.type === "question") {{
      startLiveQuiz(item.question, index);
    }}
  }}

  function sendNextFlowItem() {{
    if (activeFlowIndex === null) {{
      setStatus("warning", "Aucune position courante dans le parcours.");
      closeResultsModal();
      return;
    }}
    sendFlowItem(activeFlowIndex + 1);
  }}

  function connectResponses() {{
    if (responseSource) responseSource.close();
    if (!window.EventSource) {{
      setStatus("warning", "SSE indisponible pour les reponses.");
      return;
    }}
    responseSource = new EventSource(`${{currentAdminTopic()}}/sse`);
    responseSource.onmessage = (event) => {{
      try {{
        const payload = JSON.parse(event.data);
        const message = payload.message ? JSON.parse(payload.message) : payload;
        handleQuizResponse(message);
      }} catch (_error) {{
        // Ignore non-quiz messages on the admin response topic.
      }}
    }};
  }}

  document.querySelector("[data-close-results]").addEventListener("click", closeResultsModal);

  document.querySelectorAll("[data-flow-index]").forEach((button) => {{
    button.addEventListener("click", () => {{
      sendFlowItem(Number.parseInt(button.dataset.flowIndex, 10));
    }});
  }});

  document.querySelector("[data-send-text]").addEventListener("click", () => {{
    publish(messageInput.value);
  }});

  document.querySelector("[data-send-code]").addEventListener("click", () => {{
    publish(action("code", {{ title: "Code live", source: messageInput.value }}));
  }});

  questionSelect.addEventListener("change", updateQuestionJson);

  document.querySelector("[data-send-bank-question]").addEventListener("click", () => {{
    startLiveQuiz(selectedBankQuestion().question);
  }});

  document.querySelector("[data-send-json-question]").addEventListener("click", () => {{
    try {{
      startLiveQuiz(JSON.parse(questionJson.value));
    }} catch (error) {{
      setStatus("danger", `Question JSON invalide : ${{error.message}}`);
    }}
  }});

  groupSelect.addEventListener("change", connectResponses);

  if (sessionStorage.getItem(authKey) === "true") {{
    showApp();
  }}
}})();
</script>
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
    lines.append("")
    lines.append(f"[Reviser avec les mini-quiz]({QUIZ_INDEX})")
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


def quiz_index_markdown(courses):
    lines = ["# Mini-quiz", ""]
    lines.append("Tous les quiz du support. La validation est enregistree localement dans le navigateur.")
    lines.append("")
    for course in courses:
        quizzes = quizzes_from_source(read_text(course["path"]), course)
        if not quizzes:
            continue
        lines.append(f"## {course['title']}")
        lines.append("")
        for quiz in quizzes:
            lines.append(render_html_quiz(quiz, fold_validated=True))
            lines.append("")
    return "\n".join(lines)


def build_quiz_pdf(courses):
    blocks = ["# Mini-quiz BUT INFO S3 SAE-C", ""]
    for course in courses:
        quizzes = quizzes_from_source(read_text(course["path"]), course)
        for quiz in quizzes:
            blocks.append(render_pdf_quiz(quiz, show_answers=False))
            blocks.append("")
    run_pandoc("\n".join(blocks), BUILD / QUIZ_PDF, html_mode=False)


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
    ZIP_DST.mkdir(parents=True, exist_ok=True)
    write_pdf_footer()
    if PLAYER_DST.exists():
        shutil.rmtree(PLAYER_DST)
    shutil.copytree(PLAYER_SRC, PLAYER_DST)
    if VENDOR_DST.exists():
        shutil.rmtree(VENDOR_DST)
    shutil.copytree(VENDOR_SRC, VENDOR_DST)

    courses = course_infos()
    all_starters = all_exercises()
    write_starter_zip(BUILD / FULL_ZIP, all_starters)
    course_starters = {}
    for course in courses:
        source = read_text(course["path"])
        exercises = [load_exercise(path) for path in exercise_directives(source)]
        zip_href = starter_zip_name(course["stem"]) if exercises else None
        if zip_href:
            write_starter_zip(BUILD / zip_href, exercises)
        course_starters[course["html"]] = zip_href

    write_text(BUILD / "index.html", landing_page())
    write_text(BUILD / LIVE_CODE_PAGE, live_code_page())
    write_text(BUILD / LIVE_QUIZ_PAGE, live_quiz_page())

    run_pandoc(course_index_markdown(courses), BUILD / COURSE_INDEX, True, "Documentation en ligne")
    postprocess_doc_page(BUILD / COURSE_INDEX, courses, COURSE_INDEX, "course", FULL_PDF, FULL_ZIP)

    run_pandoc(expand_markdown(exercises_markdown(), html_mode=True), BUILD / "exercices.html", True, "Exercices")
    postprocess_doc_page(BUILD / "exercices.html", courses, "exercices.html", "exercises", None, FULL_ZIP)

    run_pandoc(quiz_index_markdown(courses), BUILD / QUIZ_INDEX, True, "Mini-quiz")
    postprocess_doc_page(BUILD / QUIZ_INDEX, courses, QUIZ_INDEX, "quiz", QUIZ_PDF, None)

    admin_flow = []
    for course in courses:
        source = read_text(course["path"])
        run_pandoc(expand_markdown(source, html_mode=True), BUILD / course["html"], True, course["title"])
        raw_body = TITLE_BLOCK_RE.sub("", extract_body(read_text(BUILD / course["html"]))).strip()
        admin_flow.extend(admin_flow_items(course, source, raw_body))
        postprocess_doc_page(BUILD / course["html"], courses, course["html"], "course", course["pdf"], course_starters[course["html"]])
        run_pandoc(expand_markdown(source, html_mode=False), BUILD / course["pdf"], False)

    write_text(BUILD / ADMIN_PAGE, admin_page(admin_flow, live_question_bank(courses)))
    build_full_pdf(courses)
    build_quiz_pdf(courses)


if __name__ == "__main__":
    main()
