# Prompt Studio Suite — Prompt Architecture

Working name for the suite: **Prompt Studio** (one studio per market,
ten studios total). Inspired by the "AI Studio White Label Collection"
at prompttoolfactory.com, rebuilt from scratch in David's style:
practical, concrete, no hype. All names are placeholders David can
rebrand.

Each studio is one standalone HTML file. No backend, no API keys. The
studio collects context, the user picks a workflow, fills that
workflow's fields, and the studio assembles a finished prompt the user
copies into ChatGPT, Claude, or any other assistant.

This document is the contract for every studio's data bank. The build
script (`build/build_studio.py`) injects a studio's JSON into the
shared template (`build/studio-template.html`) and refuses JSON that
breaks the schema.

## What one studio contains

- **Business profile**: 4 to 5 context fields the user fills once.
  Saved to localStorage. Injected into every generated prompt.
- **48 workflows** in 6 categories of 8. Each workflow is a small form
  plus a back-end prompt spec (role, task, rules, output).
- **6 advisory modes**: expert personas that generate a session-setup
  prompt turning the AI into an ongoing advisor that interviews the
  user one question at a time.
- **Prompt manual**: every generated prompt can be saved into a
  manual the user reorders and prints to PDF (browser print) or
  downloads as an HTML file.

## Studio JSON schema

```json
{
  "slug": "paid-traffic",
  "title": "Paid Traffic Prompt Studio",
  "kicker": "Guided prompt system for paid media",
  "subtitle": "One or two sentences saying who this is for and what it produces. Concrete, no hype.",
  "badge": "48 guided workflows",
  "accent": "#1f7a5a",
  "accent2": "#d6a11f",
  "footer": "Prompt Studio",
  "profile": [
    {
      "id": "business",
      "label": "What you sell and who buys it",
      "type": "textarea",
      "required": true,
      "placeholder": "Example: online course for wedding photographers, $497, sold through Instagram ads",
      "helper": "One or two sentences. Every prompt in this studio uses this."
    }
  ],
  "categories": [
    { "id": "strategy", "title": "Campaign Strategy", "note": "One line on what this group of workflows decides." }
  ],
  "workflows": [ ... 48 workflow objects ... ],
  "advisors": [ ... 6 advisor objects ... ]
}
```

Profile field rules: first profile field is always required, the rest
optional. Field `type` is `text`, `textarea`, or `select` (with
`options`). Blank optional fields are left out of generated prompts.

## Workflow object schema

```json
{
  "id": "traffic-north-star",
  "category": "strategy",
  "title": "Traffic North Star",
  "description": "What this workflow decides or produces, in one sentence a media buyer would recognize.",
  "role": "a senior paid-media strategist who plans campaigns for direct-response offers and gets judged on cost per acquisition, not impressions",
  "fields": [
    {
      "id": "budget",
      "label": "Monthly ad budget",
      "type": "text",
      "required": true,
      "placeholder": "Example: $3,000/month",
      "helper": ""
    }
  ],
  "task": [
    "Name the single conversion action this campaign should be judged on, and say why the alternatives are weaker for this offer.",
    "Write the campaign objective as one sentence a media buyer could read before touching the ad account."
  ],
  "rules": [
    "Work only from the context I gave you. Where you assume something, flag the assumption in one line.",
    "Skip generic ad advice. Every recommendation has to reference my offer, my audience, or my budget."
  ],
  "output": "a one-page campaign direction memo with sections for objective, conversion action, buyer motivation, message direction, and the three biggest performance risks"
}
```

Constraints per workflow:

- `fields`: 1 to 4 fields beyond the profile. Only ask for inputs the
  prompt actually uses. Review-and-improve workflows (the
  "-in-Chief" pattern) use one required `textarea` with id `material`
  for the pasted draft.
- `role`: a specific persona with a stated accountability, not "an
  expert marketer."
- `task`: 3 to 6 numbered steps. Each step is one concrete
  instruction.
- `rules`: 1 to 3 workflow-specific rules. The template adds shared
  rules automatically; don't repeat them.
- `output`: the shape of the deliverable, specific enough that the
  user can tell whether the AI followed it.

## The assembled workflow prompt (the back end)

The engine builds this exact structure. `{...}` marks injected values.

```
You are {role}.

MY CONTEXT
- {Profile field label}: {value}      (each filled profile field)
- {Workflow field label}: {value}     (each filled workflow field)

WORK WITH THIS MATERIAL                (only if a `material` field exists)
---
{pasted draft}
---

YOUR TASK
1. {task step}
2. {task step}
...

RULES
- {workflow rule}
...
- Work from my context above. Don't invent numbers, results, or customer quotes I didn't give you.
- Plain language. No hype words, no filler sentences, no advice so generic it would fit any business.

OUTPUT
Give me {output}.

Before you start: if any part of my context is too thin to do this well, ask me up to 3 specific questions first, then produce the deliverable.
```

Shared rules (the last two RULES lines and the closing paragraph) live
in the template, not in the JSON. If a workflow's own `rules` would
duplicate them, cut the duplicate.

## Advisor object schema

```json
{
  "id": "roas-doctor",
  "title": "The ROAS Doctor",
  "description": "A diagnostic advisor for campaigns that spend money and return too little.",
  "role": "a paid-media diagnostician who has audited hundreds of underperforming ad accounts and starts from the numbers, not the creative",
  "focus": "finding why a live campaign underperforms and prescribing the fix order",
  "questions": [
    "current spend, ROAS, and the target that would make this campaign worth keeping",
    "where conversions drop: ad click-through, landing page, checkout, or follow-up"
  ],
  "deliverable": "a diagnosis of the most likely failure point, ranked next tests, and what to stop spending on this week"
}
```

## The assembled advisory prompt

```
You are {role}. Act as my ongoing advisor for {focus}.

MY CONTEXT
- {Profile field label}: {value}      (each filled profile field)

HOW THIS SESSION WORKS
Interview me before you advise. Ask one question at a time and wait
for my answer. Start with what you most need to know, including:
- {question}
- {question}

After you have enough to work with (usually 4 to 6 answers), give me
{deliverable}. Then stay in this role: I'll bring you follow-up
situations and you keep advising with the same standards.

RULES
- One question per message while interviewing.
- Don't invent numbers or facts I didn't give you. If you assume something, say so in one line.
- Plain language. No hype, no filler, no generic advice.
```

## Copy rules for every string in the JSON

The full rules live in `brain/voice/anti-ai-writing-style.md`. The
ones that get violated most:

- No banned words: delve, intricate, tapestry, interplay, foster,
  garner, underscore, pivotal, showcase, enduring, landscape, robust,
  seamless, leverage, unlock, elevate, transformative, dynamic,
  essential, compelling, quietly. Don't synonym-swap; rebuild the
  sentence around the concrete thing.
- Zero em dashes in UI strings and prompt specs.
- Contractions everywhere ("don't", not "do not") except inside
  numbered task steps where imperative verbs start the sentence.
- Every description passes the replace-with-[X] test: if you can swap
  the specifics out and the sentence still reads fine, it says
  nothing. Rewrite it.
- Placeholders show a real, lived example ("Example: abandoned-cart
  emails for a $58 skincare bundle"), never "Enter your details".
- No fake urgency, no income claims, no "secret" framing.

## Sizing

48 workflows per studio, 8 per category, 6 categories. 6 advisors.
4 to 5 profile fields. Workflow titles stay under 5 words where
possible and name the artifact or decision, not the vibe.
