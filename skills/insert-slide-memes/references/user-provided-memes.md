# User-Provided Meme Contract

Use this reference when the user supplies any part of a meme placement.

## Accepted input

Accept one or more of:

- attached or local image file
- direct image URL or source-page URL
- recognized meme template name
- caption or setup text
- target slide, section, or narrative moment
- layout preference

Do not require every field. Infer non-material omissions from the deck and ask only when an assumption could change the joke, target, rights posture, or presentation structure.

## Precedence

Treat user-supplied fields as locked unless the user invites alternatives:

1. exact image asset
2. target placement
3. caption
4. template name
5. layout preference

Do not silently replace a locked asset with a searched or generated alternative. If it cannot be used safely or legibly, explain the concrete issue and request a replacement or permission to adapt it.

User choice does not override safety, accessibility, source honesty, layout integrity, or the selected rights mode.

A user-provided exact asset may bypass the searched-candidate established-format gate. It does not bypass the presenter-identity, audience clarity, semantic fit, rights, or screenshot tests. Treat explicit provision of an exact fandom or gaming asset as approval of that identity signal for the requested placement only; do not generalize that approval to other slides or future decks.

## Asset handling

### Local or attached image

1. Inspect the image before editing the deck.
2. Preserve the original file.
3. Complete the strict legal basis or practical review required by the selected rights mode before copying or embedding it.
4. Do not crop, recolor, remove text, or otherwise edit the raster unless requested.
5. Set `data-meme-origin="user-provided"`.
6. Set `data-meme-source` to the attribution URL and render the same source at the planned attribution location.
7. Keep the placement provisional until it passes the selected rights mode.

### URL

1. Distinguish a source page from a direct image URL.
2. Verify the mode-appropriate review and intended-use scope; do not infer permission from accessibility.
3. Audit the selected plan, then download the asset locally; never hotlink it.
4. Preserve the attribution URL in `data-meme-source` and the planned attribution.

### Template name only

Treat the named template as locked but search for a suitable source and asset. Ask before switching templates.

## Caption and placement

- Preserve a user-supplied caption unless it creates a material safety, clarity, or reputational problem.
- Avoid duplicating text already baked into the image.
- Honor an explicit target slide when it fits. If it causes overflow or interrupts required instructions, propose the nearest safe placement.
- When placement is not specified, select it using the same narrative criteria as searched memes.
- When caption is not specified, localize one to the deck language and keep it concise.

## Planning record

Add these fields to the meme plan:

```yaml
id: m-user-01
slide_id: s12
status: provisional
origin: user-provided
role: reaction
communicative_job: "Use the supplied reaction at the requested beat"
intended_response: "The user's intended reaction"
template: "User-provided exact asset"
caption: "User-supplied or approved caption"
asset: "/path/or/source-url"
user_locked:
  asset: true
  placement: true
  caption: false
hard_gates:
  established_format: false
  semantic_match: true
  audience_fit: true
  two_second_recognition: true
  caption_clarity: true
  presenter_safe: true
  asset_matches_template: true
identity_signal:
  level: "<none, low, or material>"
  domain: "<fandom or identity domain, or null>"
  user_approved: true
source: "pending"
rights_status: "user-provided-unverified"
distribution: "internal"
layout: "Requested or inferred layout"
risk: "Concrete audience, identity, rights, or layout risk"
```

Use `status: selected` only after adding every field required by [rights-clearance.md](rights-clearance.md) for the plan's rights mode and passing `audit_meme_plan.py --strict`. In practical mode, set `rights_status: practical-reviewed` only for one-off `live-internal` use. Keep unreviewed assets `provisional`.

## Delivery

Report:

- which user-supplied fields were preserved
- any inferred caption, placement, or layout
- whether the asset was copied or embedded
- source, rights mode, legal basis or practical review, intended use modes, and attribution
- any adaptation explicitly approved by the user
