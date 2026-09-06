# Plan-and-Build Contract

Use this reference only when planning and generating a new meme-aware HTML deck.

## Contents

- Planning order
- Outline record
- Placement logic
- Candidate commitment
- Plan-to-HTML mapping

## Planning order

Plan in this order:

1. audience and outcome
2. storyline and section sequence
3. slide-level primary messages
4. tension, density, surprise, and transition points
5. provisional humor jobs
6. recognizable meme candidates
7. captions, assets, and layouts

Never choose a meme first and bend the argument around it.

## Outline record

Represent each slide with this minimum structure. It may remain an internal working artifact unless the user requests the plan.

```yaml
- id: s08
  title: "같은 요청이 항상 같은 결과를 만들지는 않습니다"
  narrative_job: "재현성 문제를 체감시킨다"
  primary_message: "AI 출력에는 변동성이 있다"
  evidence:
    - "동일 프롬프트 반복 실행 예시"
  meme:
    status: provisional
    origin: searched
    role: reaction
    intended_response: "우리도 겪었다는 공감"
    search_job: "같은 입력인데 결과가 달라 혼란스러운 상황"
    callback_to: null
    candidates:
      - {template: "<candidate>", discovery_route: imgflip-first, discovery_source: "<imgflip-page-url>", humor_evidence: "<why its active format lands>", semantic_source: "<meaning-source-url>", ecosystem: global}
```

Use `meme: null` when a slide has no humor job. Allowed status values:

- `provisional`: the narrative moment is selected but the asset may change
- `selected`: the asset, caption, source, and layout are ready to build
- `dropped`: the idea failed recognition, tone, rights, or layout review

When the user supplies a meme asset or instruction, add `origin: user-provided` and a `user_locked` map for asset, placement, caption, and layout. Do not run candidate search for a locked exact asset.

After selecting a candidate, store the executable plan as JSON:

```json
{
  "plan_version": 2,
  "audience": "Intended audience",
  "rights_mode": "common-use",
  "placements": [
    {
      "id": "m01",
      "slide_id": "s08",
      "status": "selected",
      "origin": "searched",
      "role": "reaction",
      "callback_to": null,
      "communicative_job": "Release tension after inconsistent results",
      "intended_response": "Shared recognition",
      "template": "Recognized Template",
      "caption": "Localized caption",
      "asset_kind": "meme-template",
      "recognition_basis": "broad-recognition",
      "recognition_evidence": "Documented recurring template use",
      "identity_signal": {
        "level": "none",
        "domain": null,
        "user_approved": false
      },
      "hard_gates": {
        "established_format": true,
        "semantic_match": true,
        "audience_fit": true,
        "two_second_recognition": true,
        "caption_clarity": true,
        "presenter_safe": true,
        "asset_matches_template": true
      },
      "scores": {
        "narrative_value": 2,
        "template_semantics": 2,
        "audience_recognition": 2,
        "novelty_fatigue": 1,
        "caption_clarity": 2,
        "layout_fit": 2,
        "safety_rights": 2
      },
      "score_total": 13,
      "ubiquity_penalty": 0,
      "adjusted_score": 13,
      "discovery_route": "imgflip-first",
      "discovery_source": "https://imgflip.com/meme/Two-Buttons",
      "discovery_fallback_reason": null,
      "humor_evidence": "Current variants preserve a compact either-or dilemma that can be localized to the slide.",
      "semantic_source": "https://example.com/meaning",
      "original_source": null,
      "asset_source": "https://example.com/image.jpg",
      "attribution_text": "Recognized Template — template source page",
      "attribution_url": "https://example.com/template",
      "attribution_location": "credits-slide",
      "source": "https://example.com/template",
      "rights_status": "common-use-unverified",
      "distribution": "public",
      "use_modes": ["public-pdf", "online-publication"],
      "layout": "Sidecar",
      "risk": "Ordinary meme use; license unverified, no concrete issue identified."
    }
  ]
}
```

Use these exact field names. A Markdown table may summarize the plan, but only the JSON plan is passed to `audit_meme_plan.py` and `audit_memes.py`.

This is an illustrative schema, not a sourced asset selection. New plans should
record `rights_mode: common-use`; omission also defaults to common-use in the
auditor. Omit `use_modes` and `distribution` together when delivery is unknown.
Unknown `original_source` may be `null` or omitted. No extra rights-review form is
required. For opt-in strict/practical, use the fields in
[rights-clearance.md](rights-clearance.md).

## Placement logic

Prefer:

- after evidence exposes a shared pain point
- after several dense slides
- immediately before a major section reset
- as a callback once the audience understands the earlier premise

Avoid:

- title and agenda slides
- before the audience understands the setup
- instructions that must be remembered exactly
- slides already carrying dense charts, code, or tables
- predictable spacing such as every fifth slide

Add a dedicated meme slide when the joke needs breathing room. Use a sidecar or corner reaction only when it does not reduce the primary content's legibility.

## Candidate commitment

Keep the humor job provisional while planning the outline. Commit to an exact template only when:

1. the surrounding content is stable enough to define the intended reaction;
2. every hard gate passes;
3. the audience recognition basis is recorded and is not an unsupported assumption;
4. all seven score dimensions are recorded and satisfy the threshold;
5. semantic, original, asset, attribution, and rights fields remain distinct;
6. discovery route, direct discovery page, and concrete humor evidence are recorded, with a fallback reason for a non-Imgflip-first route;
7. common-use has an established meme, source, and honest unverified rights status, or the requested strict/practical review is complete;
8. any material presenter-identity signal has explicit user approval;
9. a callback points to an earlier setup;
10. the layout can survive the target and smaller viewport; and
11. `audit_meme_plan.py --strict` passes.

Drop the meme instead of forcing a weak candidate.

## Plan-to-HTML mapping

- Preserve the outline `id` as the stable slide identifier.
- Map the placement `id` to `data-meme-plan-id`.
- Map `role` to `data-meme-role`.
- Map `template` to `data-meme-template`.
- Map `source` and `attribution_url` to `data-meme-source`.
- Render `attribution_text` as a `.meme-attribution` link to `attribution_url` at `attribution_location`.
- Map `origin` to `data-meme-origin`.
- Put localized punchline text in HTML, not only inside the raster image.
- Keep `alt` text descriptive rather than duplicating the punchline.
- Store downloaded assets under a deck-local path such as `assets/memes/`.
- Embed the image as a Base64 `data:` URL only when producing a self-contained HTML file.
- Keep source metadata even when the image is embedded.

After rendering, update each planned placement to `selected` or `dropped` and report any changed candidate.
