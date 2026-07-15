#!/usr/bin/env python3
"""Validate a Prompt Studio data bank and build its standalone HTML file.

Usage:
    python3 build_studio.py <studio.json> [--out <dir-or-file.html>] [--lint-only]

Schema and copy rules: ../docs/prompt-architecture.md
"""
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "studio-template.html"

BANNED_WORDS = [
    "delve", "intricate", "tapestry", "interplay", "foster", "garner",
    "underscore", "pivotal", "showcase", "enduring", "landscape", "robust",
    "seamless", "leverage", "unlock", "elevate", "transformative", "dynamic",
    "essential", "compelling", "quietly",
]

FIELD_TYPES = {"text", "textarea", "select"}


def walk_strings(node, path="$"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from walk_strings(item, f"{path}[{i}]")
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, f"{path}.{key}")


def check_field(field, where, errors):
    for key in ("id", "label", "type"):
        if not field.get(key):
            errors.append(f"{where}: field missing '{key}'")
    if field.get("type") not in FIELD_TYPES:
        errors.append(f"{where}: field '{field.get('id')}' has bad type {field.get('type')!r}")
    if field.get("type") == "select" and not field.get("options"):
        errors.append(f"{where}: select field '{field.get('id')}' has no options")


def lint(data):
    errors, warnings = [], []

    for key in ("slug", "title", "kicker", "subtitle", "badge", "accent",
                "accent2", "footer", "profile", "categories", "workflows", "advisors"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")
    if errors:
        return errors, warnings

    if not (4 <= len(data["profile"]) <= 5):
        errors.append(f"profile has {len(data['profile'])} fields, want 4-5")
    if data["profile"] and not data["profile"][0].get("required"):
        errors.append("first profile field must be required")
    for f in data["profile"]:
        check_field(f, f"profile.{f.get('id')}", errors)

    if len(data["categories"]) != 6:
        errors.append(f"{len(data['categories'])} categories, want 6")
    cat_ids = [c.get("id") for c in data["categories"]]
    if len(set(cat_ids)) != len(cat_ids):
        errors.append("duplicate category ids")
    for c in data["categories"]:
        if not c.get("title") or not c.get("note"):
            errors.append(f"category '{c.get('id')}' missing title or note")

    if len(data["workflows"]) != 48:
        errors.append(f"{len(data['workflows'])} workflows, want 48")
    per_cat = {cid: 0 for cid in cat_ids}
    wf_ids = set()
    for wf in data["workflows"]:
        wid = wf.get("id", "?")
        where = f"workflow '{wid}'"
        if wid in wf_ids:
            errors.append(f"{where}: duplicate id")
        wf_ids.add(wid)
        if wf.get("category") not in per_cat:
            errors.append(f"{where}: unknown category {wf.get('category')!r}")
        else:
            per_cat[wf["category"]] += 1
        for key in ("title", "description", "role", "output"):
            if not wf.get(key):
                errors.append(f"{where}: missing '{key}'")
        fields = wf.get("fields", [])
        if not (1 <= len(fields) <= 4):
            errors.append(f"{where}: {len(fields)} fields, want 1-4")
        for f in fields:
            check_field(f, where, errors)
        task = wf.get("task", [])
        if not (3 <= len(task) <= 6):
            errors.append(f"{where}: {len(task)} task steps, want 3-6")
        rules = wf.get("rules", [])
        if not (1 <= len(rules) <= 3):
            errors.append(f"{where}: {len(rules)} rules, want 1-3")
        role = wf.get("role", "")
        if role.lower().startswith(("an expert", "a expert", "expert")):
            warnings.append(f"{where}: role starts with 'expert', wants a specific persona")
    for cid, count in per_cat.items():
        if count != 8:
            errors.append(f"category '{cid}' has {count} workflows, want 8")

    if len(data["advisors"]) != 6:
        errors.append(f"{len(data['advisors'])} advisors, want 6")
    for adv in data["advisors"]:
        where = f"advisor '{adv.get('id', '?')}'"
        for key in ("title", "description", "role", "focus", "deliverable"):
            if not adv.get(key):
                errors.append(f"{where}: missing '{key}'")
        if not (2 <= len(adv.get("questions", [])) <= 5):
            errors.append(f"{where}: want 2-5 questions")

    banned_re = re.compile(r"\b(" + "|".join(BANNED_WORDS) + r")\w*\b", re.IGNORECASE)
    for path, text in walk_strings(data):
        if "—" in text or "–" in text:
            errors.append(f"{path}: contains an em/en dash: {text[:70]!r}")
        m = banned_re.search(text)
        if m:
            errors.append(f"{path}: banned word '{m.group(0)}': {text[:70]!r}")
        for expanded in (" do not ", " does not ", " did not ", " cannot ", " it is ", " you are not "):
            if expanded in " " + text.lower() + " ":
                warnings.append(f"{path}: expanded form '{expanded.strip()}', wants a contraction: {text[:60]!r}")

    return errors, warnings


def build(data, out_path):
    html = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, indent=None).replace("</", "<\\/")
    html = html.replace("/*__STUDIO_DATA__*/ null", payload)
    for placeholder, value in {
        "{{APP_TITLE}}": data["title"],
        "{{KICKER}}": data["kicker"],
        "{{SUBTITLE}}": data["subtitle"],
        "{{BADGE}}": data["badge"],
        "{{ACCENT}}": data["accent"],
        "{{ACCENT2}}": data["accent2"],
        "{{BRAND_OR_FOOTER}}": data["footer"],
    }.items():
        html = html.replace(placeholder, value)
    if "{{" in html:
        leftover = re.findall(r"\{\{[A-Z_2]+\}\}", html)
        raise SystemExit(f"unreplaced placeholders: {leftover}")
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    src = Path(args[0])
    data = json.loads(src.read_text(encoding="utf-8"))
    errors, warnings = lint(data)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        raise SystemExit(f"{src.name}: {len(errors)} errors, not building.")
    print(f"{src.name}: lint clean ({len(warnings)} warnings)")
    if "--lint-only" in args:
        return
    out = Path(__file__).parent.parent / "dist" / f"{data['slug']}-prompt-studio.html"
    if "--out" in args:
        target = Path(args[args.index("--out") + 1])
        out = target / f"{data['slug']}-prompt-studio.html" if target.is_dir() else target
    built = build(data, out)
    print(f"built {built}")


if __name__ == "__main__":
    main()
