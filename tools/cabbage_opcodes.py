#!/usr/bin/env python3
"""Import the Cabbage opcode pages from the cabbageaudio.com sources into the manual.

The pages are read from src/content/docs/docs/opcodes/ in the site repository
(https://github.com/nodro7/cabbageaudio.com), either from GitHub or from a local
checkout. Each page becomes a docs/opcodes/<name>.md article, the examples it
shows are copied from public/examples/ to docs/examples/ and
docs/cabbage/cabbage.md lists the opcodes by category.
Run parse_data_to_lsp/to_parse.py afterwards to refresh the LSP data.
"""

import argparse
import json
import os
from pathlib import Path
import re
import urllib.request


BASE = "https://cabbageaudio.com"
REPO = "nodro7/cabbageaudio.com"
OPCODES_DIR = "src/content/docs/docs/opcodes"
EXAMPLES_DIR = "public/examples"

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
    request = urllib.request.Request(url)
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        # Avoids the unauthenticated rate limit shared by CI runners.
        request.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


class Source:
    """The site sources, from a local checkout or from GitHub at a given ref."""

    def __init__(self, checkout, ref):
        self.checkout = checkout
        self.ref = ref

    def pages(self):
        """Return {slug: text} for every opcode page."""
        if self.checkout:
            files = sorted((self.checkout / OPCODES_DIR).glob("*.md*"))
            pages = {p.name.split(".")[0]: p.read_text(encoding="utf-8") for p in files}
        else:
            listing = json.loads(fetch(f"https://api.github.com/repos/{REPO}/contents/{OPCODES_DIR}?ref={self.ref}"))
            pages = {
                entry["name"].split(".")[0]: fetch(entry["download_url"])
                for entry in listing
                if entry["type"] == "file" and re.search(r"\.mdx?$", entry["name"])
            }
        pages.pop("overview", None)
        return pages

    def example(self, name):
        if self.checkout:
            # Raw bytes: some examples end lines with \r\r\n, which read_text() would double.
            return (self.checkout / EXAMPLES_DIR / f"{name}.csd").read_bytes().decode("utf-8")
        return fetch(f"https://raw.githubusercontent.com/{REPO}/{self.ref}/{EXAMPLES_DIR}/{name}.csd")


def front_matter(page):
    """Split the YAML front matter from the page; return ({key: value}, body)."""
    m = re.match(r"---\n(.*?)\n---\n", page, re.S)
    if not m:
        return {}, page
    meta = {}
    for line in m.group(1).split("\n"):
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, page[m.end():]


def convert(slug, page, names, source, examples_dir):
    """Return the markdown article for one opcode page; write the examples it shows."""
    _, body = front_matter(page)
    name = names[slug]

    def link(m):
        text, href = m.group(1), m.group(2)
        opcode = re.match(r"^/docs/opcodes/([a-z]+)/?(#.*)?$", href)
        if opcode and opcode.group(1) in names:
            href = f"../opcodes/{names[opcode.group(1)]}.md" + (opcode.group(2) or "")
        elif href.startswith("/"):
            href = BASE + href
        return f"[{text}]({href})"

    syntax_done = False
    in_note = False
    section = ""
    fence = None
    out = []
    for line in body.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if fence is not None:
            out.append(fence + line if line.strip() else "")
            if stripped.startswith("```"):
                fence = None
            continue
        if stripped.startswith("```"):
            lang = {"csound": "csound-orc", "js": "javascript"}.get(stripped[3:].strip(), stripped[3:].strip())
            if section == "Syntax" and not syntax_done:
                # The first synopsis is the one to_parse.py reads for the LSP.
                syntax_done = True
                out += ['=== "Modern"', "    ``` csound-orc"]
                fence = "    "
            else:
                out.append(f"``` {lang}".rstrip())
                fence = ""
            continue
        if stripped.startswith("import "):
            continue
        if stripped.startswith(":::"):
            # Starlight asides, e.g. ":::note[Title]" ... ":::", become quoted notes.
            m = re.match(r":::(\w+)(?:\[(.*)\])?", stripped)
            in_note = bool(m)
            if m:
                out += [f"> **{m.group(2) or m.group(1).title()}**", ">"]
            continue
        example = re.fullmatch(r'<ExampleCode\s+name="([^"]+)"\s*/>', stripped)
        if example:
            fname = f"{example.group(1)}.csd"
            code = [l.rstrip() for l in re.split(r"\r*\n|\r", source.example(example.group(1)))]
            (examples_dir / fname).write_text("\n".join(code).strip("\n") + "\n", encoding="utf-8")
            out.append(f"Here is an example of the {name} opcode. It uses the file [{fname}](../examples/{fname}).")
            out.append("")
            out.append(f'``` csound-csd title="Example of the {name} opcode." linenums="1"')
            out.append(f'--8<-- "examples/{fname}"')
            out.append("```")
            continue
        heading = re.match(r"(#{2,6}) (.*)", line)
        if heading:
            title = heading.group(2).strip().rstrip(":")
            if heading.group(1) == "##":
                section = title = {"Example": "Examples", "See Also": "See also"}.get(title, title)
            if out and out[-1]:
                out.append("")
            out += [f"{heading.group(1)} {title}", ""]
            continue
        line = re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", link, line.rstrip())
        # Python-Markdown needs a blank line between a paragraph and a list.
        if re.match(r"\s*([*-]|\d+\.) ", line) and out and out[-1].strip() and not re.match(r"[\s>]*([*-]|\d+\.) ", out[-1]):
            out.append(">" if in_note else "")
        out.append(f"> {line}".rstrip() if in_note else line)
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
    parser.add_argument("--src", type=Path, help="local checkout of the cabbageaudio.com repository, instead of GitHub")
    parser.add_argument("--ref", default="main", help="branch, tag or commit to read from GitHub (default: main)")
    args = parser.parse_args()

    docs = args.root / "docs"
    source = Source(args.src, args.ref)
    pages = source.pages()
    names = {slug: front_matter(page)[0]["title"] for slug, page in pages.items()}

    for slug, page in sorted(pages.items()):
        md = convert(slug, page, names, source, docs / "examples")
        (docs / "opcodes" / f"{names[slug]}.md").write_text(md, encoding="utf-8")
        print(f"{slug} -> opcodes/{names[slug]}.md ({category(names[slug])})")
    write_category_page(names.values(), docs / "cabbage" / "cabbage.md")
    print(f"Imported {len(pages)} Cabbage opcodes.")


if __name__ == "__main__":
    main()
