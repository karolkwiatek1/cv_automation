# CV Builder

Modular CV generation from Markdown templates using Pandoc + LaTeX.

## Usage

```bash
# Full CV in Polish (default)
python3 script.py header.md PROJECTS project1.md project2.md project3.md EDUCATION education.md SKILLS skills.md

# Full CV in English
python3 script.py --lang eng header.md PROJECTS ... EDUCATION education.md SKILLS skills.md

# Select specific projects only
python3 script.py --lang eng header.md PROJECTS project1.md project2.md EDUCATION education.md

# Custom output filename (add .pdf at the end)
python3 script.py --lang pl header.md PROJECTS ... cv.pdf
```

## Structure

```
automation/
├── script.py             # entry point
├── templates_pl/         # Polish templates
├── templates_eng/        # English templates
└── README.md

cv-template.tex           # LaTeX template (shared)
merge-raw.lua             # Pandoc Lua filter (shared)
```

## Requirements

- [Pandoc](https://pandoc.org/) 3.x
- LaTeX (pdfTeX) with packages: `fontawesome5`, `FiraMono`, `tgheros`, `titlesec`, `enumitem`, `fancyhdr`, `babel`, `tabularx`, `hyperref`, `contour`, `ulem`
