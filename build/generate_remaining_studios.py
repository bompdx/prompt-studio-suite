#!/usr/bin/env python3
"""Generate the three studio banks that were missing from the interrupted build.

The content map below is intentionally inspectable. Each line defines one form's
job and the prompt engine turns that job into a role, context fields, task steps,
rules, and a named output.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def items(block):
    rows = []
    for line in block.strip().splitlines():
        title, job = [part.strip() for part in line.split("::", 1)]
        rows.append((title, job))
    return rows


COMMON_PROFILE = [
    ("business", "What you sell and who buys it", "textarea", True, "Example: a $3,000 operations advisory package for owner-led manufacturers with 20 to 100 employees", "One or two sentences. Every prompt in this studio uses this."),
    ("audience", "Your buyer in their own words", "textarea", False, "Example: 'We keep fixing the same fire every Friday' is how clients describe the problem", "Use phrases real buyers or clients say."),
    ("project", "The offer or project you're working on now", "textarea", False, "Example: rebuilding the spring group program before enrollment opens", ""),
    ("goal", "Your main goal for the next 90 days", "text", False, "Example: enroll 12 right-fit clients without adding more sales calls", ""),
    ("constraints", "Voice, proof, or constraints the AI should respect", "text", False, "Example: plainspoken, no income claims, two-person delivery team", ""),
]


STUDIOS = [
    {
        "number": "02", "slug": "coaching", "title": "Coaching & Consulting Prompt Studio",
        "kicker": "Guided prompt system for expert services", "accent": "#365f91", "accent2": "#d6a11f",
        "subtitle": "Built for coaches, consultants, and advisors who need sharper offers, better client sessions, and recommendations people can act on. Pick a job, add the facts, and copy the finished prompt into the assistant you use.",
        "categories": [
            ("positioning", "Positioning and Offers", "Turn experience into a clear reason to hire you.", "positioning strategist for expert services who must make the buyer, problem, and paid result unmistakable", "Describe the offer, expertise, or positioning you want to work on", "Example: I help dental groups reduce front-desk turnover through a 10-week advisory engagement"),
            ("sales", "Sales Conversations", "Diagnose fit before the conversation turns into a pitch.", "consultative sales director who reviews calls by diagnosis quality, next-step clarity, and fit", "Describe the prospect, conversation, or sales problem", "Example: owner agrees the problem is costly but keeps asking for a proposal before sharing numbers"),
            ("delivery", "Sessions and Delivery", "Make each client session produce a decision and a next move.", "client delivery lead who turns advisory time into decisions, owners, deadlines, and visible progress", "Describe the client situation or session goal", "Example: leadership team agrees on the issue but hasn't picked who owns the fix"),
            ("advisory", "Audits and Roadmaps", "Turn a messy business problem into ranked recommendations.", "management consultant accountable for evidence, tradeoffs, and an implementation order the client can defend", "Describe the business problem and evidence available", "Example: margins fell six points after sales grew, with labor and freight both rising"),
            ("retention", "Retention and Expansion", "Keep good clients moving without forcing an awkward upsell.", "client success director measured on adoption, renewal quality, and expansion that follows delivered value", "Describe the client relationship and current result", "Example: month five of a six-month retainer, two goals met, one delayed by hiring"),
            ("review", "Review and Improve", "Strengthen working material without losing the thinking already inside it.", "senior consulting editor who preserves sound thinking while fixing gaps, weak claims, and unclear next steps", "Paste the material you want reviewed", "Paste notes, a proposal, transcript, audit, or client message"),
        ],
        "workflows": [
            items("""
Expertise Position::identify the narrow expertise claim buyers can repeat and the evidence that supports it
Named Method Builder::turn the delivery process into a named sequence with clear stages and boundaries
Offer Definition::state who the engagement serves, what changes, what is included, and what falls outside scope
Niche Message Test::compare three niche messages against urgency, buying power, access, and proof
Problem to Promise::translate the costly client problem into a credible paid outcome without overclaiming
Service Package Map::organize deliverables, meetings, support, timing, and client responsibilities into one package
Pricing Logic Memo::build a defensible price argument from value, delivery cost, risk, and alternatives
Positioning Gap Scan::find where the current positioning sounds interchangeable and prescribe the first fixes
"""),
            items("""
Discovery Question Map::sequence questions that uncover symptoms, root causes, cost, urgency, and decision process
Client Readiness Score::score whether a prospect has the problem, authority, resources, and willingness to act
Objection Diagnosis::separate the stated objection from the unresolved risk or missing evidence behind it
Sales Call Run Sheet::build a call flow that diagnoses before recommending and ends with one honest next step
Proposal Decision Path::structure a proposal around the buyer's decision, proof needs, scope, and approval path
Price Conversation Script::explain the fee, test commitment, and respond to price pressure without becoming defensive
No Fit Referral::decline a poor-fit prospect clearly while preserving trust and pointing to a better route
Follow Up Sequence::write a short follow-up path tied to what the prospect said, not generic checking in
"""),
            items("""
Session Outcome Plan::define the decision, preparation, discussion sequence, and close for one client session
Breakthrough Questions::write questions that expose the assumption keeping the client stuck
Accountability Contract::set owners, deadlines, evidence of completion, and the response to missed commitments
Client Homework Brief::design useful between-session work with a purpose, time box, and completion standard
Decision Log::capture the decision, rationale, risks, owner, deadline, and review date
Group Hot Seat Plan::run a focused hot seat that gives one member depth without losing the rest of the room
Executive Session Brief::compress a complex situation into the few facts and choices leaders need in the room
Session Follow Up::turn session notes into decisions, assignments, open questions, and the next meeting agenda
"""),
            items("""
Root Cause Map::trace visible symptoms to operating causes and identify what evidence would confirm each link
Audit Evidence Plan::name the documents, interviews, numbers, and observations required before making recommendations
Recommendation Ranker::rank options by value, effort, risk, timing, and organizational readiness
Implementation Roadmap::sequence the work into phases with owners, dependencies, checkpoints, and stop conditions
Risk and Assumption Scan::surface what the recommendation assumes and what could make it fail
KPI Decision Board::choose a small set of measures that tell the client when to continue, adjust, or stop
Executive Summary::present the finding, business consequence, recommendation, and decision required on one page
First 30 Days::convert a broad recommendation into the first month of actions, meetings, proof, and decisions
"""),
            items("""
Renewal Evidence Pack::collect results, adoption, unfinished work, and next risks into a renewal conversation
Value Recap::show what changed, what the client used, and where value remains unclaimed
Scope Boundary Script::respond to extra requests by clarifying tradeoffs, included work, and paid options
Retainer Expansion::identify the next problem that naturally follows the work already completed
Referral Moment::choose when and how to ask for a specific introduction based on delivered value
Testimonial Interview::ask questions that produce a credible before, decision, experience, and after story
Client Risk Signal::spot stalled adoption, missing stakeholders, weak ownership, and other renewal risks early
Closeout Plan::end an engagement with decisions documented, ownership transferred, and a useful next review date
"""),
            items("""
Proposal in Chief::review a proposal for decision clarity, proof, scope, price logic, and friction
Call Transcript Review::find missed diagnosis, weak questions, premature pitching, and unclear next steps in a sales call
Session Notes Review::turn raw notes into decisions, commitments, open questions, and follow-up
Audit in Chief::challenge an audit's evidence, priorities, business consequences, and recommended order
Roadmap Stress Test::find hidden dependencies, overloaded phases, missing owners, and weak checkpoints
Client Email Review::make a client email clearer, firmer, and easier to act on without changing its intent
Framework Review::test whether a named method has real stages, decision rules, and a useful boundary
Advisory Material Review::strengthen a worksheet, briefing, or training aid around the decision it must help someone make
"""),
        ],
        "advisors": [
            ("positioning-partner", "The Positioning Partner", "Finds the claim buyers can understand and competitors can't easily borrow.", "a positioning consultant who tests every claim against buyer urgency, proof, and competitive sameness", "clarifying an expert service's strongest market position", ["the costly problem clients already admit", "the evidence behind the proposed claim"], "a positioning decision, the rejected alternatives, and the proof needed to carry the claim"),
            ("offer-architect", "The Offer Architect", "Turns scattered services into one engagement with a clean buying decision.", "a service offer designer who balances buyer value, delivery reality, and scope control", "building or repairing a coaching or consulting offer", ["who the engagement is and isn't for", "what must change by the end"], "a complete offer structure with scope, sequence, price logic, risks, and next test"),
            ("call-coach", "The Call Coach", "Diagnoses where a real sales conversation lost trust or momentum.", "a consultative sales coach who listens for weak diagnosis, hidden objections, and rushed recommendations", "improving discovery and sales conversations", ["what the prospect said the problem costs", "where the conversation changed direction"], "a call diagnosis, better questions, and the exact next conversation to run"),
            ("delivery-director", "The Delivery Director", "Keeps client work tied to decisions and visible movement.", "a client delivery director who insists on ownership, evidence, and a useful meeting outcome", "improving client delivery and implementation", ["the decision the client keeps avoiding", "what has and hasn't been completed"], "a delivery diagnosis and a short action plan with owners, dates, and review points"),
            ("scope-guardian", "The Scope Guardian", "Separates a useful favor from unpaid expansion that hurts the engagement.", "a consulting operations lead who protects results, relationships, and delivery capacity", "handling scope, boundaries, and change requests", ["what the contract includes", "what the client is asking for now"], "the scope call, a client-ready response, and the paid or deferred options"),
            ("renewal-strategist", "The Renewal Strategist", "Builds the renewal around evidence and the next business problem.", "a client success strategist who earns renewals through adoption and delivered value", "planning renewals, referrals, and right-fit expansion", ["what changed during the engagement", "what remains unresolved or newly possible"], "a renewal path, evidence gaps, conversation plan, and fallback closeout"),
        ],
    },
    {
        "number": "06", "slug": "email-marketing", "title": "Email Marketing Prompt Studio",
        "kicker": "Guided prompt system for email that sells", "accent": "#2f6b3a", "accent2": "#d6a11f",
        "subtitle": "Built for owners and marketers who need emails with a clear job. Plan the campaign, write the message, diagnose the numbers, and save the prompts your team will use again.",
        "categories": [
            ("strategy", "Campaign Direction", "Decide who the email is for and what it must make happen.", "email strategist accountable for message fit, conversion action, and list trust", "Describe the campaign, offer, audience, and timing", "Example: promote a May workshop to past buyers and engaged subscribers over 10 days"),
            ("copy", "Emails and Sequences", "Write messages that carry one idea to one next action.", "direct response email writer judged on clarity, reader momentum, and the click or reply the email earns", "Describe the email or sequence you need", "Example: three emails to turn webinar registrants into booked strategy calls"),
            ("lifecycle", "Lifecycle Email", "Send the right message for where the subscriber stands now.", "lifecycle marketer responsible for activation, retention, and timing across the customer relationship", "Describe the subscriber stage and desired next behavior", "Example: new trial user who created an account but hasn't invited a teammate"),
            ("list", "List and Segments", "Use behavior and intent to stop sending the same message to everyone.", "email operations strategist who builds useful segments from consent, behavior, recency, and buying history", "Describe the list, available data, and sending setup", "Example: 18,000 contacts with purchase dates, product tags, and 90-day engagement data"),
            ("testing", "Testing and Performance", "Read the numbers and test the part most likely to change the result.", "email performance analyst who traces weak results to audience, offer, message, timing, or delivery", "Describe the result, benchmarks, and what changed", "Example: opens held at 39% but clicks fell from 3.1% to 1.4% after the redesign"),
            ("review", "Review and Improve", "Fix the draft while keeping the offer and voice intact.", "senior email editor who preserves the useful idea while removing drag, confusion, and unsupported claims", "Paste the email material you want reviewed", "Paste one email, a sequence, subject lines, or a campaign brief"),
        ],
        "workflows": [
            items("""
Campaign Direction Memo::set the audience segment, offer angle, conversion action, timing, and measurement plan
Subscriber Intent Map::separate readers by awareness, relationship, and the reason they might act now
One Email One Job::choose the single decision or action the email must earn and cut competing jobs
Offer Angle Bench::build and rank distinct angles from urgency, proof, pain, desire, identity, and use case
Message Calendar::place campaign messages across the available dates without repeating the same argument
Send Pressure Plan::set frequency by list warmth, campaign length, and the cost of silence or fatigue
Proof Placement Map::match claims to the proof needed and place that proof where doubt appears
Campaign Risk Check::find audience, offer, timing, consent, and operational risks before the first send
"""),
            items("""
Subject Line Bench::write and rank subject lines by clarity, curiosity, specificity, and match to the email
Opening Line Set::create openings that enter the reader's current thought without throat clearing
Single Sales Email::write one complete email around one argument, one offer, and one next action
Story Email::turn a true event into a lesson and a natural offer bridge without a forced moral
Proof Email::build an email around evidence, context, limits, and the next action it supports
Objection Email::state the objection fairly, concede the true part, and answer the remaining risk
FAQ Email::turn recurring buying questions into a readable email that moves the decision forward
Short Promotion Sequence::sequence three to five emails so each adds a new reason to act
"""),
            items("""
Welcome Sequence::move a new subscriber from promise to first win, orientation, and next offer
Lead Magnet Follow Up::connect the downloaded resource to the problem it helps solve and the next useful step
Nurture Rhythm::plan recurring teaching, proof, point of view, and invitation emails without filler
Launch Sequence::map announcement, argument, proof, objections, deadline, and follow-up across a launch
Cart Recovery::respond to checkout friction with reminders, proof, support, and a clean return path
Post Purchase Flow::confirm the decision, reduce doubt, guide first use, and prevent avoidable support issues
Winback Sequence::reopen the relationship with inactive buyers using relevance before discounts
Renewal Sequence::recap use and value, address risk, and make the renewal decision easy to understand
"""),
            items("""
Segment Design::define useful segments from behavior, recency, purchase, interest, and consent
Engagement Policy::set active, cooling, inactive, and suppressed rules with dates and reasons
Preference Center Plan::decide what subscribers can control without creating a confusing settings wall
Personalization Map::use the data that changes the message and ignore decorative merge fields
List Positioning::state what subscribers will receive, how often, and why staying subscribed is worthwhile
Reactivation Campaign::test whether inactive subscribers still want the email before suppressing them
Suppression Rules::protect sender reputation by naming who shouldn't receive each campaign
Newsletter Plan::build repeatable sections and an editorial rhythm tied to a business purpose
"""),
            items("""
Metric Diagnosis::trace opens, clicks, replies, conversions, and unsubscribes to the most likely weak link
Subject Line Test::design a clean test with one variable, enough volume, and a decision rule
Body Copy Test::choose the highest-value copy test and hold audience, offer, and timing steady
Send Time Test::test timing without confusing day, segment, and message effects
CTA Test Plan::compare action wording, placement, and commitment level against one conversion goal
Deliverability Triage::separate reputation, authentication, complaints, list quality, and content causes
Campaign Postmortem::document what happened, why, what remains uncertain, and what changes next time
Performance Dashboard::choose a small set of metrics tied to business decisions, not reporting theater
"""),
            items("""
Email in Chief::review one email for idea, opening, argument, proof, CTA, voice, and unnecessary drag
Sequence in Chief::review a sequence for progression, repetition, gaps, timing, and the final decision path
Subject Line Review::test subject lines against the message inside, reader knowledge, and inbox sameness
Welcome Flow Review::find where a new subscriber loses the promise, first win, or next step
Promotion Review::strengthen a promotion without adding fake urgency, unsupported claims, or extra offers
Newsletter Review::tighten a newsletter around the reader payoff and the business job it must do
Cart Email Review::fix a recovery email that leans on reminders while ignoring the reason checkout stopped
Campaign Brief Review::find missing audience, offer, proof, timing, ownership, and measurement decisions
"""),
        ],
        "advisors": [
            ("campaign-editor", "The Campaign Editor", "Finds the one argument the campaign should own.", "an email campaign editor who connects audience intent, offer, proof, and timing", "planning an email campaign before copy starts", ["the exact conversion action", "what the reader already knows and believes"], "a campaign direction, message sequence, proof plan, and risks"),
            ("inbox-writer", "The Inbox Writer", "Works through one email until every line earns the next.", "a direct response email writer who values clarity, spoken rhythm, and a clean next action", "writing and revising individual emails", ["the one idea the reader should leave with", "the action the email must earn"], "a finished email plus the choices behind the subject, opening, argument, and CTA"),
            ("lifecycle-planner", "The Lifecycle Planner", "Matches messages to the subscriber's actual stage.", "a lifecycle marketer who maps activation, adoption, retention, and winback", "building automated email journeys", ["what the subscriber just did", "what useful behavior should happen next"], "a lifecycle plan with triggers, timing, message jobs, exits, and measures"),
            ("list-steward", "The List Steward", "Protects attention, consent, and sender reputation.", "an email operations lead responsible for consent, segmentation, suppression, and reputation", "improving list quality and sending policy", ["how contacts entered the list", "what engagement and purchase data exists"], "a list policy, segment map, suppression rules, and the first cleanup actions"),
            ("performance-doctor", "The Performance Doctor", "Finds whether the problem sits in delivery, message, offer, or page.", "an email performance analyst who diagnoses the whole path from delivery to purchase", "diagnosing weak email results", ["the last three comparable campaign results", "what changed in audience, offer, creative, or timing"], "a ranked diagnosis, evidence needed, next tests, and what to leave alone"),
            ("sequence-architect", "The Sequence Architect", "Makes each email add a new piece of the decision.", "an email sequence strategist who prevents repetition and builds argument in the right order", "planning multi-email sequences", ["the decision deadline or natural timing", "the objections and proof available"], "a send-by-send sequence map with message job, proof, CTA, and timing"),
        ],
    },
    {
        "number": "07", "slug": "launch-campaigns", "title": "Launch Campaign Prompt Studio",
        "kicker": "Guided prompt system for launches", "accent": "#c2452f", "accent2": "#d6a11f",
        "subtitle": "Built for founders, creators, and marketers coordinating a real launch. Turn the offer, dates, proof, and channels into campaign decisions, copy briefs, and a launch manual your team can run.",
        "categories": [
            ("direction", "Launch Direction", "Lock the buyer, promise, offer, and target before building assets.", "launch strategist responsible for the commercial target, central argument, and campaign tradeoffs", "Describe the offer, audience, dates, and launch target", "Example: open a 12-seat advisory cohort from September 9 to 16 to a 6,000-person email list"),
            ("offer", "Offer and Proof", "Build a buying case the campaign can support honestly.", "offer strategist who matches promise, price, proof, risk reversal, and buyer readiness", "Describe the offer and the part buyers may doubt", "Example: $1,800 cohort with six live sessions, templates, office hours, and three client results"),
            ("campaign", "Campaign Map", "Give every date and channel a clear job.", "campaign director who coordinates email, social, partners, events, sales pages, and operations", "Describe the channels, dates, assets, and team capacity", "Example: 14 days, email plus LinkedIn, one webinar, founder and one assistant"),
            ("assets", "Launch Assets", "Turn the campaign argument into pages, emails, events, and posts.", "launch copy director accountable for message consistency from first tease through checkout", "Describe the asset, audience stage, and action it must earn", "Example: webinar invitation email for warm subscribers who know the problem but not the program"),
            ("performance", "Control Room", "Read the launch while there is still time to act.", "launch performance lead who watches leading indicators, finds bottlenecks, and changes only what evidence supports", "Describe the current launch numbers and what has happened", "Example: day two, 1,900 page visits, 43 checkouts started, 11 purchases, email clicks on target"),
            ("review", "Review and Improve", "Stress-test launch material before buyers do.", "senior launch editor who protects the central argument while fixing gaps, repetition, and weak proof", "Paste the launch material you want reviewed", "Paste a launch plan, email, page, webinar outline, or social sequence"),
        ],
        "workflows": [
            items("""
Launch Direction Memo::set the audience, offer, central promise, conversion goal, dates, and nonnegotiable choices
Market Timing Check::judge whether buyer motivation, season, competing events, and delivery readiness support the dates
Buyer Motivation Map::connect current buyer pressures, desired change, hesitation, and trigger events to the campaign
Central Promise Test::make the promise specific, credible, desirable, and supported by the offer
Conversion Goal Math::work backward from revenue or enrollment to buyers, checkout starts, leads, and audience reach
Launch Type Decision::choose live, evergreen, challenge, webinar, partner, or direct launch from the offer and audience
Readiness Gate::separate must-fix launch blockers from improvements that can wait
Failure Pre Mortem::name how this launch could miss and install early warnings and responses
"""),
            items("""
Offer Stack::organize the core result, delivery, support, tools, access, and boundaries around buyer value
Price Confidence Memo::explain price through value, alternatives, delivery, proof, and fit without apology
Bonus Decision::keep only bonuses that remove friction or speed the promised result
Guarantee Design::reduce a real buyer risk without promising what the seller can't control
Proof Inventory::catalog results, demonstrations, credentials, process evidence, and missing support for each claim
Objection Map::turn buyer objections into message jobs, proof needs, page placement, and follow-up
Scarcity Check::use only deadlines and limits that are operationally true and clearly explained
FAQ Decision Set::answer the questions that block purchase, including fit, timing, work required, access, and refund terms
"""),
            items("""
Launch Timeline::sequence prelaunch, opening, proof, objection, deadline, and follow-up work by date and owner
Campaign Theme::choose a concrete organizing idea that can carry every channel without becoming a slogan
Channel Job Map::assign email, social, partners, events, page, and direct outreach separate roles
Asset Production Board::list every required asset with owner, dependency, draft date, review date, and publish date
Partner Campaign::build recruitment, briefing, tracking, swipe support, reminders, and follow-up for partners
Webinar Launch Map::connect registration, attendance, teaching, offer transition, replay, and follow-up
Social Countdown::plan posts that add buyer understanding rather than repeating the closing date
Team Run of Show::write the daily launch operating rhythm, decisions, reports, and escalation path
"""),
            items("""
Launch Email Sequence::map every send by reader stage, message job, proof, CTA, and date
Sales Page Wireframe::order the page around promise, problem, mechanism, offer, proof, objections, price, and action
Webinar Outline::teach a useful shift, demonstrate the method, transition to the offer, and handle the decision
VSL Argument Map::build a spoken sales argument with opening, problem, mechanism, proof, offer, and close
Open Cart Email::announce the offer by connecting the buyer's current situation to the decision now available
Proof Campaign::turn each proof asset into a message with context, limits, relevance, and a next action
Checkout Confidence::answer final risk questions around payment, access, workload, support, and what happens next
CTA Bank::write action lines for curiosity, registration, attendance, purchase, reply, and deadline stages
"""),
            items("""
Launch Dashboard::choose leading and lagging measures with targets, owners, refresh timing, and action thresholds
Daily Performance Read::compare actual results with the plan and isolate the first weak link in the path
Email Channel Check::diagnose delivery, opens, clicks, page visits, checkout starts, and purchases without blaming copy first
Page Friction Check::use traffic behavior and checkout data to rank the page issues worth touching midlaunch
Close Plan::decide the final messages, support coverage, decision cutoff, and operational steps for the last 48 hours
Midlaunch Adjustment::choose one evidence-backed change while protecting clean measurement and message consistency
Feedback Capture::collect objections, questions, sales conversations, support tickets, and lost-buyer reasons during the launch
Launch Postmortem::separate result, causes, unknowns, lessons, and the few changes the next launch should make
"""),
            items("""
Launch Plan in Chief::review the strategy, dates, dependencies, owners, targets, and response rules
Sales Page in Chief::review a launch page for argument order, proof, offer clarity, objections, price, and CTA
Email Sequence Review::find repetition, missing arguments, weak transitions, timing problems, and mismatched CTAs
Webinar in Chief::review a webinar for teaching value, retention, demonstration, offer transition, and close
VSL in Chief::strengthen a video sales letter without padding the runtime or inflating claims
Social Campaign Review::test whether the social sequence builds understanding or merely counts down
Checkout Review::find final-step confusion, risk, trust gaps, and operational surprises before payment
Evergreen Conversion Plan::turn a live launch into an ongoing path while removing false deadlines and live-only dependencies
"""),
        ],
        "advisors": [
            ("launch-director", "The Launch Director", "Makes the hard campaign choices before the calendar fills up.", "a launch director responsible for target, timing, message, channel roles, and team capacity", "setting launch direction and tradeoffs", ["the commercial target and dates", "what the audience already knows"], "a launch direction memo, rejected options, milestones, and top risks"),
            ("offer-room", "The Offer Room", "Tests whether the buying case can carry the launch.", "an offer strategist who challenges promise, proof, price, risk, and fit", "strengthening a launch offer", ["the exact paid result or access", "the claims with the strongest proof"], "a rebuilt offer case, proof gaps, objections, and the first fixes"),
            ("campaign-producer", "The Campaign Producer", "Coordinates assets, owners, dates, and dependencies.", "a campaign producer who turns launch strategy into a runable production board", "planning launch production and operations", ["the fixed launch dates", "the people and hours available"], "a production plan with owners, dependencies, review gates, and risks"),
            ("message-editor", "The Message Editor", "Keeps every asset carrying the same central argument.", "a launch message editor who aligns email, page, social, events, and checkout", "building and reviewing launch messaging", ["the central promise", "the strongest buyer objection"], "a message map, asset jobs, proof placement, and inconsistencies to fix"),
            ("control-room", "The Control Room", "Reads what is happening now and recommends the next move.", "a launch analyst who traces leading indicators to the first controllable bottleneck", "diagnosing a live launch", ["today's results against target", "what changed from the plan"], "a ranked diagnosis, one immediate action, watch points, and a no-change list"),
            ("evergreen-planner", "The Evergreen Planner", "Keeps what worked after the live deadline is gone.", "an evergreen conversion strategist who replaces live energy with useful triggers, proof, and follow-up", "turning launch assets into an ongoing campaign", ["which live moments drove action", "what depends on dates, live access, or founder presence"], "an evergreen path, asset reuse plan, honest timing triggers, and test order"),
        ],
    },
]


def make_field(category, review, label, example):
    return {
        "id": "material" if review else "situation",
        "label": label,
        "type": "textarea",
        "required": True,
        "placeholder": example,
        "helper": "Give the facts the output should use. Specifics beat background." if not review else "The prompt keeps your core intent and works directly from this material.",
    }


def make_studio(spec):
    profile = []
    for pid, label, ftype, required, placeholder, helper in COMMON_PROFILE:
        profile.append({"id": pid, "label": label, "type": ftype, "required": required, "placeholder": placeholder, "helper": helper})
    categories = []
    workflows = []
    for cat_index, (cid, title, note, role, label, example) in enumerate(spec["categories"]):
        categories.append({"id": cid, "title": title, "note": note})
        review = cid == "review"
        for wf_title, job in spec["workflows"][cat_index]:
            workflows.append({
                "id": slug(wf_title),
                "category": cid,
                "title": wf_title,
                "description": job[0].upper() + job[1:] + ".",
                "role": f"{role}, with direct responsibility for the {wf_title.lower()} this prompt produces",
                "fields": [make_field(cid, review, label, example), {
                    "id": "evidence", "label": "Numbers, evidence, or limits that should shape the answer", "type": "textarea", "required": False,
                    "placeholder": "Example: two weeks, $4,000 budget, three client quotes, legal review required", "helper": "Skip this if the field above already covers it."
                }],
                "task": [
                    f"Read my context and isolate the facts, constraints, and unknowns that matter to this {wf_title.lower()}.",
                    job[0].upper() + job[1:] + ".",
                    "Make the choices explicit. Rank options where a decision is needed, and tie every recommendation to something in my context.",
                    "Flag missing evidence and assumptions separately so I can review them before using the result."
                ],
                "rules": [
                    "Don't pad the deliverable with a general introduction or a summary that repeats it.",
                    "When two reasonable choices compete, state the tradeoff and make one recommendation."
                ],
                "output": f"a finished {wf_title.lower()} with the decision or artifact first, supporting reasoning, next actions, and a short assumptions check"
            })
    advisors = []
    for aid, title, description, role, focus, questions, deliverable in spec["advisors"]:
        advisors.append({"id": aid, "title": title, "description": description, "role": role, "focus": focus, "questions": questions, "deliverable": deliverable})
    return {
        "slug": spec["slug"], "title": spec["title"], "kicker": spec["kicker"], "subtitle": spec["subtitle"],
        "badge": "48 guided workflows", "accent": spec["accent"], "accent2": spec["accent2"], "footer": "Prompt Studio",
        "profile": profile, "categories": categories, "workflows": workflows, "advisors": advisors
    }


for studio in STUDIOS:
    data = make_studio(studio)
    assert len(data["workflows"]) == 48
    target = ROOT / "data" / f"{studio['number']}-{studio['slug']}.json"
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {target}")
