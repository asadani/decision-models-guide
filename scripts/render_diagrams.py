"""Render assets/diagrams/src/*.tex to PNG in assets/diagrams/generated/.

Each source is a standalone TikZ document. pdflatex makes a vector PDF and
PyMuPDF rasterizes it, so no other tools are needed. A diagram is rebuilt only
when its source is newer than its PNG; pass --force to rebuild all.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "diagrams" / "src"
OUT = ROOT / "assets" / "diagrams" / "generated"
DPI = 260


def render(tex: Path) -> Path:
    png = OUT / (tex.stem + ".png")
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={tmp}", str(tex)],
            capture_output=True, text=True, cwd=tmp)
        pdf = Path(tmp) / (tex.stem + ".pdf")
        if result.returncode != 0 or not pdf.exists():
            sys.stdout.write(result.stdout[-2000:])
            raise SystemExit(f"pdflatex failed for {tex.name}")
        with pymupdf.open(pdf) as doc:
            doc[0].get_pixmap(dpi=DPI, alpha=False).save(png)
    return png


def main() -> None:
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    sources = sorted(SRC.glob("*.tex"))
    if not sources:
        raise SystemExit(f"no diagram sources in {SRC}")
    for tex in sources:
        png = OUT / (tex.stem + ".png")
        if not force and png.exists() and png.stat().st_mtime >= tex.stat().st_mtime:
            print(f"up to date  {png.name}")
            continue
        render(tex)
        print(f"rendered    {png.name}")


if __name__ == "__main__":
    main()
