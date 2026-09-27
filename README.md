# Decision models: from a typed prediction to an accountable action

A short book on Jev and other decision models: what they return, how to read the numbers, what the early experiments actually showed, and the policy that has to sit between a prediction and an action. It comes as a PDF, a paperback interior, and a reading edition you can also listen to.

## Read or listen

- **Reading edition with narration:** https://tech.anujsadani.in/decision-models-guide/ (source: [`docs/index.html`](docs/index.html), which also opens from disk; fonts load over the network). The narration is 100 minutes in a synthetic voice, in `docs/audio/`.
- **Typeset PDF:** sold on [Ko-fi](https://ko-fi.com/s/9e3a539eb0). It is not published in this repo or on the site. `make pdf` builds it (`output/decision-models.pdf`, Letter, with the cover); `make paperback` builds the 6x9 interior.

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
python scripts/render_audio.py        # narration -> docs/audio/*.mp3 via narrate-your-writing (Kokoro-82M, resumable) + manifest
python scripts/build_html.py          # -> docs/index.html with the player (GitHub Pages serves docs/)
node scripts/check_site.cjs           # structure and layout checks (Playwright)
```

Rendering uses `narrate.py` from the sibling [`narrate-your-writing`](../narrate-your-writing) checkout (or `$NARRATE_YOUR_WRITING`), including its model files (`python narrate.py --fetch-model` there once). `render_audio.py` only fixes this book's settings and writes the manifest the player reads. Nothing is sent anywhere.

## Layout

```text
book/00-front-matter, 01-chapters, 02-appendices   the manuscript (Markdown)
build/          pandoc metadata, the chapter-heading filter, the reading-edition template
scripts/        build, claim checking, narration, site checks
assets/diagrams TikZ sources and rendered PNGs (original figures)
assets/cover   front cover (PNG, 1024x1536) and the prompt it was generated from; the screen PDF opens with it
examples/       the offline lab (Chapter 8) and the optional live call (Chapter 4)
narration/      spoken-form scripts, one per audio track (derived from book/)
docs/           the reading edition and its audio (served by GitHub Pages)
.research/      source ledger, claim ledger, captured sources, page-image checks
tutorial/       the earlier tutorial draft (Markdown only), kept for reference
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
