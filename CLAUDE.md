# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a lecture course website for "Bussysteme" (Bus Systems / Building Automation) at MCI, built with MkDocs. Content covers building automation, PLCs, control engineering, bus systems, and smart metering.

## Commands

Dependencies are managed with PDM (Python 3.12):

```bash
pdm install          # Install dependencies into .venv
```

Serve the site locally:
```bash
python -m mkdocs serve -a 127.0.0.1:7000
# or use the configured default address:
python -m mkdocs serve   # listens on 0.0.0.0:7000
```

Deploy to GitHub Pages:
```bash
python -m mkdocs gh-deploy
```

## Architecture

- **`docs/`** — All lecture content as Markdown files, served by MkDocs
  - Files are numbered by chapter/section (e.g. `5_2_Buszugriffsverfahren.md`)
  - Each `.md` file has a Marp frontmatter (`marp: true`, `theme: beams`) — these are dual-purpose: slide decks via Marp and web pages via MkDocs
  - `index.md` is the course overview/homepage
  - `docs/images/` — Images used in slides
  - `docs/javascripts/mathjax.js` — MathJax config for LaTeX math rendering
- **`mkdocs.yml`** — Site config: navigation, theme (`readthedocs`), plugins, and markdown extensions
- **`Aufgaben/`** — Exercise files organized by topic (subdirectories like `2_1_1`, `3_2_3`, etc.)
- **`Klausur/`** — Exam materials (Word docs, Multiple Choice markdown)

## Key Configuration

- **Password protection**: The `encryptcontent` plugin protects all pages with password `mci_!!!` (configured in `mkdocs.yml`)
- **Math**: LaTeX rendered via MathJax using `pymdownx.arithmatex`; inline with `\(...\)`, block with `\[...\]`
- **Code blocks**: `pymdownx.superfences` enables indented/fenced code blocks with syntax highlighting
- **Snippets**: `pymdownx.snippets` allows including content from other files
- **Navigation**: Defined explicitly in `mkdocs.yml` under `nav:`; adding a new page requires updating this list
