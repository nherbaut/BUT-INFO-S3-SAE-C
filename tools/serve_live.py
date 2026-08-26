#!/usr/bin/env python3
import argparse
import posixpath
import os
import queue
import subprocess
import threading
import time
import urllib.parse
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "supports"
WATCH_DIRS = ["cours", "exercices", "projet", "tools", "web"]
WATCH_EXTENSIONS = {".c", ".css", ".h", ".html", ".js", ".json", ".md", ".png", ".py", ".tex"}
clients = set()
clients_lock = threading.Lock()


def watched_snapshot():
    snapshot = {}
    for dirname in WATCH_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in WATCH_EXTENSIONS:
                try:
                    snapshot[str(path)] = path.stat().st_mtime_ns
                except FileNotFoundError:
                    pass
    return snapshot


def build_supports():
    return subprocess.run(["python3", "tools/build_supports.py"], cwd=ROOT).returncode == 0


def broadcast_reload():
    with clients_lock:
        targets = list(clients)
    for client in targets:
        client.put_nowait("reload")


def watch_loop(interval):
    snapshot = watched_snapshot()
    while True:
        time.sleep(interval)
        current = watched_snapshot()
        if current == snapshot:
            continue
        snapshot = current
        print("Changement detecte, regeneration des supports...", flush=True)
        if build_supports():
            print("Supports regeneres, reload navigateur.", flush=True)
            broadcast_reload()
        else:
            print("Erreur pendant la regeneration, reload ignore.", flush=True)


class LiveHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BUILD), **kwargs)

    def do_GET(self):
        if self.path == "/__live-reload":
            self.handle_live_reload()
            return
        if self.is_html_request():
            self.handle_html_request()
            return
        super().do_GET()

    def end_headers(self):
        if self.path.endswith(".html") or self.path == "/":
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def is_html_request(self):
        path = urllib.parse.urlparse(self.path).path
        return path == "/" or path.endswith("/") or path.endswith(".html")

    def handle_html_request(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/" or path.endswith("/"):
            path = posixpath.join(path, "index.html")
        relative = Path(urllib.parse.unquote(path).lstrip("/"))
        target = (BUILD / relative).resolve()
        try:
            target.relative_to(BUILD.resolve())
        except ValueError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        if not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        content = target.read_text(encoding="utf-8")
        script = live_reload_script()
        if "</body>" in content:
            content = content.replace("</body>", script + "</body>", 1)
        body = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def handle_live_reload(self):
        channel = queue.Queue()
        with clients_lock:
            clients.add(channel)
        try:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            self.wfile.write(b"event: open\ndata: ok\n\n")
            self.wfile.flush()
            while True:
                message = channel.get()
                self.wfile.write(f"event: {message}\ndata: {int(time.time())}\n\n".encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with clients_lock:
                clients.discard(channel)


def live_reload_script():
    return """
<script>
(() => {
  if (!window.EventSource) return;
  const source = new EventSource("/__live-reload");
  source.addEventListener("reload", () => window.location.reload());
})();
</script>
"""


def main():
    parser = argparse.ArgumentParser(description="Serve build/supports with live reload.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    if not build_supports():
        raise SystemExit(1)

    watcher = threading.Thread(target=watch_loop, args=(args.interval,), daemon=True)
    watcher.start()

    server = ThreadingHTTPServer(("", args.port), LiveHandler)
    print(f"Site local avec live reload: http://localhost:{args.port}/", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
