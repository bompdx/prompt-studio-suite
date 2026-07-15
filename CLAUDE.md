# Prompt Studio Suite

Ten standalone prompt-generator micro apps, one per market: paid
traffic, coaching/consulting, content creators, course builders,
ecommerce, email marketing, launches, memberships, offers/sales pages,
social media. Inspired by the "AI Studio White Label Collection" at
prompttoolfactory.com/AIStudio, rebuilt from scratch in David's style.
All product names are working names David can rebrand.

Each studio: 48 guided workflows in 6 categories, 6 expert advisory
modes, a business profile injected into every prompt, and a prompt
manual the user can print to PDF. One HTML file per studio, no backend.

## Where things live

- `docs/prompt-architecture.md` — the contract: JSON schema, exact
  prompt-assembly templates (the back-end prompts), copy rules. Read
  this before touching anything.
- `docs/studio-briefs.md` — per-studio market briefs and coverage.
- `data/NN-slug.json` — one data bank per studio. This is where all
  user-visible copy and all prompt specs live. Edit content here,
  never in dist/.
- `build/studio-template.html` — the shared engine (UI + prompt
  assembly logic).
- `build/build_studio.py` — lints a data bank and builds its HTML:
  `python3 build/build_studio.py data/01-paid-traffic.json`
- `build/generate_remaining_studios.py` — inspectable source map for the
  coaching, email, and launch banks recovered after the interrupted build.
- `build/build_suite_index.py` — builds the collection launcher at
  `dist/index.html`.
- `build/serve_dist.js` — local static server for verification
  (launch config `prompt-studio-dist`, port 8741).
- `dist/` — built studios. Generated files; rebuild instead of editing.

## Finished output

A finished suite is ten lint-clean data banks, ten standalone HTML
studios, and the launcher at `dist/index.html`. Verify at desktop and
mobile widths: profile saves, search works, workflows validate and
assemble prompts, copy buttons work, advisor sessions build, and the
manual saves, reorders, prints, and downloads.

## Editing rules

- Change copy in the JSON, run the build script, verify.
- The lint enforces David's banned-word list and the no-em-dash rule
  across every string. Don't weaken the lint to make content pass.
- Template changes affect all ten studios: rebuild all data files
  after touching `studio-template.html`.
