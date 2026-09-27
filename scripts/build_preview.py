"""Build the local tutorial from Markdown; requires Pandoc on PATH."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'tutorial/decision-models.md').read_text(encoding='utf-8')
# The masthead supplies the title; preserve the rest of the source verbatim.
source = source.split('\n', 1)[1]
result = subprocess.run([
    'pandoc', '--from=markdown', '--to=html5', '--standalone',
    '--math-method=mathml', '--section-divs', '--toc', '--toc-depth=2',
    '--template=' + str(ROOT / 'tutorial/preview-template.html'),
], input=source, text=True, encoding='utf-8', capture_output=True, check=True)
html = result.stdout
# Mermaid expects plain diagram text, not Pandoc's nested code element.
html, count = re.subn(r'<pre class="mermaid"><code>(.*?)</code></pre>',
                     r'<pre class="mermaid">\1</pre>', html, flags=re.S)
expected = source.count('```mermaid')
if count != expected:
    raise RuntimeError(f'Expected {expected} Mermaid blocks, normalized {count}')
renderer = (ROOT / 'tutorial/preview-renderer.html').read_text(encoding='utf-8')
html = html.replace('<!-- RENDERER -->', renderer)
(ROOT / 'tutorial/decision-models.html').write_text(html, encoding='utf-8')
print(f'Built tutorial/decision-models.html ({count} diagram blocks)')
