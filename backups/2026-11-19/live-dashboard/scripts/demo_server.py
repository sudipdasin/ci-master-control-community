#!/usr/bin/env python3
"""Read-only synthetic CI dashboard: safe local Community preview.

Not connected to GitHub or CircleCI. No source-code writes or CI runs.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "config" / "projects.example.json"
HOST = "127.0.0.1"
PORT = int(os.environ.get("CI_COMMUNITY_PREVIEW_PORT", "8787"))


def inventory():
    """Read the bundled, non-sensitive synthetic inventory."""
    return json.loads(DATA.read_text(encoding="utf-8"))


HTML = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CI Master Control Community — Development Preview</title>
<style>
:root{color-scheme:dark;font-family:system-ui,-apple-system,sans-serif;background:#0b1220;color:#e9f1ff}
body{margin:0;padding:clamp(1rem,4vw,4rem);max-width:1120px;margin:auto}
h1{letter-spacing:-.04em;font-size:clamp(2rem,4vw,3.5rem);margin:.6rem 0}
p{color:#afc1d8;line-height:1.65}.pill{display:inline-block;border:1px solid #496181;border-radius:100px;padding:.4rem .8rem;color:#bed8fc;font-size:.8rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin:2rem 0}
article{background:#162236;border:1px solid #2d415f;border-radius:16px;padding:1.35rem}
small{color:#a9bad1}.status{color:#a9d6ff}a{color:#a9d6ff}
footer{border-top:1px solid #2d415f;padding-top:1rem;margin-top:3rem}
</style><main><span class="pill">Community • Read-only synthetic development preview</span>
<h1>CI Master Control</h1><p>Monitor, understand and review CI failures — with humans approving consequential changes.</p>
<p><strong>No CI provider connected.</strong> All repository names and statuses below are synthetic samples. This preview makes no network requests to GitHub or CircleCI.</p>
<section aria-label="Sample CI projects"><h2>Sample project status</h2><div class="grid" id="projects" role="status" aria-live="polite">Loading sample data…</div></section>
<section><h2>Hybrid control</h2><p>Future versions will propose diagnoses and repairs automatically, but code changes, reruns, merges and deployments require human approval.</p></section>
<footer><small>Development preview • Self-hosted and local-only • No real CI monitoring or repairs yet</small></footer></main>
<script>
fetch('/api/inventory').then(r=>{if(!r.ok)throw Error('Unable to load samples');return r.json()}).then(v=>{
 const root=document.getElementById('projects');root.replaceChildren();
 v.projects.forEach(p=>{const card=document.createElement('article'),h=document.createElement('h3'),status=document.createElement('p'),meta=document.createElement('small');
 h.textContent=p.repository;status.className='status';status.textContent='Sample status: '+p.status;meta.textContent='Provider: '+p.provider;
 card.append(h,status,meta);root.append(card)});
}).catch(e=>document.getElementById('projects').textContent=e.message);
</script></html>"""


class Handler(BaseHTTPRequestHandler):
    def respond(self, code, body, content_type="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/inventory":
            self.respond(200, json.dumps(inventory()).encode())
        elif path == "/health":
            self.respond(200, b'{"ok":true,"mode":"synthetic-preview"}')
        elif path == "/":
            self.respond(200, HTML.encode(), "text/html; charset=utf-8")
        else:
            self.respond(404, b'{"error":"not found"}')

    def do_POST(self):
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_PUT = do_POST
    do_DELETE = do_POST
    do_PATCH = do_POST


if __name__ == "__main__":
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
