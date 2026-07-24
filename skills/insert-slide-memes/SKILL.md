---
name: insert-slide-memes
description: Plan, select, and add restrained, context-aware, widely recognizable memes to HTML slide decks in two modes. Use postprocess mode when Codex receives a completed HTML deck and must insert or revise memes without weakening its message, layout, accessibility, or navigation. Use plan-and-build mode when Codex is planning or generating a new HTML presentation and should decide meme timing, candidates, captions, and layout as part of the storyline before building the deck. Search across languages and meme cultures; select by communicative fit and audience recognition rather than the deck language. Trigger for requests to create funnier HTML slides, add memes or comic relief, plan humor beats, generate a meme-aware deck, or review existing meme placement.
---

# Insert Slide Memes

Use humor as pacing, analogy, reaction, or callback. Keep the deck's argument primary.

## Select a mode

Honor an explicitly requested mode. Otherwise:

- Choose `postprocess` when the user supplies a completed HTML deck or asks to revise an existing deck.
- Choose `plan-and-build` when the user supplies a topic, brief, source material, or outline and asks to create HTML slides with memes.
- If both an outline and HTML exist, choose the mode matching the requested stage. Do not require finished HTML for `plan-and-build`.
- State the selected mode in the first work update.

## Shared selection rules

1. Infer audience, setting, language, formality, shared references, and humor tolerance.
2. Read [references/meme-playbook.md](references/meme-playbook.md).
3. Define the communicative job before searching for an image.
4. Compare candidates from global, regional, and language-specific meme ecosystems.
5. Prefer an established, recognizable template. Do not generate an original meme unless the user explicitly asks.
6. Localize the caption while preserving the template's familiar meaning.
7. Verify the source and reuse status. Download chosen assets; never hotlink third-party images.
8. Default to roughly one meme per 5–7 content slides, cap at three unless requested otherwise, and use at most one meme per slide.
9. Reject a meme that decorates, repeats the slide, needs explanation, targets a person or group, or weakens the presenter's credibility.

## Mode: `postprocess`

1. Inspect the complete deck, assets, framework, slide boundaries, navigation, stable identifiers, and intended viewport.
2. Identify high-value release, analogy, callback, and transition moments without changing the deck's argument.
3. Create a short internal meme plan using the fields in **Meme plan**.
4. Search, score, source, and download only the selected recognizable templates.
5. Insert semantic markup and scoped CSS. Preserve the existing slide system, stable IDs, visual language, and keyboard behavior.
6. Choose the packaging method:
   - Default to relative local assets beside the deck.
   - Use Base64 `data:` URLs when the user requests a single self-contained HTML file.
   - Preserve `data-meme-source` metadata in either case.
7. Render every changed slide and its neighbors at the target viewport and one smaller viewport.
8. Verify keyboard navigation, image loading, overflow, and browser console output.
9. Run `python3 scripts/audit_memes.py path/to/deck.html --strict`.
10. Report changed slides, why each joke belongs, asset sources, reuse status, and packaging.

## Mode: `plan-and-build`

Read [references/plan-and-build.md](references/plan-and-build.md), then:

1. Establish the presentation goal, audience, setting, duration, tone, source material, and delivery format.
2. Build a content-first outline. Give every slide a narrative job and one primary message.
3. Mark only the moments that benefit from release, analogy, callback, or transition. Do not place memes at fixed intervals.
4. Add provisional meme briefs to the outline before choosing exact assets. Keep content slides understandable if every meme is removed.
5. Search and compare recognizable candidates only after the surrounding argument is clear. Record the winner, localized caption, source, reuse status, layout, and risk.
6. Treat outline approval already required by the presentation workflow as approval of the meme beats too. Add a separate approval gate only for material tone, reputational, or rights risk.
7. Generate the complete HTML deck with the selected meme moments included. Use stable slide identifiers from the first build.
8. Apply the same packaging, markup, guardrail, rendering, and audit requirements as `postprocess`.
9. Replace or drop any meme that fails the two-second recognition test in the rendered deck.
10. Report planned versus final meme placements and any candidate changed during visual QA.

## Meme plan

For each proposed placement record:

- slide identifier and narrative job
- role: `reaction`, `analogy`, `callback`, or `transition`
- intended audience response
- candidates considered across cultures and why the winner is most recognizable
- caption or setup, preferably under 12 words
- source and reuse status
- layout and primary-content tradeoff
- risk: audience fit, ambiguity, stereotype, copyright, or dated reference
- status: `provisional`, `selected`, or `dropped`

## HTML contract

Use this structure when the deck permits it:

```html
<figure
  class="slide-meme"
  data-meme-role="reaction"
  data-meme-source="https://source.example/template-page"
>
  <img
    src="assets/memes/recognized-template.jpg"
    alt="Description of the recognizable reaction shown in the meme"
  />
  <figcaption>Localized caption that completes the joke</figcaption>
</figure>
```

Use a verified source page or a short project-owned marker in `data-meme-source`. Keep meaningful alternative text distinct from the joke caption. Use `alt=""` only for a truly decorative image.

Scope styles under the deck or `.slide-meme` namespace:

```css
.slide-meme {
  margin: 0;
  max-width: min(34vw, 30rem);
}

.slide-meme img {
  display: block;
  width: 100%;
  max-height: 42vh;
  object-fit: contain;
}

.slide-meme figcaption {
  margin-top: 0.4rem;
  font-size: clamp(0.85rem, 1.4vw, 1.1rem);
  line-height: 1.2;
}
```

Adapt values to the deck. Do not introduce global `img`, `figure`, or typography rules.

## Guardrails

- Do not put a meme on the title, agenda, legal/compliance material, sensitive personal stories, layoffs, safety incidents, or solemn conclusions unless explicitly requested and clearly appropriate.
- Do not target protected traits, appearance, disability, victims, junior staff, customers, or identifiable coworkers.
- Avoid political, sexual, violent, insulting, or profanity-heavy material by default.
- Do not treat popularity or search availability as permission. Record the source and rights status; use a cleared alternative when public distribution requires it.
- Never invent an image source, license, quotation, or attribution.
- Do not let a meme shrink body text, cover controls, cause overflow, or become necessary to understand the slide.
- Preserve a usable deck if images fail to load.

## Verification

Check:

- no cropping of faces, captions, or key visual details
- no overlap at the target viewport and one smaller viewport
- sufficient caption contrast and readable type
- no remote hotlinks; local or valid embedded assets only
- meaningful `alt` text and source metadata
- restrained density and no more than one meme per slide
- coherent visual treatment
- no autoplay, flashing animation, or layout shift

The audit script performs structural checks, not visual judgment. Rendering and human-context review remain mandatory.
