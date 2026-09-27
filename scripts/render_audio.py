#!/usr/bin/env python3
"""Render the narration with narrate-your-writing, then write the player manifest.

The synthesis itself is done by narrate.py in the sibling narrate-your-writing
repo (Kokoro-82M, resumable, GPU-capable, per-file skip stamps). This wrapper
only fixes the settings for this book and turns narrate.py's output into
docs/audio/manifest.json, which the reading edition's player reads.

    python scripts/make_narration.py      # book -> narration/*.txt
    python scripts/render_audio.py        # narration -> docs/audio/*.mp3 + manifest.json
    python scripts/render_audio.py --manifest-only
    python scripts/render_audio.py --force --voice bm_george --speed 0.95

Where narrate.py lives: $NARRATE_YOUR_WRITING, else ../narrate-your-writing.
Its model files (kokoro-v1.0.onnx, voices-v1.0.bin) are expected in that
checkout's models/ folder; run `python narrate.py --fetch-model` there once.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NARRATION = ROOT / "narration"
AUDIO = ROOT / "docs" / "audio"
CREDIT = "Synthetic voice, Kokoro-82M"


def find_tool() -> Path:
    candidates = []
    if os.environ.get("NARRATE_YOUR_WRITING"):
        candidates.append(Path(os.environ["NARRATE_YOUR_WRITING"]))
    candidates.append(ROOT.parent / "narrate-your-writing")
    for c in candidates:
        if (c / "narrate.py").exists():
            return c
    sys.exit("narrate.py not found. Looked in: %s\nSet NARRATE_YOUR_WRITING to the checkout."
             % ", ".join(map(str, candidates)))


def write_manifest(voice: str) -> None:
    tracks = json.loads((NARRATION / "tracks.json").read_text(encoding="utf-8"))
    stamps_path = AUDIO / "stamps.json"
    stamps = json.loads(stamps_path.read_text()) if stamps_path.exists() else {}
    out = {}
    for t in tracks:
        stem = Path(t["file"]).stem
        mp3 = AUDIO / (stem + ".mp3")
        if not mp3.exists() or stem not in stamps:
            sys.exit("Missing audio or stamp for %s; run scripts/render_audio.py first." % stem)
        out[t["id"]] = {"f": mp3.name, "d": stamps[stem]["d"], "t": t["title"]}
    manifest = {"voice": voice, "credit": CREDIT, "dir": "audio/", "tracks": out}
    (AUDIO / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print("manifest: %d tracks, %.0f minutes" % (len(out), sum(v["d"] for v in out.values()) / 60))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", default="bm_george+bm_fable")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="narrate.py's own default is 0.9; this book was recorded at 1.0")
    ap.add_argument("--force", action="store_true", help="re-render every track")
    ap.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto",
                    help="passed to narrate.py; cuda needs onnxruntime-gpu in the interpreter used")
    ap.add_argument("--python", default=sys.executable,
                    help="interpreter that runs narrate.py (e.g. a conda env with onnxruntime-gpu)")
    ap.add_argument("--manifest-only", action="store_true")
    args = ap.parse_args()

    if not (NARRATION / "tracks.json").exists():
        sys.exit("No narration/tracks.json; run scripts/make_narration.py first.")
    AUDIO.mkdir(parents=True, exist_ok=True)

    if not args.manifest_only:
        tool = find_tool()
        cmd = [args.python, str(tool / "narrate.py"), str(NARRATION),
               "--out", str(AUDIO), "--engine", "kokoro",
               "--voice", args.voice, "--speed", str(args.speed), "--device", args.device,
               # make_narration.py already respells acronyms and numbers for the ear
               "--no-acronyms"]
        if args.force:
            cmd.append("--force")
        print("running:", " ".join(cmd))
        subprocess.run(cmd, cwd=str(tool), check=True)   # cwd so narrate.py finds its models/

    write_manifest(args.voice)


if __name__ == "__main__":
    main()
