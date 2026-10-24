#!/usr/bin/env python3
"""Import the Cabbage opcode pages from cabbageaudio.com into the manual.

Each page listed under /docs/opcodes/ in the site map is converted to a
docs/opcodes/<name>.md article, full CSD examples go to docs/examples/ and
docs/cabbage/cabbage.md lists the opcodes by category. Requires pandoc.
Run parse_data_to_lsp/to_parse.py afterwards to refresh the LSP data.
"""

import argparse
import html
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request


BASE = "https://cabbageaudio.com"
SITEMAP = BASE + "/sitemap-0.xml"

# Categories must also be listed in categories.py.
CATEGORY_ORDER = ["Widgets", "JSON", "Files and State", "ARA"]
FILES_AND_STATE = {"cabbageLoadState", "cabbageSaveState", "cabbageCreateFileName", "cabbageGetFiles"}

INTRO = """\
[Cabbage](https://cabbageaudio.com) ships with a number of opcodes that provide an interface to each widget's underlying JSON object. Any property of a widget's `props` member can be accessed or modified using the [cabbageGet](../opcodes/cabbageGet.md)/[cabbageSet](../opcodes/cabbageSet.md) opcodes. A widget's value can be queried and set using the [cabbageGetValue](../opcodes/cabbageGetValue.md) and [cabbageSetValue](../opcodes/cabbageSetValue.md) opcodes. A number of utility opcodes are also included.

These opcodes are only available when running Csound inside Cabbage. See the [Cabbage documentation](https://cabbageaudio.com/docs/opcodes/overview/) for details.
"""


def category(name):
    if name.startswith("cabbageAra"):
        return "ARA"
    if name.startswith("cabbageJson"):
        return "JSON"
    if name in FILES_AND_STATE:
        return "Files and State"
    return "Widgets"


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def load_pages(cache):
    """Return {slug: html} for every opcode page, from the site or a local cache."""
    if cache:
        return {p.stem: p.read_text(encoding="utf-8") for p in sorted(Path(cache).glob("*.html")) if p.stem != "overview"}
    urls = re.findall(r"<loc>([^<]*/docs/opcodes/[^<]+)</loc>", fetch(SITEMAP))
    pages = {}
    for url in urls:
        slug = url.rstrip("/").rsplit("/", 1)[1]
        if slug != "overview":
            pages[slug] = fetch(url)
    return pages


def code_text(block):
    lines = []
    for line in re.findall(r'<div class="code">(.*?)</div></div>', block, re.S):
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(html.unescape(line).rstrip())
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def blockquote_notes(md):
    """Turn the ADMON marker paragraphs left in blockquotes into a bold title."""
    out = []
    for line in md.split("\n"):
        m = re.match(r"^> ADMON\\?\|(\w+)\\?\|(.*)$", line)
        out.append(f"> **{m.group(2).strip()}**" if m else line)
    return "\n".join(out)


def convert(slug, page, names, examples_dir):
    """Return the markdown article for one opcode page; write its CSD examples."""
    name = names[slug]
    body = re.search(r'<div class="sl-markdown-content">(.*?)<footer', page, re.S).group(1)
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<link[^>]*>", "", body, flags=re.S)
    body = re.sub(r'<a class="sl-anchor-link".*?</a>', "", body, flags=re.S)

    # Code blocks are replaced by markers and written back after pandoc,
    # which would otherwise drop their titles.
    blocks = []

    def code_marker(m):
        block = m.group(0)
        title = re.search(r'<span class="title">(.*?)</span>', block)
        lang = re.search(r'data-language="([^"]*)"', block)
        blocks.append({
            "title": html.unescape(title.group(1)).strip() if title else "",
            "lang": lang.group(1) if lang else "",
            "code": code_text(block),
        })
        return f"<p>CODEBLOCK{len(blocks) - 1}X</p>"

    body = re.sub(r'<div class="expressive-code[^"]*">.*?</figure>\s*</div>', code_marker, body, flags=re.S)

    def note(m):
        kind, inner = m.group(1), m.group(2)
        title = re.search(r'<p class="starlight-aside__title"[^>]*>(.*?)</p>', inner, re.S)
        title = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else kind.title()
        content = re.search(r'<div class="starlight-aside__content">(.*)</div>', inner, re.S).group(1)
        return f"<blockquote><p>ADMON|{kind}|{html.escape(title)}</p>{content}</blockquote>"

    body = re.sub(r'<aside[^>]*starlight-aside--(\w+)[^>]*>(.*?)</aside>', note, body, flags=re.S)

    def link(m):
        href = html.unescape(m.group(1))
        opcode = re.match(r"^/docs/opcodes/([a-z]+)/?(#.*)?$", href)
        if opcode and opcode.group(1) in names:
            href = f"../opcodes/{names[opcode.group(1)]}.md" + (opcode.group(2) or "")
        elif href.startswith("/"):
            href = BASE + href
        return f'href="{html.escape(href)}"'

    body = re.sub(r'href="([^"]*)"', link, body)

    md = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
        input=body, capture_output=True, text=True, check=True,
    ).stdout
    md = blockquote_notes(md)
    md = re.sub(r"^## Examples?:?\s*$", "## Examples", md, flags=re.M)
    md = re.sub(r"^## See Also\s*$", "## See also", md, flags=re.M)

    used = set()
    syntax_done = False
    section = ""
    out = []
    for line in md.split("\n"):
        if line.startswith("## "):
            section = line[3:].strip()
        m = re.fullmatch(r"CODEBLOCK(\d+)X", line.strip())
        if not m:
            out.append(line)
            continue
        block = blocks[int(m.group(1))]
        code = block["code"]
        if section == "Syntax" and not syntax_done:
            # The first synopsis is the one to_parse.py reads for the LSP.
            syntax_done = True
            out.append('=== "Modern"')
            out.append("    ``` csound-orc")
            out += ["    " + c if c.strip() else "" for c in code.split("\n")]
            out.append("    ```")
        elif "<CsoundSynthesizer>" in code:
            base = block["title"] if block["title"].endswith(".csd") else f"{name}.csd"
            fname, k = base, 2
            while fname in used:
                fname = f"{base[:-4]}-{k}.csd"
                k += 1
            used.add(fname)
            (examples_dir / fname).write_text(code + "\n", encoding="utf-8")
            if out and out[-1].strip():
                out.append("")
            out.append(f"Here is an example of the {name} opcode. It uses the file [{fname}](../examples/{fname}).")
            out.append("")
            out.append(f'``` csound-csd title="Example of the {name} opcode." linenums="1"')
            out.append(f'--8<-- "examples/{fname}"')
            out.append("```")
        else:
            lang = {"csound": "csound-orc", "js": "javascript"}.get(block["lang"], block["lang"])
            title = f' title="{block["title"]}"' if block["title"] else ""
            out.append(f"``` {lang}{title}".rstrip())
            out += code.split("\n")
            out.append("```")
    md = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"

    header = f"<!--\nid:{name}\ncategory:Cabbage:{category(name)}\n-->\n# {name}\n"
    credits = f"\n## Credits\n\nFrom the [Cabbage documentation]({BASE}/docs/opcodes/{slug}/).\n"
    return header + md + credits


def write_category_page(names, path):
    by_cat = {}
    for name in sorted(names):
        by_cat.setdefault(category(name), []).append(name)
    lines = ["# **Cabbage Opcodes**", "", INTRO]
    for cat in CATEGORY_ORDER:
        lines += [f"## {cat}", ""]
        lines += [f"- [{n}](../opcodes/{n}.md)" for n in by_cat.get(cat, [])]
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="manual repository root")
    parser.add_argument("--pages", type=Path, help="directory of already downloaded <slug>.html pages, instead of the site")
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        sys.exit("pandoc is required: https://pandoc.org/installing.html")

    docs = args.root / "docs"
    pages = load_pages(args.pages)
    names = {slug: html.unescape(re.search(r'<h1 id="_top"[^>]*>(.*?)</h1>', page).group(1)).strip() for slug, page in pages.items()}

    for slug, page in pages.items():
        md = convert(slug, page, names, docs / "examples")
        (docs / "opcodes" / f"{names[slug]}.md").write_text(md, encoding="utf-8")
        print(f"{slug} -> opcodes/{names[slug]}.md ({category(names[slug])})")
    write_category_page(names.values(), docs / "cabbage" / "cabbage.md")
    print(f"Imported {len(pages)} Cabbage opcodes.")


if __name__ == "__main__":
    main()
