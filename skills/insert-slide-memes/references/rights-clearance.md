# Meme Use and Optional Rights Clearance

Use common-use by default for widely circulating internet memes. This is a working
preference, not a claim of legal permission. Keep source records honest and read
the detailed review sections only when strict or practical mode is requested, or
when a concrete issue needs attention.

## Contents

- Rights modes
- Selection rule
- Intended use modes
- Clearance evidence
- Statutory-exception analysis
- Additional rights
- Attribution
- Example

## Rights modes

Choose one plan-level `rights_mode`.

### `common-use` — default

Proceed with recognizable internet memes without seeking a license, a legal
opinion, or separate user approval for each image. This applies to internal and
client presentations, paid talks, shared decks, exports, recordings, and public
posting. Unknown delivery context does not trigger strict mode or a question.

Use `rights_status: "common-use-unverified"`. Reuse existing selection fields:

- `hard_gates.established_format: true` and a meme `asset_kind`
- `recognition_evidence`: a short, concrete note about the template's recurring use
- the actual source page, image location, and an honest attribution

This applies equally to searched and user-provided memes. A template page or
repost can be the asset/attribution source; it need not establish ownership.
Record `original_source` when known and omit it or use `null` when unknown. Do not
invent a creator or block a familiar meme solely because its original is untraced.
No `legal_basis`, `practical_review`, or `additional_rights` form is required.
Record known `use_modes` and the matching `distribution`; omit both when unknown.
Missing license evidence alone does not generate an audit warning or score penalty.

Reserve `cleared` and `exception-reviewed` for their documented bases, even in
common-use mode. Popularity does not establish legal permission or immunity from
claims. Do not promise that a rights holder will ignore a particular user.
If an actual objection, an explicit reuse restriction, or misleading endorsement
is identified, address that specific issue. Do not turn hypothetical concerns
into a routine approval or legal-research workflow.

### `strict`

Use strict mode when the user requests cleared assets or a stated project
requirement demands them. Do not infer that requirement from sharing, clients,
payment, export, recording, or publication alone. A selected placement must use
one of the legal bases below.

### `practical`

Practical mode is an optional legacy risk screen for a one-off internal live
presentation. Every selected placement must use only `live-internal` with
`distribution: internal`. File sharing, client or paid audiences, PDF or image
export, recording, and online publication are forbidden.

A previously unclear or user-provided asset may become
`rights_status: "practical-reviewed"` only after recording:

- `transformative_context`: how the slide comments on, reacts to, or repurposes the
  image in the presentation's own message
- `necessity`: why this image and this single use serve that communicative job
- `amount_resolution`: the limited amount, low resolution, and treatment used
- `market_substitution`: why the slide does not replace demand for the source work
- `moral_personality_risk`: alteration, dignity, endorsement, portrait/publicity,
  and sensitive-person risks
- `attribution_method`: exactly `on-slide`, `credits-slide`, or `speaker-notes`,
  matching `attribution_location`
- `checked_at`: review date
- `no_recording_or_distribution: true`

For a scored searched candidate, set `scores.safety_rights` to `1`;
`practical-reviewed` is bounded risk, not documented clearance.

This mode does not supply a statutory exception, certify legality, or predict a
court result. If a practical constraint changes, update the plan using common-use
for established memes, or strict when clearance is requested. Do not present the
old practical review as covering the expanded use.

## Selection rule

In common-use mode, an established meme may be `selected` with
`rights_status: "common-use-unverified"` using the selection evidence above.

In strict mode, a placement may be `selected` only when it has one documented
legal basis:

- `license`
- `permission`
- `public-domain`
- `quotation-art-28`
- `fair-use-art-35-5`
- `school-education-art-25`

Use the statutory-exception labels only for a Korean-law analysis. Record another jurisdiction in `jurisdiction` and use a licensed or permitted asset when the applicable exception has not been reviewed.

Use `rights_status: "cleared"` for a license, permission, or public-domain basis. Use `rights_status: "exception-reviewed"` for a reviewed statutory exception. In practical mode only, use `rights_status: "practical-reviewed"` after completing the compact review above. `unclear` and `user-provided-unverified` are provisional intake states; an established meme can move to `common-use-unverified` without resolving its license.

The audit verifies that evidence and analysis fields exist. It does not certify that a license is authentic or that a court would accept a statutory exception.

## Intended use modes

Record known planned uses (required in strict/practical mode):

- `live-internal`
- `internal-file-share`
- `live-client`
- `external-file-share`
- `paid-event`
- `public-pdf`
- `public-recording`
- `online-publication`

Set `distribution` to:

- `internal` for internal-only modes
- `external-limited` when `live-client`, `external-file-share`, or `paid-event` is the broadest mode
- `public` when a public PDF, recording, or online publication is planned

Adding a use mode does not automatically change common-use. When claiming a
license, permission, or reviewed exception, check that it covers the new scope;
a live-only permission does not authorize PDF distribution or recording.

## Clearance evidence

For `license` or `permission`, record:

- rights holder
- evidence URL, local permission record, or contract reference
- date checked
- jurisdiction
- covered use modes
- commercial-use permission
- modification permission
- territory
- expiration or `none`

For `public-domain`, record the evidence, date checked, jurisdiction, and the reason the work is in the public domain. Do not infer public-domain status from age, popularity, or anonymous reposting.

## Statutory-exception analysis

For `quotation-art-28`, record:

- every use mode covered by the analysis
- purpose of the quotation
- why the presentation remains the main work and the meme remains subordinate
- why the amount used is necessary
- why the form of use follows fair practice
- market effect
- visible attribution method

For `fair-use-art-35-5`, record:

- every use mode covered by the analysis
- purpose and character
- nature and use of the original work
- amount and importance used
- effect on the current and potential market

For `school-education-art-25`, record:

- every use mode covered by the analysis
- qualifying institution basis
- actual class purpose
- necessary scope
- compensation and access-control treatment

Do not use a statutory exception as a generic label for decoration, an icebreaker, or attention capture. The analysis must connect the asset to the presentation's actual criticism, explanation, education, or research purpose.

## Additional rights

These structured checks are required for strict/practical records and claims of
clearance. Common-use requires attention to concrete issues, not this form.

Review and explain:

- `moral_rights`: use `not-modified`, `permitted`, or `reviewed`
- `portrait_publicity`: use `not-applicable`, `permission`, or `reviewed`
- `trademark`: use `not-applicable`, `permission`, `descriptive-use`, or `reviewed`

Do not imply endorsement, partnership, or a person's recommendation. Do not materially distort an original or combine an identifiable person with degrading, sexual, political, or promotional messaging without a documented basis.

## Attribution

Keep discovery, semantic history, original provenance, asset location, legal evidence, and attribution separate.

Record:

- `attribution_text`: template/work and actual source; creator and license only when known
- `attribution_url`: in common-use, the actual template, source, or repost page; for strict/practical, the creator-controlled, publisher-controlled, or license-required source
- `source`: the same value as `attribution_url` for HTML mapping

Record `attribution_location`:

- `on-slide` or `credits-slide` in strict mode
- `on-slide`, `credits-slide`, or `speaker-notes` in common-use or practical mode

Prefer credits or speaker notes for common-use when an on-slide source would
distract from the joke. Include visible credits in a PDF if notes are not exported.

Render `attribution_text` as a link with class `meme-attribution`. An on-slide link
belongs inside the meme figure. A credits or speaker-notes link belongs outside the
figure and must carry both `data-meme-plan-id` and
`data-meme-attribution-location`. A hidden `data-meme-source` attribute,
`user-provided`, or `source: internet` is not sufficient. An actual aggregator or
template page is acceptable attribution in common-use, but is not legal evidence.

Put a credits link in a slide classed as `credits`, `credits-slide`, `references`,
or `sources`. Put a speaker-notes link in an element with class `speaker-notes` or
the `data-speaker-notes` attribute. The HTML audit checks these containers.

## Examples

### Common-use placement

These are the use-related fields, not a complete placement. No rights-review
object is needed; see `plan-and-build.md` for the full selection schema.

```json
{
  "rights_status": "common-use-unverified",
  "asset_kind": "meme-template",
  "recognition_evidence": "The template page shows recurring variations of the same two-choice joke.",
  "original_source": null,
  "attribution_text": "Two Buttons — Imgflip template page",
  "attribution_url": "https://imgflip.com/meme/Two-Buttons",
  "source": "https://imgflip.com/meme/Two-Buttons",
  "attribution_location": "credits-slide",
  "distribution": "public",
  "use_modes": ["public-pdf", "online-publication"]
}
```

### Strict placement

```json
{
  "rights_status": "cleared",
  "attribution_location": "on-slide",
  "distribution": "external-limited",
  "use_modes": ["live-client"],
  "legal_basis": {
    "type": "license",
    "jurisdiction": "KR",
    "evidence": "https://example.com/license",
    "checked_at": "2026-07-25",
    "rights_holder": "Example Creator",
    "scope": {
      "use_modes": ["live-client"],
      "commercial_use": true,
      "modification": true,
      "territory": "worldwide",
      "expiration": "none"
    }
  },
  "additional_rights": {
    "moral_rights": {
      "status": "not-modified",
      "note": "The licensed template is shown without altering the raster."
    },
    "portrait_publicity": {
      "status": "not-applicable",
      "note": "No identifiable natural person appears."
    },
    "trademark": {
      "status": "not-applicable",
      "note": "No third-party mark is used."
    }
  },
  "attribution_text": "Example Creator — Licensed Template, CC BY 4.0",
  "attribution_url": "https://example.com/license",
  "source": "https://example.com/license"
}
```

### Practical placement

This record is valid only in a plan with `"rights_mode": "practical"`:

```json
{
  "rights_status": "practical-reviewed",
  "attribution_location": "speaker-notes",
  "distribution": "internal",
  "use_modes": ["live-internal"],
  "practical_review": {
    "transformative_context": "The reaction image comments on the team's own workflow failure.",
    "necessity": "One image supports this specific discussion beat.",
    "amount_resolution": "A low-resolution copy appears once without cropping.",
    "market_substitution": "The slide does not replace demand for the source work.",
    "moral_personality_risk": "No degrading alteration, endorsement implication, or sensitive person.",
    "attribution_method": "speaker-notes",
    "checked_at": "2026-07-25",
    "no_recording_or_distribution": true
  }
}
```
