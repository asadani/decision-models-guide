"""Build the reading edition: site/index.html with the narration player.

Pandoc turns the book's Markdown (without the print-only cover, copyright and
contents pages) into one HTML page in the project's reading theme. The audio
manifest written by scripts/generate_audio.py is embedded, and each track is
attached to its chapter. If there is no manifest, the page is built without a
player and works as a plain reading copy.

Run:  python scripts/build_html.py
Output: site/index.html, site/style.css, site/player.js, site/assets/...
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
SITE = ROOT / "site"

SOURCES = ([BOOK / "00-front-matter/03-preface.md", BOOK / "00-front-matter/04-how-to-read.md"]
           + sorted((BOOK / "01-chapters").glob("*.md"))
           + sorted((BOOK / "02-appendices").glob("*.md")))


def main():
    if not shutil.which("pandoc"):
        sys.exit("pandoc is required")
    SITE.mkdir(exist_ok=True)

    body = "\n\n".join(p.read_text(encoding="utf-8").replace("../../assets/", "assets/") for p in SOURCES)
    md = ROOT / "output" / "site-body.md"
    md.parent.mkdir(exist_ok=True)
    md.write_text(body, encoding="utf-8", newline="\n")

    html_path = SITE / "index.html"
    subprocess.run(
        ["pandoc", str(md),
         "--from", "markdown+footnotes+pipe_tables+task_lists+smart+tex_math_dollars",
         "--to", "html5", "--standalone", "--section-divs", "--wrap=none",
         "--toc", "--toc-depth=1", "--reference-location=section", "--mathml",
         "--lua-filter", str(ROOT / "build/chapter-headings.lua"),
         "--template", str(ROOT / "build/site-template.html"),
         "-o", str(html_path)],
        check=True, cwd=str(ROOT))
    html = html_path.read_text(encoding="utf-8")

    # Top-level sections in document order: preface, how to read, chapters, appendices.
    sections = re.findall(r'<section id="([^"]+)"[^>]*class="level1[^"]*"', html)
    if len(sections) < 14:
        sys.exit("expected at least 14 top-level sections, found %d" % len(sections))

    manifest_path = SITE / "audio" / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        tracks = manifest["tracks"]
        for cid, track in tracks.items():
            n = int(cid[2:])
            track["sec"] = sections[n]
            # Sanity check: the section's heading should match the track title.
            m = re.search(r'<section id="%s"[^>]*>\s*<h1[^>]*>(.*?)</h1>' % re.escape(sections[n]), html, re.S)
            heading = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            a = re.sub(r"[^a-z0-9]", "", heading.lower())
            b = re.sub(r"[^a-z0-9]", "", track["t"].lower())
            if a[:12] != b[:12]:
                sys.exit("track %s (%r) does not match section heading %r" % (cid, track["t"], heading.strip()))
        block = "var AUDIO = %s;" % json.dumps(manifest, ensure_ascii=False)
        html = html.replace("var AUDIO = null;", block, 1)
        print("player: %d tracks attached, %.0f minutes"
              % (len(tracks), sum(t["d"] for t in tracks.values()) / 60))
    else:
        print("player: no audio manifest found; building a reading copy without narration")

    html_path.write_text(html, encoding="utf-8", newline="\n")

    # Stylesheet, script and assets.
    css = (ROOT / "tutorial/preview.css").read_text(encoding="utf-8") + "\n" + \
          (ROOT / "build/site-extra.css").read_text(encoding="utf-8")
    (SITE / "style.css").write_text(css, encoding="utf-8", newline="\n")
    shutil.copyfile(ROOT / "build/site-player.js", SITE / "player.js")
    dest = SITE / "assets" / "diagrams" / "generated"
    dest.mkdir(parents=True, exist_ok=True)
    for png in (ROOT / "assets/diagrams/generated").glob("*.png"):
        shutil.copyfile(png, dest / png.name)
    pdf = ROOT / "output" / "decision-models.pdf"
    if pdf.exists():
        shutil.copyfile(pdf, SITE / "decision-models.pdf")

    # Every reader-facing page needs the site header with a link home (screen only).
    nav = re.search(r'<nav class="sitebar"[^>]*>(.*?)</nav>', html, re.S)
    if not nav or "href=" not in nav.group(1):
        sys.exit("site header (nav with a link home) is missing")
    print("built %s (%d KB), %d sections" % (html_path.relative_to(ROOT), html_path.stat().st_size // 1024, len(sections)))


if __name__ == "__main__":
    main()
