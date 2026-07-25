# Meme Selection Playbook

## Placement score

Score a candidate from 0–2 on each dimension:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Narrative value | decoration only | mild emphasis | clarifies a feeling, analogy, or transition |
| Template semantics | format conflicts with message | workable adaptation | template's established meaning matches exactly |
| Audience recognition | obscure or niche | many may know it | immediately recognizable to this audience |
| Novelty and fatigue | stale default or likely eye-roll | familiar but still usable | fresh to this audience without becoming obscure |
| Caption clarity | needs explanation | caption carries it | lands at a glance |
| Layout fit | displaces content | requires rearrangement | fits without weakening hierarchy |
| Safety and rights | material concern | manageable with warning | appropriate and reuse status is clear |

Apply an additional `-1` ubiquity penalty when a template repeatedly appears as a generic answer across unrelated presentation topics. Common examples include `Confused Math Lady`, `Drake Hotline Bling`, and `This Is Fine`; treat these as illustrative, not as a permanent blacklist. Keep the penalty even when the template remains the best semantic fit.

Insert only candidates with an adjusted score of at least 12/14 and no unresolved safety concern. Record both the seven-dimension score and any ubiquity penalty.

## Cross-language search

Treat language as a search dimension, not a selection rule.

1. Define the precise communicative job: reaction, dilemma, reversal, escalation, false confidence, shared pain, or transition.
2. Search current sources using:
   - the deck language
   - English and globally common meme terminology
   - relevant regional or professional-community vocabulary when the audience is likely to know it
3. Build a sourced candidate slate with at least:
   - 2 globally common templates
   - 2 regional or language-specific templates
   - 2 workplace, professional, or relevant community templates
4. Record a concrete template name and source or search evidence for every candidate. Do not count an unnamed category such as “Korean reaction image” as a candidate.
5. If one ecosystem has no credible candidate for the audience and communicative job, record why and replace it with candidates from another distinct ecosystem. Do not pad the slate with weak or invented entries.
6. Do not add an original, generated, or directly produced meme to the candidate slate unless the user explicitly requests one.
7. Eliminate candidates that depend on a niche community, untranslated wordplay, or cultural knowledge the audience probably lacks.
8. Score the survivors with the table above and apply the ubiquity penalty.
9. Break ties by semantic precision, audience recognition, novelty/fatigue, caption brevity, rights clarity, and asset quality—in that order.

Do not prefer a Korean meme for Korean slides or an English meme for English slides merely because the languages match. A globally known template with a localized caption can outperform a same-language reference, and a regional meme can win when the audience clearly recognizes it.

## Useful roles

- **Reaction:** Release tension after a dense, painful, or surprising fact.
- **Analogy:** Make an abstract system or failure mode memorable.
- **Callback:** Reuse an earlier joke after the audience understands the premise.
- **Transition:** Reset attention before a major section change.

Prefer one role per asset. A callback usually works better than introducing three unrelated meme formats.

## Timing

Good moments:

- immediately after a difficult truth, not before the evidence
- after a dense run of slides
- at a recognizable “we have all experienced this” moment
- before a section transition when the audience needs a reset

Weak moments:

- every slide or at predictable intervals
- before the audience understands the premise
- during instructions that must be remembered exactly
- on a slide already carrying a chart, code sample, and long explanation

## Tone levels

- **Subtle:** Widely recognized reaction template, visual metaphor, or dry caption with restrained treatment. Use for executives, clients, and mixed audiences.
- **Conversational:** Recognizable workplace situation with a concise caption. Use for internal talks and workshops.
- **Internet-native:** Strong format conventions or niche references. Use only when the audience clearly shares that culture.

Default to subtle when context is missing.

## Asset guidance

Prefer a recognizable template whose established meaning does part of the comedic work. Do not generate an original meme by default; unfamiliar imagery must explain itself and therefore usually lands less reliably.

Add or localize the caption in HTML when practical rather than baking text into the image. This improves accessibility, editing, localization, and rendering quality. Preserve original template text when it is itself the recognized punchline, such as a short catchphrase the audience is likely to understand.

For external assets:

1. Verify the source page and reuse terms.
2. Download a suitable local copy.
3. Record the source URL and license or permission status.
4. Preserve attribution if required.
5. Do not treat search-result availability as permission.

## Layout patterns

- **Sidecar:** Main point on one side, meme on the other. Best for reaction and analogy.
- **Punchline reveal:** Evidence first, small reaction visual second. Use only if the slide framework supports deliberate reveals.
- **Section bumper:** Large image with a short caption between content sections.
- **Corner reaction:** Small visual accent that does not compete with a chart or quote.

Never place essential text inside the raster image. Keep captions concise and use the deck's existing spacing, border, shadow, and color tokens.

## Final editorial test

For every meme, ask:

1. Does the slide become clearer or better paced?
2. Will the intended audience understand it within two seconds?
3. Is the joke aimed at a shared situation rather than a person or group?
4. Would the presenter be comfortable if the slide were screenshotted without context?
5. Is the source or generation status honest and recorded?
6. Did a familiar default win because it was truly best after the novelty and ubiquity checks, rather than because it was the first recognizable result?

Remove the meme if any answer is no.
