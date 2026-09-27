# Project handoff: decision-models-guide

Last updated: 27 September 2026.

## Book rewrite and narration — 27 September 2026

This supersedes the tutorial (`tutorial/`) as the main deliverable. The user found the tutorial thin, asked for a full essay using the detail in the PDFs, links and notes, chose about 30 pages, and asked for the book-writing skill's format (author, preface, front matter).

**What exists**

- `book/` is the manuscript in the skill's layout: `00-front-matter/` (title, copyright, contents, preface, how to read), `01-chapters/` (11 chapters), `02-appendices/` (A validation, B glossary, C sources). About 13.6K words of chapters plus front and back matter. Footnotes are chapter-scoped ids (`[^chN-k]`); a repeated source in a chapter gets a short-form note.
- Build: `make pdf` (Letter, 62 pp), `make paperback` (6x9 interior, 90 pp with blank versos), `make verify` (26 URLs; `build/link-allowlist.txt` skips one POST-only endpoint), `make diagrams` (TikZ sources in `assets/diagrams/src/` to PNG). On Windows pandoc's `--resource-path` separator is `;`; the Makefile handles it.
- Cover: `assets/cover/decision-models-front-cover.png` (supplied; 1024x1536, text matches the book). `make pdf` puts it on page 1 via `build/frontcover.tex`; the paperback interior has none. The reading edition shows a 720px JPEG in the masthead. 1024x1536 is fine for Ko-fi and screens but too small for print: a 6x9 KDP cover needs at least 1800x2700.
- Published as `docs/` (GitHub Pages, `https://tech.anujsadani.in/decision-models-guide/`). The typeset PDF is sold on Ko-fi (https://ko-fi.com/s/9e3a539eb0) and is deliberately not in the repo or on the site; the reading edition links to Ko-fi in its header, masthead and footer.
- Trimmed to what the book needs: the research-phase scripts (source capture, OCR, reference rendering), the tutorial's HTML page and its builder, and `DESIGN.md` were removed. `tutorial/` keeps the Markdown only; the base theme moved to `build/site-base.css`.
- Claim ledger: `python scripts/check_book_claims.py` checks 80 claims (60 against captured source text, 5 read from page images, 15 recomputed) and writes `.research/book-claims.jsonl`. Numbers taken from OCR'd PDFs were checked against rendered page images where they matter; Appendix A lists what was and was not verified.
- Narration: `scripts/make_narration.py` derives `narration/NN-*.txt` from the book (spoken versions of tables, code, figures and equations are in `scripts/narration_say.py`); `scripts/render_audio.py` calls `narrate.py` from the sibling `narrate-your-writing` repo (Kokoro-82M, voice `bm_george+bm_fable`, speed 1.0, `--no-acronyms`; resumable) and writes `docs/audio/manifest.json` for the player. The existing audio was rendered by an earlier in-repo renderer with the same model, voice and speed; its stamps were converted to narrate.py's format so it is recognized as current. A forced re-render through narrate.py runs about 3 percent longer (pauses between sentence chunks). `scripts/build_html.py` builds the reading edition `docs/index.html` with the player; `node scripts/check_site.cjs` checks it (needs Playwright via `NODE_PATH` and `PREVIEW_CHROMIUM`).

**Decisions and cautions**

- No live Jev call was made; no benchmark reproduced. Every measurement is reported by its author and attributed.
- The preface, "How this book was written" and the one-line "About the author" are drafts in the author's voice and need the author's review.
- The `jev.txt` accountability ideas (Chapter 9) and the coding-agent document (Chapter 10) are presented as proposals. The coding-agent PDF's attribution to TypeSafe's founder is unverified.
- Writing files with Python heredocs mangles backslashes on this machine; use the file-edit tool for anything containing LaTeX.
- The old `tutorial/` and its research scripts are kept for reference; the README points to the book.

## Theme and Mermaid correction — 27 September 2026

The user reported Mermaid syntax errors and selected the sibling `mcp-101` theme. This supersedes the earlier preview/visual-QA status below.

- Fixed Pandoc's nested `<code>` wrapper being passed to Mermaid. The builder strips it; rendering uses explicit text content and handles each graph independently.
- Added `tutorial/preview-template.html`; rebuilt the page with the MCP-101 grid-paper palette, IBM Plex fonts, condensed headings, chapter rail, code/table panels and responsive layout. Design intent is in `DESIGN.md`.
- Changed three wide source diagrams from left-to-right to top-to-bottom. All five now fit the desktop reading column; mobile figures have keyboard-accessible internal scrolling.
- Verified with installed Chromium/Playwright after the connected-browser tool returned no browsers. Temporary test packages were installed under the user Temp directory. No live model SDK was installed.
- Desktop 1440px and mobile 390px: five rendered SVGs, zero Mermaid errors, seven MathML expressions, no page overflow or broken fragment links. Navigation, reduced motion and offline source fallback passed. Screenshots and JSON evidence are in `.research/preview-qa/`; repeatable test is `scripts/check_preview.cjs`.
- Preview still loads Mermaid 11.12.0 and Google fonts over the internet. No publication occurred.

## Folder rename and immediate resume

Resume update (26 September 2026): the directory rename is confirmed complete at the expected location below. The earlier rename notes describe the previous session. This directory currently has no Git repository metadata.

The user requested continuation without selecting a follow-up. A local reading preview was chosen as the reversible next step; no publishing destination was selected. Added `tutorial/decision-models.html`, `tutorial/preview.css`, `tutorial/preview-renderer.html` and `scripts/build_preview.py`. Rebuild with `python scripts/build_preview.py` (requires Pandoc). Mermaid 11.12.0 loads from jsDelivr; math uses native MathML. Markdown is still the source of truth.

Resume checks: all six tests pass, offline demo runs, optional integration compiles, citation gate remains PASS with 0 hard failures / 80 advisory warnings. Generated HTML structure and local/fragment links were checked. Browser QA could not run: the browser automation tool reports no available browsers. Do not claim diagrams or equations have been visually verified. No SDK installation or live model call was performed.

The user chose `decision-models-guide` as the project directory name. An attempted rename from `decision-model` was blocked by a Windows file lock; no rename or file move occurred. The user will close this session, rename the directory manually, and reopen it.

Expected location after rename: `C:/Users/anuj_/gitrepo/asadani/decision-models-guide`.

Read this file, `README.md`, and `tutorial/plan.md` when resuming. Work is already saved; do not repeat source collection or regenerate the tutorial from scratch. No background job needs to be resumed. Internal deliverable links are relative and should survive the rename. Capture/verification scripts reference the installed research plugin under the user's `.codex/plugins` directory; those external paths are separate from the project name.

## User intent and preferences

Create a detailed tutorial on decision models, centered on TypeSafe AI's Jev and several alternatives. First collect the supplied articles and scrape `links.txt`, group overlapping information, and design a natural learning path. Include code, diagrams, concerns/risks and next steps from `jev.txt`.

Do not copy personal/article diagrams. Create original explanatory diagrams. If an official company image is used, credit its owner and link the original article next to it; check reuse permission/license separately. No third-party artwork is embedded in the current tutorial.

Audience/format assumption: Python developers familiar with basic LLM APIs; editable Markdown. This was offered as an optional clarification, but no explicit audience/publishing preference was received. The user has not yet reviewed or approved the tutorial content or selected a publishing destination. Nothing has been published, committed or pushed.

## Completed deliverables

- `tutorial/decision-models.md`: approximately 4,100 words before references; eleven learning sections; five original Mermaid diagrams; 29 claim references. Covers Jev, Laya, Decision 1.0, GLiNER2.5-Decide, AnyJev and SemIf.
- `tutorial/plan.md`: chapter layout, source grouping, deduplication, corrections and completion criteria.
- `tutorial/assets.md`: diagram provenance and optional image attribution/reuse policy.
- `README.md`: entry point and run instructions.
- `examples/decision_workflow.py`: dependency-free offline lesson using synthetic predictions, probability validation, routing/review policy, calibration metrics and a minimal receipt.
- `examples/test_decision_workflow.py`: six boundary/arithmetic tests.
- `examples/jev_triage.py`: optional Jev call based on the documented Python SDK interface; sends a synthetic ticket and executes no business action.

## Research and evidence

All five PDFs (72 pages total) were processed. Four were scanned image-only PDFs and required Windows OCR; the engineering PDF had native text. All four URLs in `links.txt` were captured. Archestra was captured through the browser after shell DNS failed. Additional embedded URLs were inventoried; not every incidental reference or video was followed.

- `.research/synthesis.md`: thematic source map, findings and limits.
- `.research/pdf-reading-notes.md`: detailed reading notes for all five PDFs, with page locators and figure inventories.
- `.research/sources.jsonl`: 33 captured source records (8 T1, 13 T2, 1 T3, 11 T4).
- `.research/claims.jsonl`: 29 source-bound claims.
- `.research/snapshots/`: immutable captured source text with hashes.
- `.research/extracted/` and `.research/rendered/`: PDF text/OCR and research page renders.
- `.research/url-inventory.json`: links in the supplied text files.
- `.research/claim-audit.md`: independent semantic audit, 29 pass / 0 fail.
- `.research/final-review.md`: final editorial/code review and resolution of its minor suggestions.
- `.research/verification-report.md`: mechanical citation gate PASS, 0 hard failures, 80 advisory warnings. Warnings largely concern original teaching examples, arithmetic and recommendations; they were reviewed, not suppressed. A gate pass is not model-performance validation.
- `.research/offline-demo-result.json`: recorded synthetic lesson output.
- `.research/state.yaml`: phase `reported`; deliverable path and validation status.

Original user-supplied files are unchanged. Captured articles, scanned pages and OCR are research inputs, not publication assets to republish wholesale.

## Important editorial decisions to preserve

- Schema validity is not semantic correctness or authorization.
- RLVR and TypeSafe's RLCD are distinct; a training objective does not guarantee perfect calibration.
- TypeSafe Choice/Score confidence is a derived signal; Noul has no separate confidence field. Do not transfer thresholds blindly between models or question types.
- `lasa.pdf` is about **Laya**.
- Fastino's **JevK5** benchmark comparator is not TypeSafe **Jev**.
- AnyJev is a readout/debiasing/calibration toolkit, not merely a pretrained checkpoint. Current SemIf documentation includes workload calibration.
- Decision 1.0 native vLLM-SR integration is described as planned in the captured release.
- The supplied Banking77 experiment reports that one fallback setup fixed 84 errors but introduced 211. This was visually checked on PDF page 22; it remains an attributed, unreplicated experiment, not a universal claim that cascades fail.
- The coding-agent PDF is an independent synthesis, not an official TypeSafe whitepaper. Its cost/token figures and proposed architecture are not measured production results.
- Commercial-incentive concerns in `jev.txt` are hypothetical threats and design proposals, not supported allegations about named vendors.
- A hash is not immutable storage, a receipt is not hidden model reasoning, and a second model is not an independent authority by default.

## Validation and remaining limits

Executed successfully:

```text
python examples/decision_workflow.py
python -m unittest discover -s examples -p "test_*.py" -v
python -m py_compile examples/jev_triage.py
```

All six tests passed. Python snippets parse; local deliverable links resolve. Mermaid diagrams are supplied as source blocks for compatible Markdown viewers; rendered diagram QA has not been performed.

The TypeSafe SDK was NOT installed, and the live Jev example was NOT executed. Its API shape was checked against captured docs and its Python syntax compiled. No model weights were downloaded; no vendor/practitioner benchmark was reproduced. The offline data is synthetic and must never be presented as a model benchmark.

## Possible next work, awaiting user direction

1. Review the chapter layout and draft with the user; adjust depth, audience and examples.
2. Choose a publishing format, then render and visually review diagrams/math for that target.
3. Validate the optional live integration in an isolated environment if the user wants it and provides appropriate access; preserve the synthetic-only baseline.
4. Build a real, labeled application evaluation and test model/cascade behavior before making deployment recommendations.

Do not assume that these follow-ups authorize publishing, paid model calls, or uploading private data.

## Tooling notes

`rg` was unavailable; PowerShell enumeration/search was used. Windows built-in OCR is available through the saved `scripts/ocr-pages.ps1`. Toward the end, `apply_patch` and `view_image` hit a sandbox-helper argument error; ordinary `exec_command` still worked, so text edits used PowerShell/Python. This was an environment issue, not a damaged project.

Research tools live at:
`C:/Users/anuj_/.codex/plugins/cache/research-anything/research-anything/0.1.0/scripts`.

To rerun the gate (from the renamed project directory):

```text
python -X utf8 C:/Users/anuj_/.codex/plugins/cache/research-anything/research-anything/0.1.0/scripts/verify_claims.py --workspace .research --report tutorial/decision-models.md --quiet
```

`scripts/render_references.py` regenerates references from the ledgers. Capture scripts append source records; do not rerun them casually and duplicate the corpus. Preserve original snapshot bytes and hashes when updating research.
