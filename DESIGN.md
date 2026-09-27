# Tutorial reading theme

The user selected the local `../mcp-101/index.html` as the visual reference.
This is a long-form educational content page, not an application dashboard.

- Match its light grid-paper surface, IBM Plex Sans body, Sans Condensed uppercase display, and Mono labels/code.
- Preserve the 1180px frame, 186px sticky chapter rail, 44px column gap, and single-column layout below 860px.
- Use magenta for model judgment, teal for application policy, and ochre for evidence/evaluation. The masthead labels explain these roles.
- `tutorial/preview.css` owns color and typography tokens. Mermaid reads color tokens from computed CSS rather than copying them.
- `tutorial/preview-template.html` owns the page structure. Markdown remains the tutorial source; `scripts/build_preview.py` regenerates HTML.
- Diagram rendering consumes plain text, handles each figure independently, and preserves source on errors. Tables and wide figures scroll within the content column.
- Preserve native navigation, visible keyboard focus, a skip link, reduced-motion behavior, readable fallback fonts, and print styling.

No publication or live-model execution is part of this theme correction.
