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

User choice does not override safety, accessibility, source honesty, or layout integrity.

A user-provided exact asset may bypass the searched-candidate established-format gate. It does not bypass the presenter-identity, audience clarity, semantic fit, rights, or screenshot tests. Treat explicit provision of an exact fandom or gaming asset as approval of that identity signal for the requested placement only; do not generalize that approval to other slides or future decks.

## Asset handling

### Local or attached image

1. Inspect the image before editing the deck.
2. Preserve the original file.
3. Copy it under a deck-local ASCII filename or embed it when producing a self-contained HTML file.
4. Do not crop, recolor, remove text, or otherwise edit the raster unless requested.
5. Set `data-meme-origin="user-provided"`.
6. Use `data-meme-source="user-provided"` when no verifiable source URL is available.
7. Record reuse status as user-provided and unverified unless the user supplies rights information.

### URL

1. Distinguish a source page from a direct image URL.
2. Download the asset locally; never hotlink it.
3. Preserve the source-page URL in `data-meme-source` when verified.
4. Do not infer permission from accessibility.

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
status: selected
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
source: "user-provided"
rights_status: "user-provided-unverified"
distribution: "internal"
layout: "Requested or inferred layout"
risk: "Concrete audience, identity, rights, or layout risk"
```

Use `status: selected` when the asset and placement are ready. Use `provisional` when required information or permission remains unresolved.

## Delivery

Report:

- which user-supplied fields were preserved
- any inferred caption, placement, or layout
- whether the asset was copied or embedded
- source and reuse status
- any adaptation explicitly approved by the user
