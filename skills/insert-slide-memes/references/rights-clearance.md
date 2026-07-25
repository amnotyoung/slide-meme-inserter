# Rights Clearance Contract

Use this contract before downloading, copying, embedding, or inserting any meme asset. Recording a source or limiting a deck to an internal audience does not itself authorize use.

## Contents

- Selection rule
- Intended use modes
- Clearance evidence
- Statutory-exception analysis
- Additional rights
- Attribution
- Example

## Selection rule

A placement may be `selected` only when it has one documented legal basis:

- `license`
- `permission`
- `public-domain`
- `quotation-art-28`
- `fair-use-art-35-5`
- `school-education-art-25`

Use the statutory-exception labels only for a Korean-law analysis. Record another jurisdiction in `jurisdiction` and use a licensed or permitted asset when the applicable exception has not been reviewed.

Use `rights_status: "cleared"` for a license, permission, or public-domain basis. Use `rights_status: "exception-reviewed"` for a reviewed statutory exception. Keep `unclear` and `user-provided-unverified` placements `provisional` or `dropped`; they may not be copied into the deck for internal use.

The audit verifies that evidence and analysis fields exist. It does not certify that a license is authentic or that a court would accept a statutory exception.

## Intended use modes

Record every planned use:

- `live-internal`
- `internal-file-share`
- `live-client`
- `paid-event`
- `public-pdf`
- `public-recording`
- `online-publication`

Set `distribution` to:

- `internal` for internal-only modes
- `external-limited` when `live-client` or `paid-event` is the broadest mode
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

- `attribution_text`: visible creator, work, source, and license text appropriate to the use
- `attribution_url`: the creator-controlled, publisher-controlled, or license-required source
- `source`: the same value as `attribution_url` for HTML mapping

Render `attribution_text` as a visible link with class `meme-attribution` inside the meme figure. A hidden `data-meme-source` attribute, `user-provided`, `source: internet`, or an aggregator link is not sufficient attribution.

## Example

```json
{
  "rights_status": "cleared",
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
