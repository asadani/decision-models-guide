#!/usr/bin/env python3
"""Render the narration scripts to MP3 with Kokoro-82M, locally and offline.

Reads narration/NN-*.txt (blank-line separated paragraphs), writes
site/audio/chNN.mp3 plus site/audio/manifest.json (durations, titles) that the
HTML edition's player reads. Only tracks whose script or settings changed are
re-rendered, so an interrupted run resumes where it stopped.

Setup (once):
    pip install kokoro-onnx soundfile numpy
    model files: kokoro-v1.0.onnx and voices-v1.0.bin. The script looks in
    $KOKORO_MODELS, then ./models, then ../narrate-your-writing/models, then
    ../mcp-101/models.

Run:
    python scripts/make_narration.py        # book -> narration/*.txt
    python scripts/generate_audio.py        # narration -> site/audio/*.mp3
    python scripts/generate_audio.py --only 06 07
    python scripts/generate_audio.py --voice bm_george --speed 0.95
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
NARRATION = ROOT / "narration"
AUDIO = ROOT / "site" / "audio"
SAMPLE_RATE = 24_000
GAP_PARAGRAPH = 0.55   # seconds of silence between paragraphs
GAP_OPENING = 0.85     # a longer beat after the opening line
CREDIT = "Synthetic voice, Kokoro-82M"


def find_models() -> Path:
    candidates = []
    if os.environ.get("KOKORO_MODELS"):
        candidates.append(Path(os.environ["KOKORO_MODELS"]))
    candidates += [ROOT / "models",
                   ROOT.parent / "narrate-your-writing" / "models",
                   ROOT.parent / "mcp-101" / "models"]
    for c in candidates:
        if (c / "kokoro-v1.0.onnx").exists() and (c / "voices-v1.0.bin").exists():
            return c
    sys.exit("Kokoro model files not found. Looked in: %s" % ", ".join(map(str, candidates)))


def resolve_voice(spec, kokoro):
    """A voice spec is a name, or names joined with + for an even blend."""
    names = [p.strip() for p in spec.split("+") if p.strip()]
    available = kokoro.get_voices()
    unknown = [n for n in names if n not in available]
    if unknown:
        sys.exit("Unknown voice(s): %s" % ", ".join(unknown))
    lang = "en-gb" if all(n.startswith("b") for n in names) else "en-us"
    if len(names) == 1:
        return names[0], lang
    blend = None
    for n in names:
        term = kokoro.get_voice_style(n) * (1.0 / len(names))
        blend = term if blend is None else np.add(blend, term)
    return blend, lang


def paragraphs(path: Path):
    blocks = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        joined = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if joined:
            blocks.append(joined)
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="bm_george+bm_fable")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--only", nargs="*", help="track numbers to render, e.g. 06 07")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list-voices", action="store_true")
    args = ap.parse_args()

    from kokoro_onnx import Kokoro
    models = find_models()
    kokoro = Kokoro(str(models / "kokoro-v1.0.onnx"), str(models / "voices-v1.0.bin"))
    if args.list_voices:
        print("\n".join(sorted(kokoro.get_voices())))
        return
    voice, lang = resolve_voice(args.voice, kokoro)

    scripts = sorted(NARRATION.glob("[0-9][0-9]-*.txt"))
    if not scripts:
        sys.exit("No narration scripts in %s; run scripts/make_narration.py first." % NARRATION)
    titles = {t["id"]: t["title"] for t in json.loads((NARRATION / "tracks.json").read_text(encoding="utf-8"))}
    wanted = set(n.zfill(2) for n in args.only) if args.only else None

    AUDIO.mkdir(parents=True, exist_ok=True)
    stamp_path = AUDIO / "stamps.json"
    stamps = json.loads(stamp_path.read_text()) if stamp_path.exists() else {}
    tracks = {}
    rendered = 0.0
    started = time.time()

    for path in scripts:
        cid = "ch" + path.name[:2]
        mp3 = AUDIO / (cid + ".mp3")
        blocks = paragraphs(path)
        key = hashlib.sha256(("\x00".join(blocks) + "|%s|%s|%s" % (args.voice, args.speed, lang))
                             .encode("utf-8")).hexdigest()[:16]
        if wanted is not None and path.name[:2] not in wanted:
            if cid in stamps and mp3.exists():
                tracks[cid] = stamps[cid]["d"]
            continue
        if not args.force and mp3.exists() and stamps.get(cid, {}).get("k") == key:
            print("%s  unchanged, skipping" % cid, flush=True)
            tracks[cid] = stamps[cid]["d"]
            continue

        print("%s  %2d paragraphs ..." % (cid, len(blocks)), end="", flush=True)
        began = time.time()
        pieces = []
        for i, block in enumerate(blocks):
            samples, rate = kokoro.create(block, voice=voice, speed=args.speed, lang=lang)
            pieces.append(samples)
            if i < len(blocks) - 1:
                gap = GAP_OPENING if i == 0 else GAP_PARAGRAPH
                pieces.append(np.zeros(int(rate * gap), dtype=samples.dtype))
        audio = np.concatenate(pieces)
        peak = float(np.max(np.abs(audio))) or 1.0
        audio = (audio / peak) * 0.89               # even loudness across tracks
        sf.write(mp3, audio, SAMPLE_RATE, format="MP3", bitrate_mode="VARIABLE", compression_level=0.4)

        duration = round(len(audio) / SAMPLE_RATE, 1)
        tracks[cid] = duration
        stamps[cid] = {"k": key, "d": duration}
        stamp_path.write_text(json.dumps(stamps, indent=1))     # record each track as it lands
        rendered += duration
        elapsed = time.time() - began
        print(" %.1f min, %.1f MB  (%.0fs, RTF %.2f)"
              % (duration / 60, mp3.stat().st_size / 1e6, elapsed, elapsed / max(duration, 1e-9)), flush=True)

    manifest = {
        "voice": args.voice,
        "credit": CREDIT,
        "dir": "audio/",
        "tracks": {cid: {"f": cid + ".mp3", "d": d, "t": titles.get(cid, cid)} for cid, d in sorted(tracks.items())},
    }
    (AUDIO / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    total = sum(tracks.values())
    print("Rendered %.1f min in %.1f min of wall clock. Book total: %.0f min across %d tracks."
          % (rendered / 60, (time.time() - started) / 60, total / 60, len(tracks)))


if __name__ == "__main__":
    main()
