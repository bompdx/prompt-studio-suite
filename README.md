# Prompt Studio Suite

Ten standalone prompt workbenches for paid traffic, coaching and
consulting, content creation, course building, ecommerce, email
marketing, launch campaigns, memberships, offers, and social media.

The collection includes 480 guided workflows and 60 advisor modes.
Each studio stores its business profile and prompt manual in the local
browser. There is no API or server-side application.

## Open the suite

The hosted collection is published with GitHub Pages from the
`gh-pages` branch. Open `dist/index.html` to run it locally.

## Project structure

- `data/` contains the inspectable content and prompt specifications.
- `build/studio-template.html` contains the shared interface and prompt engine.
- `build/build_studio.py` validates and builds a studio.
- `build/build_suite_index.py` builds the collection launcher.
- `dist/` contains the finished standalone pages.
- `docs/prompt-architecture.md` documents the back-end prompt contract.

## Rebuild

```bash
for file in data/[0-9][1-9]-*.json data/10-social-media.json; do
  python3 build/build_studio.py "$file"
done
python3 build/build_suite_index.py
```

Every studio is a single HTML file with no third-party JavaScript.
