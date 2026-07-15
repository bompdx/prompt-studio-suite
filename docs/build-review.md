# Prompt Studio Suite Build Review

## Finished product

The collection contains ten standalone browser studios plus a suite
launcher. Each studio contains 48 guided workflows, six category
groups, six ongoing advisor modes, a saved business profile, and a
prompt manual that prints to PDF or downloads as HTML.

The ten markets are paid traffic, coaching and consulting, content
creation, course building, ecommerce, email marketing, launch
campaigns, memberships and communities, offers and sales pages, and
social media.

## What each form produces

Workflow forms assemble a prompt in this fixed order:

1. A specific professional role with a stated responsibility.
2. The saved business profile and the workflow's current inputs.
3. Pasted working material when the workflow reviews an existing draft.
4. Three to six concrete task steps.
5. Workflow-specific rules plus the suite's truth and plain-language rules.
6. A named output shape the user can judge.
7. A final instruction to ask up to three questions when the context is too thin.

Advisor forms assemble a session prompt that keeps the same business
profile, assigns a standing role, interviews the user one question at
a time, produces a defined advisory deliverable, and stays in role for
follow-up questions.

The exact assembly templates and JSON contracts live in
`prompt-architecture.md`. Every workflow's role, fields, task steps,
rules, and output shape remain readable in its `data/NN-slug.json`
source bank.

## Interface direction

The finished interface uses a focused workbench model: a compact
product bar, a clear three-step path, saved-context progress, searchable
workflow cards, category filters, distinct prompt output surfaces, and
an integrated manual. Light and dark themes share the same semantic
tokens. Motion is limited to short entrance and interaction feedback,
and reduced-motion preferences are respected.

The suite launcher gives the ten standalone files one entry point
without creating a backend or coupling the studios together.

## Verification result

- Ten source banks: 48 workflows, six categories, six advisors each.
- All source banks pass the schema and copy lint with zero warnings.
- All ten studios load without browser errors.
- Required-field validation, prompt assembly, workflow search, advisor
  prompts, theme switching, and manual saving were exercised in Chrome.
- The flagship studio was checked at 1440 pixels and 375 pixels.
- No horizontal overflow was found at the phone width.
- Workflow and advisor prompts include every required back-end section.

## Scope note

The current Prompt Tool Factory public site no longer exposes the
original AI Studio product page. This suite is an original build in the
same broad prompt-tool category. It doesn't copy proprietary prompts,
code, protected member content, or branding.
