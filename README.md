# Decision models: from a typed prediction to an accountable action

A short book on Jev and other decision models: what they return, how to read the numbers, what the early experiments actually showed, and the policy that has to sit between a prediction and an action. It comes as a PDF, a paperback interior, and a reading edition you can also listen to.

## Read or listen

- **Reading edition with narration:** open [`site/index.html`](site/index.html) in a browser. Fonts load over the network; everything else is local. The narration (100 minutes, a synthetic voice) is in `site/audio/`.
- **PDF:** `make pdf` writes `output/decision-models.pdf` (Letter). `make paperback` writes the 6x9 interior.

## What is in it

Eleven chapters, a preface and three appendices.

| | |
|---|---|
| 1 | The ticket that isn't one question |
| 2 | What a decision model is, and isn't |
| 3 | Reading the numbers |
| 4 | One real call |
| 5 | A measured case (Banking77, and a security benchmark) |
| 6 | The cascade that made things worse |
| 7 | The alternatives |
| 8 | Between prediction and action |
| 9 | The accountability argument |
| 10 | Extending the pattern to coding agents |
| 11 | What to build first |
| A, B, C | What was and was not validated; glossary; sources |

## Build

Needs Pandoc, a LaTeX install with `pdflatex`, Python and `make`.

```text
make diagrams      # TikZ sources in assets/diagrams/src -> PNG
make pdf paperback
make verify        # every URL in book/ must return 2xx or 3xx
python scripts/check_book_claims.py   # numbers and quotations against their sources
```

The narration and the reading edition:

```text
python scripts/make_narration.py      # book -> narration/*.txt
python scripts/generate_audio.py      # narration -> site/audio/*.mp3 (Kokoro-82M, CPU, resumable)
python scripts/build_html.py          # -> site/index.html with the player
node scripts/check_site.cjs           # structure and layout checks (Playwright)
```

Kokoro needs `pip install kokoro-onnx soundfile numpy` and the two model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`); `generate_audio.py` looks in `$KOKORO_MODELS`, `./models`, and the sibling `narrate-your-writing` and `mcp-101` folders. Nothing is sent anywhere.

## Layout

```text
book/00-front-matter, 01-chapters, 02-appendices   the manuscript (Markdown)
build/          pandoc metadata, the chapter-heading filter, the reading-edition template
scripts/        build, claim checking, narration, site checks
assets/diagrams TikZ sources and rendered PNGs (original figures)
examples/       the offline lab (Chapter 8) and the optional live call (Chapter 4)
narration/      spoken-form scripts, one per audio track (derived from book/)
site/           the reading edition and its audio
.research/      source ledger, claim ledger, captured sources, page-image checks
tutorial/       the earlier tutorial draft, kept for reference
archive/        the supplied PDFs and notes (jev.txt, links.txt, other-model.txt); not in git
```

## Run the offline lesson

```text
python examples/decision_workflow.py
python -m unittest discover -s examples -p "test_*.py" -v
```

No dependencies or credentials are needed. Its predictions are synthetic, not measurements of any model.

## Optional Jev call

`examples/jev_triage.py` uses the TypeSafe Python API documented on 26 September 2026. Install `typesafe-sdk==0.7.1` in a separate environment and set `TYPESAFE_API_KEY`. It sends a synthetic ticket and prints interpretations; it does not issue a refund. It has not been run live: the code was syntax-checked and compared with the documentation.

## What was and was not validated

No live Jev call was made and no benchmark was reproduced. Every measurement in the book is reported by the person who ran it. Numbers from scanned PDFs were compared with page images where they carry an argument. The full list, and the places where sources overreach, is Appendix A. The source pack, in `.research/`, holds captured pages and PDF extracts as research records, not material to republish.

The book is an independent work. It is not affiliated with or endorsed by TypeSafe AI or any project it discusses.
