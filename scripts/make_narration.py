"""Turn the book's Markdown into narration scripts (one .txt per audio track).

The scripts are derived, not hand-written: prose is read as written, footnotes
and links are dropped, and every table, code block, figure and display formula
is replaced by the spoken version in scripts/narration_say.py. The converter
fails if an element has no spoken version.

Run:  python scripts/make_narration.py
Output: narration/NN-slug.txt  (blank-line separated paragraphs)
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from narration_say import INLINE, SAY  # noqa: E402
import mindmaps  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
OUT = ROOT / "narration"

# (track number, output slug, source file, chapter prefix for SAY, intro paragraphs, outro paragraphs, title)
# The card is read from its <!-- narrate-from --> marker: the legal lines stay in print and on the page.
CH = BOOK / "01-chapters"
TRACKS = [
    (0, "card", BOOK / "00-front-matter/01-copyright.md", None,
     ["Decision Models. From a Typed Prediction to an Accountable Action.",
      "By Anuj Sadani. An independent work, not affiliated with TypeSafe AI or any project discussed in it."], [],
     "Copyright, permissions, and how this was made"),
] + [
    (n, "chapter-%02d" % n, next(CH.glob("%02d-*.md" % n)), "%02d" % n, [], [], None) for n in range(1, 14)
] + [
    (14, "appendix-a", BOOK / "02-appendices/A-what-was-validated.md", None, [],
     ["The glossary, the full list of sources and the reference tables are in the written edition."], None),
]

# Words the text-to-speech model gets wrong, respelled for the ear. Order matters.
PRON = [
    (r"a single POST to https?://api\.typesafe\.ai/v1/systemone",
     "a single post request to the TypeSafe API's system-one address"),
    (r"https?://\S+", ""),
    (r"\bjev-1\.13\.0\b", "jev one point thirteen point zero"),
    (r"\bjev-latest\b", "jev latest"),
    (r"\bjev-preview\b", "jev preview"),
    (r"\btypesafe-sdk\b", "typesafe S D K"),
    (r"\bjev\.txt\b", "the supplied notes file"),
    (r"\bexamples/decision_workflow\.py\b", "the decision workflow example"),
    (r"\bexamples/\b", "the examples folder"),
    (r"\bmake verify\b", "make verify"),
    (r"GPT-5\.6 Terra", "G P T five point six Terra"),
    (r"GPT-5\.4", "G P T five point four"),
    (r"Qwen3-Coder-Next-80B-A3B", "Kwen three Coder Next, eighty B, A three B"),
    (r"Qwen3\.5", "Kwen three point five"),
    (r"\bQwen\b", "Kwen"),
    (r"\bMiniCPM\b", "Mini C P M"),
    (r"Sonnet 5", "Sonnet five"),
    (r"DeepSeek-R1", "DeepSeek R one"),
    (r"DeepSeek R1", "DeepSeek R one"),
    (r"InstructGPT", "Instruct G P T"),
    (r"ChatGPT", "Chat G P T"),
    (r"Banking77", "Banking seventy-seven"),
    (r"GLiNER2\.5-Decide", "Glee-ner two point five Decide"),
    (r"GLiNER-2\.5-Decide", "Glee-ner two point five Decide"),
    (r"GLiNER2\.5", "Glee-ner two point five"),
    (r"GLiNER", "Glee-ner"),
    (r"\bJevK5\b", "Jev K five"),
    (r"\bAnyJev\b", "Any Jev"),
    (r"\bSemIf\b", "Sem If"),
    (r"\bHoang\b", "Wahng"),
    (r"\bBrier\b", "Bryer"),
    (r"\bunicodeveloper\b", "unicode developer"),
    (r"\bvLLM-SR\b", "v L L M S R"),
    (r"\bvLLM\b", "v L L M"),
    (r"\bKV cache\b", "K V cache"),
    (r"\bL0\b", "L zero"),
    (r"\bL1\b", "L one"),
    (r"\bL2\b", "L two"),
    (r"max\(8, 2K\)", "the larger of eight and two K"),
    (r"CC BY 4\.0", "C C B Y four point oh"),
    (r"SHA-256", "S H A two fifty-six"),
    (r"\bRLHF\b", "R L H F"),
    (r"\bRLVR\b", "R L V R"),
    (r"\bRLCD\b", "R L C D"),
    (r"\bECE\b", "E C E"),
    (r"\bLLMs\b", "L L Ms"),
    (r"\bLLM\b", "L L M"),
    (r"\bAPIs\b", "A P Is"),
    (r"\bAPI\b", "A P I"),
    (r"\bSDK\b", "S D K"),
    (r"\bJSON\b", "Jason"),
    (r"\bHTTP\b", "H T T P"),
    (r"\bOCR\b", "O C R"),
    (r"\bPDFs\b", "P D Fs"),
    (r"\bPDF\b", "P D F"),
    (r"\bGPU\b", "G P U"),
    (r"\bAI\b", "A I"),
    (r"\bPOST\b", "post"),
    (r"\bTDS\b", "T D S"),
    (r"(\d) ?ms\b", r"\1 milliseconds"),
    (r"(\d) ?Hz\b", r"\1 hertz"),
    (r"(\d(?:\.\d)?)B\b", r"\1 billion"),
    (r"(\d+)M\b", r"\1 million"),
]
PRON = [(re.compile(p), r) for p, r in PRON]

STEP_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
DIGIT_WORDS = "zero one two three four five six seven eight nine".split()


def normalize_numbers(text: str) -> str:
    """Make numbers come out right in the speech engine.

    Checked against the engine's phonemizer: a thousands comma is read as a
    pause ("3,080" becomes "three, zero eighty"), a dollar sign is read before
    the number, and a decimal with two or more fractional digits is read as one
    number ("0.995" becomes "nine hundred ninety-five"). So: drop the commas,
    move currency after the amount, and spell fractional digits one by one.
    Version strings such as 0.7.1 are left alone.
    """
    text = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", text)
    text = re.sub(r"\$(\d+(?:\.\d+)?)", r"\1 dollars", text)

    def decimal(m):
        return m.group(1) + " point " + " ".join(DIGIT_WORDS[int(d)] for d in m.group(2))

    return re.sub(r"(?<![\d.])(\d+)\.(\d{2,})(?!\d|\.\d)", decimal, text)


def clean(text: str) -> str:
    for k, v in INLINE.items():
        text = text.replace(k, v)
    text = re.sub(r"\[\^[\w-]+\]", "", text)                    # footnote references
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]+)\)", r"\1", text)      # links keep their text
    text = re.sub(r"<https?://[^>]+>", "", text)                  # autolinks
    text = re.sub(r"\{[#.][^}]*\}", "", text)                     # pandoc attribute blocks
    text = text.replace("**", "").replace("*", "").replace("`", "")
    text = normalize_numbers(text)
    for rx, rep in PRON:
        text = rx.sub(rep, text)
    text = re.sub(r"(?<=[A-Za-z])_(?=[A-Za-z])", " ", text)       # snake_case identifiers
    text = text.replace("’", "'").replace("‘", "'").replace("—", ", ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    return text


def convert(path: Path, prefix, intro, outro):
    lines = path.read_text(encoding="utf-8").splitlines()
    if "<!-- narrate-from -->" in lines:
        lines = lines[lines.index("<!-- narrate-from -->") + 1:]
    paras = list(intro)
    counts = Counter()
    used = set()
    buf = []
    skip_italic = False      # an italic table/figure note follows the element it annotates

    def say(kind):
        counts[kind] += 1
        key = (prefix, kind, counts[kind])
        if key not in SAY:
            raise SystemExit("%s: no spoken version for %s" % (path.name, key))
        used.add(key)
        paras.append(SAY[key])

    def flush():
        nonlocal buf, skip_italic
        if not buf:
            return
        raw = " ".join(x.strip() for x in buf).strip()
        buf = []
        if skip_italic and raw.startswith("*") and raw.endswith("*"):
            skip_italic = False
            return
        skip_italic = False
        m = re.match(r"^\*\*(\d+)\. ", raw)
        if m:
            raw = "Step %s. %s" % (STEP_WORDS[int(m.group(1))], raw[m.end():])
        text = clean(raw)
        if text:
            paras.append(text)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("[^"):
            break                                            # footnote definitions start
        if line.startswith("```"):
            flush()
            i += 1
            while i < n and not lines[i].startswith("```"):
                i += 1
            i += 1
            say("code")
            continue
        if line.strip() == "$$":
            flush()
            i += 1
            while i < n and lines[i].strip() != "$$":
                i += 1
            i += 1
            say("math")
            continue
        if line.startswith("|"):
            flush()
            while i < n and lines[i].startswith("|"):
                i += 1
            say("table")
            skip_italic = True
            continue
        if line.startswith("![]("):                          # a mindmap: read its recap
            flush()
            key = re.search(r"map-([\w]+)\.png", line).group(1)
            paras.append(clean(mindmaps.spoken(key)))
            i += 1
            continue
        if line.startswith("!["):
            flush()
            i += 1
            say("figure")
            continue
        if line.startswith(("<!--", "\\")):                  # comments and raw LaTeX lines
            i += 1
            continue
        if line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            heading = clean(line.lstrip("#").strip())
            if level == 1 and heading.startswith(("Chapter ", "Appendix ")):
                heading = re.sub(r"^(Chapter|Appendix) (\w+)\. ", r"\1 \2. ", heading)
            if not heading.endswith((".", "?", "!")):
                heading += "."
            paras.append(heading)
            i += 1
            continue
        if re.match(r"^\s*(?:[-*] |\d+\. )", line):
            flush()
            item = re.sub(r"^\s*(?:[-*] |\d+\. )", "", line)
            i += 1
            while i < n and lines[i].startswith("  ") and lines[i].strip():
                item += " " + lines[i].strip()
                i += 1
            text = clean(item)
            if text:
                paras.append(text)
            continue
        if not line.strip() or line.strip() == "---":
            flush()
            i += 1
            continue
        buf.append(line)
        i += 1
    flush()
    paras.extend(outro)
    unused = [k for k in SAY if k[0] == prefix and k not in used]
    if unused:
        raise SystemExit("%s: spoken entries with no matching element: %r" % (path.name, unused))
    return paras


def main():
    OUT.mkdir(exist_ok=True)
    total_words = 0
    index = []
    for num, slug, path, prefix, intro, outro, title_override in TRACKS:
        paras = convert(path, prefix, intro, outro)
        text = "\n\n".join(paras) + "\n"
        name = "%02d-%s.txt" % (num, slug)
        (OUT / name).write_text(text, encoding="utf-8", newline="\n")
        words = len(text.split())
        total_words += words
        # Track title: the source file's first heading, without pandoc attributes.
        if title_override:
            title = title_override
        else:
            first = next(l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("# "))
            title = re.sub(r"\{[^}]*\}", "", first[2:]).strip()
        index.append({"id": "ch%02d" % num, "n": num, "file": name, "title": title})
        print("%02d-%-11s %5d words  ~%4.1f min" % (num, slug, words, words / 150))
    produced = {t["file"] for t in index}
    for old in OUT.glob("*.txt"):
        if old.name not in produced:
            old.unlink()          # stale scripts only; current ones are overwritten in place
    (OUT / "tracks.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    print("total %d words, ~%.0f minutes at 150 wpm" % (total_words, total_words / 150))


if __name__ == "__main__":
    main()
