---
name: insert-slide-memes
description: Add restrained, context-aware, widely recognizable memes to existing HTML slide decks while preserving the deck's message, layout, accessibility, and audience fit. Search across languages and meme cultures and select by communicative fit and audience recognition rather than the deck's language. Use when Codex is asked to make HTML presentations funnier, add memes or comic relief, create reaction-image moments, improve a dry web-based deck, or review and revise meme placement in HTML/CSS/JS slides.
---

# Insert Slide Memes

Add humor only where it gives the audience a useful release, analogy, or callback. Treat the deck's argument as primary and the meme as supporting evidence or pacing.

## Workflow

1. Inspect the complete deck, its assets, framework, slide boundaries, navigation, and viewport.
2. Infer the audience, setting, language, formality, shared cultural references, and humor tolerance from the deck and request. Ask only when a wrong assumption would create material reputational risk.
3. Read [references/meme-playbook.md](references/meme-playbook.md). Create a short internal meme plan before editing.
4. Select only high-value placements. Default to roughly one meme per 5–7 content slides, cap at three unless the user requests more, and place at most one meme on a slide.
5. Search broadly rather than matching the deck language mechanically:
   - Build candidates from global, regional, and language-specific meme ecosystems.
   - Compare familiar image macros, reaction stills, caption formats, and recurring phrases by meaning and recognition.
   - Select the highest-scoring candidate even when its origin language differs from the deck.
6. Prefer an established, recognizable template. Reuse a user-provided or project-owned asset when it is equally effective. Do not generate an original meme unless the user explicitly requests one.
7. Verify the source and reuse status, then store chosen images locally beside the deck's other assets. Do not hotlink third-party images.
8. Localize the caption to the presentation language while preserving the template's recognized semantic pattern. Keep original-language words only when recognition depends on them.
9. Insert semantic markup and scoped CSS that follow the contract below. Preserve the existing slide system and visual language.
10. Render the deck at its intended viewport. Inspect every changed slide, neighboring slides, keyboard navigation, asset loading, and the browser console.
11. Run `python3 scripts/audit_memes.py path/to/deck.html`. Resolve errors and assess warnings. Use `--strict` before final delivery when the deck follows the markup contract.
12. Report which slides changed, why each joke belongs there, and the source and reuse status of every asset.

## Meme Plan

For each candidate, decide:

- slide identifier and its narrative job
- meme role: `reaction`, `analogy`, `callback`, or `transition`
- intended audience response
- candidate templates considered across cultures and why the winner is most recognizable
- caption or setup, preferably under 12 words
- asset source and reuse status
- layout position and primary-content tradeoff
- risk: audience fit, ambiguity, stereotype, copyright, or dated reference

Reject candidates that merely decorate, repeat the slide text, require explanation, or make the presenter sound contemptuous.

## HTML Contract

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

Replace the example URL with the verified source page. Use a real source URL or a short project-owned marker in `data-meme-source`. Keep meaningful alternative text distinct from the joke caption. Use `alt=""` only for a truly decorative image.

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

- Do not put a meme on the title slide, agenda, legal/compliance material, sensitive personal stories, layoffs, safety incidents, or solemn conclusions unless explicitly requested and clearly appropriate.
- Do not use humor targeting protected traits, appearance, disability, victims, junior staff, customers, or identifiable coworkers.
- Avoid political, sexual, violent, insulting, or profanity-heavy material by default.
- Do not assume that popularity or search-result availability grants reuse rights. Record the source and rights status; flag unclear rights and use a cleared alternative for public or external distribution.
- Do not generate an original substitute merely to avoid searching across languages. Generate only when the user asks for original work.
- Never invent an image source, license, quotation, or attribution.
- Do not let a meme shrink body text, cover controls, cause overflow, or become necessary to understand the slide.
- Preserve a usable deck if images fail to load.

## Verification

Check at minimum:

- no cropping of faces, captions, or key visual details
- no overlap at the target viewport and one smaller viewport
- sufficient caption contrast and readable type size
- correct local paths and no remote hotlinks
- meaningful `alt` text and source metadata
- no more than one meme per slide and restrained deck-wide density
- coherent visual treatment across all inserted memes
- no autoplay, flashing animation, or layout shift

The audit script performs structural checks, not visual judgment. Rendering and human-context review remain mandatory.
