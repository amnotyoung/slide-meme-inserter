---
name: insert-slide-memes
description: Plan, select, and add context-aware, recognizable memes to HTML slide decks, either while building a new presentation or editing a completed deck. Use widely circulating internet memes by default, with strict rights clearance available on request. Accept user-supplied images, URLs, template names, captions, and placements; preserve source honesty, safety, accessibility, and layout. Search across languages and meme cultures when the user has not fixed the asset. Use for meme-aware HTML presentations, adding supplied or searched memes, and reviewing meme placement.
---

# Insert Slide Memes

Use humor as pacing, analogy, reaction, or callback. Keep the deck's argument primary.

Resolve `references/` and `scripts/` relative to the directory containing this `SKILL.md`. Do not assume the current working directory is the plugin root.

## Select a mode

Honor an explicitly requested mode. Otherwise:

- Choose `postprocess` when the user supplies a completed HTML deck or asks to revise an existing deck.
- Choose `plan-and-build` when the user supplies a topic, brief, source material, or outline and asks to create HTML slides with memes.
- If both an outline and HTML exist, choose the mode matching the requested stage. Do not require finished HTML for `plan-and-build`.
- State the selected mode in the first work update.

## Select a rights mode

Rights mode is separate from `postprocess` or `plan-and-build`. Honor an explicit
choice and record it as root-level `rights_mode` in the JSON plan.

- `common-use` is the default, including when delivery context is unknown. Use a
  widely circulating internet meme when its established use and slide fit are
  clear. Record the source and `rights_status: common-use-unverified`; no license
  proof, legal-review form, or separate user approval is needed. File sharing,
  clients, paid talks, exports, recording, and public posting do not automatically
  change this mode.
- `strict` is opt-in when the user asks for cleared assets or a stated project
  requirement calls for them. A selected asset needs a license, permission,
  public-domain basis, or documented statutory exception.
- `practical` remains available on explicit request for a one-off `live-internal` presentation with
  `distribution: internal`, no file sharing, no client or paid audience, and no
  export, recording, or publication. It permits a selected asset after the compact
  practical review in the rights contract; it does not declare the use lawful.
- Do not ask the user to reconfirm common-use for each asset or infer a clearance
  requirement from the audience alone. Popularity is a workflow selection basis,
  not permission or a promise that claims will not occur.

## Shared selection rules

1. Establish audience, setting, language, formality, shared references, humor tolerance, and known intended uses. In common-use, unknown delivery details do not block work. Treat an unverified shared reference as absent; do not infer fandom, gaming, political, or subculture affinity from profession, nationality, age, or technical fluency.
2. Read [references/meme-playbook.md](references/meme-playbook.md).
3. Apply [references/rights-clearance.md](references/rights-clearance.md). In common-use, the existing meme-recognition evidence and an honest source record are sufficient; skip legal-review paperwork. Read the detailed clearance sections only for strict or practical mode, or a concrete issue with the chosen asset.
4. Read [references/user-provided-memes.md](references/user-provided-memes.md) when the user supplies any asset, URL, template name, caption, or placement instruction.
5. Define the communicative job before searching for an image.
6. For every unresolved placement, start globally established meme discovery with Imgflip's template and active-caption ecosystem. Use it to compare comic execution, variation, and fatigue; use Know Your Meme or another maintained contextual source afterward to verify established meaning and origin. When the target culture is poorly represented on Imgflip, use a regional source first and record why. Explore globally common, regional or language-specific, and relevant professional or community meme ecosystems as coverage, not a quota.
7. Apply every hard gate in the playbook before scoring or sourcing an asset. A caption cannot turn promotional art, wallpaper, stock imagery, fandom art, or an unrelated illustration into a meme.
8. Prefer an established, recognizable template whose familiar meaning performs part of the joke. Write a new slide-specific caption for that template. Do not generate a new visual meme format or AI-original illustration unless the user explicitly asks.
9. Record the rights mode, discovery route and page, humor evidence, per-dimension score, recognition basis, identity signal, source roles, known uses, attribution location, and gate results in a machine-readable JSON plan. Add legal or practical review fields only when the selected mode requires them. Run `python3 <skill-root>/scripts/audit_meme_plan.py path/to/meme-plan.json --strict` before downloading or inserting an asset. This CLI flag treats audit warnings as failures; it does not select strict rights mode.
10. Localize the caption while preserving the template's familiar meaning.
11. Keep active-humor discovery, semantic history, original provenance, asset location, legal evidence, and attribution as separate facts. An Imgflip discovery page is not semantic or legal evidence, and a Know Your Meme history page is not the asset source. For Korean candidates, follow the Korean source hierarchy and static-image workflow in the playbook. Download only a candidate that already passed selection; never hotlink third-party images or capture frames from video.
12. Use the adaptive density rules in the playbook instead of a fixed deck-wide count. Treat the audience-specific range as a soft ceiling, not a quota; zero memes is valid, and long decks may exceed three when enough high-value placements pass every gate. Normally leave at least five non-meme content slides between distinct meme beats, account for section dividers and live demonstrations that already reset attention, and use at most one meme per slide. Honor an explicit user count while warning if it materially weakens the deck.
13. Reject a searched candidate that decorates, repeats the slide, needs explanation, depends on an unverified subculture, implies an unsupported presenter identity, or weakens the presenter's credibility. Missing license evidence or an unknown original creator alone does not make a common-use meme provisional.

## Mode: `postprocess`

1. Inspect the complete deck, assets, framework, slide boundaries, navigation, stable identifiers, and intended viewport.
2. Identify high-value release, analogy, callback, and transition moments without changing the deck's argument.
3. Create the machine-readable meme plan using the fields in **Meme plan**.
4. Use user-supplied assets and instructions first. A supplied, widely circulating meme can be selected in common-use without license evidence. Search and hard-gate candidates only for unresolved placements. Audit the plan before downloading any selected asset.
5. Insert semantic markup and scoped CSS. Preserve the existing slide system, stable IDs, visual language, and keyboard behavior.
6. Choose the packaging method:
   - Default to relative local assets beside the deck.
   - Use Base64 `data:` URLs when the user requests a single self-contained HTML file.
   - Preserve `data-meme-source` metadata in either case.
7. Render every changed slide and its neighbors at the target viewport and one smaller viewport.
8. Verify keyboard navigation, image loading, overflow, and browser console output.
9. Run `python3 <skill-root>/scripts/audit_memes.py path/to/deck.html --plan path/to/meme-plan.json --strict` (or pass multiple slide files / a slide directory for multi-file decks).
10. Report changed slides, why each joke belongs, asset sources, reuse status, and packaging.

## Mode: `plan-and-build`

Read [references/plan-and-build.md](references/plan-and-build.md), then:

1. Establish the presentation goal, audience, setting, duration, tone, source material, and delivery format.
2. Build a content-first outline. Give every slide a narrative job and one primary message.
3. Mark only the moments that benefit from release, analogy, callback, or transition. Do not place memes at fixed intervals.
4. Add provisional meme briefs to the outline before choosing exact assets. Keep content slides understandable if every meme is removed.
5. Apply user-supplied assets and instructions to the relevant outline records. Search and hard-gate recognizable candidates only for unresolved placements after the surrounding argument is clear. Record the complete gate, score, audience, identity, source, layout, and risk fields.
6. Apply any outline approval already required by the presentation workflow. Common-use needs no separate asset-rights approval; raise only concrete tone, reputational, or asset-use issues that affect the result.
7. Generate the complete HTML deck with the selected meme moments included. Use stable slide identifiers from the first build.
8. Audit the machine-readable plan before asset download, then apply the same packaging, markup, guardrail, rendering, and HTML audit requirements as `postprocess`.
9. Replace or drop any meme that fails the two-second recognition test in the rendered deck.
10. Report planned versus final meme placements and any candidate changed during visual QA.

## Meme plan

For each proposed placement record:

- unique plan ID and slide identifier
- slide identifier and narrative job
- role: `reaction`, `analogy`, `callback`, or `transition`
- earlier setup slide ID when the role is `callback`
- intended audience response
- origin: `user-provided` or `searched`
- user-locked fields such as asset, template, caption, or placement
- template name and asset kind
- recognition basis and concrete audience evidence; never `assumed` for a selected searched candidate
- identity signal level, domain, and explicit user approval when material
- every hard-gate result from the playbook
- all seven score dimensions, total, ubiquity penalty, and adjusted score
- discovery route: `imgflip-first`, `regional-first`, or `fallback-other`
- direct discovery page, concrete humor evidence, and a fallback reason when the route is not `imgflip-first`
- candidates considered across cultures and why the winner is most recognizable
- caption or setup, preferably under 12 words
- separate semantic, asset, and HTML attribution sources; original source when known
- plan-level rights mode: `common-use` (default), `strict`, or `practical`
- rights status, known intended use modes, distribution scope, and attribution location
- legal evidence and additional-rights forms only for strict/practical review or a claimed clearance; common-use needs no extra review object
- attribution text, URL, and location
- layout and primary-content tradeoff
- risk: audience fit, ambiguity, stereotype, copyright, or dated reference
- status: `provisional`, `selected`, or `dropped`

Use the JSON field names and example in [references/plan-and-build.md](references/plan-and-build.md). A Markdown summary may accompany the JSON, but it does not replace the audited plan.

## HTML contract

Use this structure when the deck permits it:

```html
<figure
  class="slide-meme"
  data-meme-plan-id="m01"
  data-meme-role="reaction"
  data-meme-template="RECOGNIZED_TEMPLATE_NAME"
  data-meme-source="SOURCE_URL_HERE"
  data-meme-origin="searched"
>
  <img
    src="assets/memes/recognized-template.jpg"
    alt="Description of the recognizable reaction shown in the meme"
  />
  <figcaption>Localized caption that completes the joke</figcaption>
  <a
    class="meme-attribution"
    data-meme-attribution-location="on-slide"
    href="ATTRIBUTION_URL_HERE"
  >
    Template — Source page
  </a>
</figure>
```

Map `data-meme-plan-id`, `data-meme-role`, `data-meme-template`, `data-meme-source`, and `data-meme-origin` from the audited plan. Set `data-meme-source` and the `.meme-attribution` link to the plan's `attribution_url`. In common-use, an actual template or repost page is a valid source; label it honestly without implying ownership or a license. Use `data-meme-plan-id` on an attribution placed outside the figure and map `data-meme-attribution-location` from the plan. Put credits in a slide classed as `credits`, `credits-slide`, `references`, or `sources`; put speaker-note attribution in a `speaker-notes` or `data-speaker-notes` container. Keep meaningful alternative text distinct from the joke caption. Use `alt=""` only for a truly decorative image.

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
- Treat gaming, sports-team, entertainment-franchise, political, religious, and other fandom imagery as a material presenter-identity signal. Do not use it for a searched candidate without concrete audience evidence and explicit user approval.
- Reject promotional art, wallpapers, press images, stock images, and unrelated illustrations as searched memes even when their slogan or subject creates a topical word association.
- Use widespread meme circulation as sufficient for common-use selection, while keeping legal permission unverified. Do not invent assurances about legality or the likelihood of a claim.
- Use public Imgflip examples to understand format rhythm and current variation; do not copy another user's distinctive caption verbatim as the deck's punchline.
- For a recognizable, widely circulating meme, use `common-use-unverified` and proceed. In strict mode, use a cleared alternative or document a statutory-exception analysis. In practical mode, complete the requested review and use `practical-reviewed`.
- Address concrete issues such as an explicit reuse restriction, an actual rights-holder objection, or a misleading endorsement; do not impose a speculative legal checklist on routine memes. Update known use modes when delivery changes without automatically switching common-use to strict.
- Never invent an image source, license, quotation, or attribution.
- Do not let a meme shrink body text, cover controls, cause overflow, or become necessary to understand the slide.
- Preserve a usable deck if images fail to load.

## Verification

Check:

- no cropping of faces, captions, or key visual details
- no overlap at the target viewport and one smaller viewport
- sufficient caption contrast and readable type
- no remote hotlinks; local or valid embedded assets only
- meaningful `alt` text, source metadata, and attribution at the planned location
- exact correspondence with a selected record in the audited meme plan
- restrained density and no more than one meme per slide
- coherent visual treatment
- no autoplay, flashing animation, or layout shift

The audit script performs structural checks, not visual judgment. Rendering and human-context review remain mandatory.
