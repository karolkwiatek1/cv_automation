#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_TEMPLATE = os.path.join(BASE_DIR, "base", "cv-template.tex")
MERGE_LUA = os.path.join(BASE_DIR, "base", "merge-raw.lua")
PANDOC = shutil.which("pandoc") or "/tmp/opencode/pandoc-3.1.11/bin/pandoc"

LANGS = {
    "pl": {
        "dir": "templates_pl",
        "headers": {
            "PROJECTS": "# PROJEKTY",
            "EDUCATION": "# EDUKACJA",
            "SKILLS": "# UMIEJĘTNOŚCI",
        },
    },
    "eng": {
        "dir": "templates_eng",
        "headers": {
            "PROJECTS": "# PROJECTS",
            "EDUCATION": "# EDUCATION",
            "SKILLS": "# SKILLS",
        },
    },
}

SECTION_PREFIX = {
    "PROJECTS": "\\resumeSubHeadingListStart",
}

SECTION_SUFFIX = {
    "PROJECTS": "\\resumeSubHeadingListEnd",
}


def build_markdown(args, lang_cfg):
    templates_dir = os.path.join(BASE_DIR, lang_cfg["dir"])
    headers = lang_cfg["headers"]

    def read_file(fpath):
        path = fpath if os.path.isabs(fpath) else os.path.join(templates_dir, fpath)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return fh.read().strip()
        return None

    lines = []
    current_section = None
    section_files = []

    def flush_section():
        nonlocal current_section, section_files
        if current_section is None:
            return
        prefix = SECTION_PREFIX.get(current_section, "")
        suffix = SECTION_SUFFIX.get(current_section, "")
        if prefix:
            lines.append(prefix)
        for f in section_files:
            content = read_file(f)
            if content:
                lines.append(content)
            else:
                print(f"Warning: file not found: {f}", file=sys.stderr)
        if suffix:
            lines.append(suffix)
        current_section = None
        section_files = []

    for arg in args:
        if arg in headers:
            flush_section()
            lines.append(headers[arg])
            current_section = arg
        else:
            if current_section:
                section_files.append(arg)
            else:
                content = read_file(arg)
                if content:
                    lines.append(content)
                else:
                    print(f"Warning: file not found: {arg}", file=sys.stderr)

    flush_section()
    return "\n\n".join(lines)


def main():
    args = sys.argv[1:]

    lang = "pl"
    output_pdf = "cv.pdf"

    cleaned = []
    skip_next = False
    for i, a in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if a == "--lang" and i + 1 < len(args):
            lang = args[i + 1]
            skip_next = True
        elif a.startswith("--lang="):
            lang = a.split("=", 1)[1]
        elif a.endswith(".pdf"):
            output_pdf = a
        else:
            cleaned.append(a)

    if lang not in LANGS:
        print(f"Error: unknown language '{lang}'. Supported: {', '.join(LANGS)}", file=sys.stderr)
        sys.exit(1)

    lang_cfg = LANGS[lang]

    if not cleaned:
        print(f"Usage: python3 script.py [--lang pl|eng] header.md [PROJECTS file.md ...] [output.pdf]")
        sys.exit(1)

    body = build_markdown(cleaned, lang_cfg)

    tmpdir = tempfile.mkdtemp()
    try:
        md_path = os.path.join(tmpdir, "body.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(body)

        template = CV_TEMPLATE
        if not os.path.exists(template):
            template = os.path.join(BASE_DIR, "..", "cv-template.tex")

        merge_lua = MERGE_LUA
        if not os.path.exists(merge_lua):
            merge_lua = os.path.join(BASE_DIR, "..", "merge-raw.lua")

        cmd = [
            PANDOC,
            "--from", "markdown+raw_tex-smart",
            "--lua-filter", merge_lua,
            "--template", template,
            "-o", output_pdf,
            md_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Pandoc error:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
        print(f"PDF generated: {os.path.abspath(output_pdf)}")
    finally:
        shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
