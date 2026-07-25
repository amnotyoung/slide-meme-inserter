# Rights Clearance Contract

Use this contract before downloading, copying, embedding, or inserting any meme asset. Recording a source or limiting a deck to an internal audience does not itself authorize use.

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

### `strict`

Use strict mode whenever the deck may be shared as a file, presented to clients,
used at a paid event, exported, recorded, or published. It is also the default when
the delivery context is unknown. A selected placement must use one of the legal
bases below.

### `practical`

Practical mode is a limited operational risk screen for a one-off internal live
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
court result. If any practical constraint changes, switch the plan to strict and
clear every selected asset again.

## Selection rule

In strict mode, a placement may be `selected` only when it has one documented
legal basis:

- `license`
- `permission`
- `public-domain`
- `quotation-art-28`
- `fair-use-art-35-5`
- `school-education-art-25`

Use the statutory-exception labels only for a Korean-law analysis. Record another jurisdiction in `jurisdiction` and use a licensed or permitted asset when the applicable exception has not been reviewed.

Use `rights_status: "cleared"` for a license, permission, or public-domain basis. Use `rights_status: "exception-reviewed"` for a reviewed statutory exception. In practical mode only, use `rights_status: "practical-reviewed"` after completing the compact review above. Keep `unclear` and `user-provided-unverified` placements `provisional` or `dropped`.

The audit verifies that evidence and analysis fields exist. It does not certify that a license is authentic or that a court would accept a statutory exception.

## Intended use modes

Record every planned use:

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

Adding a use mode later requires a new scope check. A live-only permission does not authorize PDF distribution or recording.

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

Review and explain:

- `moral_rights`: use `not-modified`, `permitted`, or `reviewed`
- `portrait_publicity`: use `not-applicable`, `permission`, or `reviewed`
- `trademark`: use `not-applicable`, `permission`, `descriptive-use`, or `reviewed`

Do not imply endorsement, partnership, or a person's recommendation. Do not materially distort an original or combine an identifiable person with degrading, sexual, political, or promotional messaging without a documented basis.

## Attribution

Keep discovery, semantic history, original provenance, asset location, legal evidence, and attribution separate.

Record:

- `attribution_text`: creator, work, source, and license text appropriate to the use
- `attribution_url`: the creator-controlled, publisher-controlled, or license-required source
- `source`: the same value as `attribution_url` for HTML mapping

Record `attribution_location`:

- `on-slide` or `credits-slide` in strict mode
- `on-slide`, `credits-slide`, or `speaker-notes` in practical mode

Render `attribution_text` as a link with class `meme-attribution`. An on-slide link
belongs inside the meme figure. A credits or speaker-notes link belongs outside the
figure and must carry both `data-meme-plan-id` and
`data-meme-attribution-location`. A hidden `data-meme-source` attribute,
`user-provided`, `source: internet`, or an aggregator link is not sufficient.

Put a credits link in a slide classed as `credits`, `credits-slide`, `references`,
or `sources`. Put a speaker-notes link in an element with class `speaker-notes` or
the `data-speaker-notes` attribute. The HTML audit checks these containers.

## Examples

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
