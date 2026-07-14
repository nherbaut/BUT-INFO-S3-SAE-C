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
DIRECTIVE = re.compile(r"^\{\{\s*(c_demo|c_exercise)\s*:\s*([^}]+?)\s*\}\}\s*$")
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
    while index < len(lines):
        line = lines[index]
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
        (QUIZ_INDEX, "Quiz", active == "quiz"),
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
{read_text(PLAYER_SRC / "site-theme.js")}
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

    run_pandoc(course_index_markdown(courses), BUILD / COURSE_INDEX, True, "Documentation en ligne")
    postprocess_doc_page(BUILD / COURSE_INDEX, courses, COURSE_INDEX, "course", FULL_PDF, FULL_ZIP)

    run_pandoc(expand_markdown(exercises_markdown(), html_mode=True), BUILD / "exercices.html", True, "Exercices")
    postprocess_doc_page(BUILD / "exercices.html", courses, "exercices.html", "exercises", None, FULL_ZIP)

    run_pandoc(quiz_index_markdown(courses), BUILD / QUIZ_INDEX, True, "Mini-quiz")
    postprocess_doc_page(BUILD / QUIZ_INDEX, courses, QUIZ_INDEX, "quiz", QUIZ_PDF, None)

    for course in courses:
        source = read_text(course["path"])
        run_pandoc(expand_markdown(source, html_mode=True), BUILD / course["html"], True, course["title"])
        postprocess_doc_page(BUILD / course["html"], courses, course["html"], "course", course["pdf"], course_starters[course["html"]])
        run_pandoc(expand_markdown(source, html_mode=False), BUILD / course["pdf"], False)

    build_full_pdf(courses)
    build_quiz_pdf(courses)


if __name__ == "__main__":
    main()
