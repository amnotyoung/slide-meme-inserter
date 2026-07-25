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
    candidates:
      - {template: "<global candidate 1>", source: "<verified-source-url>", ecosystem: global}
      - {template: "<global candidate 2>", source: "<verified-source-url>", ecosystem: global}
      - {template: "<regional candidate 1>", source: "<verified-source-url>", ecosystem: regional}
      - {template: "<regional candidate 2>", source: "<verified-source-url>", ecosystem: regional}
      - {template: "<professional candidate 1>", source: "<verified-source-url>", ecosystem: professional}
      - {template: "<professional candidate 2>", source: "<verified-source-url>", ecosystem: professional}
    score: "13/14"
    ubiquity_penalty: 0
    adjusted_score: "13/14"
    selected: "<highest-adjusted-score candidate>"
    selection_reason: "이 청중에게 신선하면서도 의미가 가장 정확하다"
    caption: "프롬프트는 같았는데 정답이 세 개입니다"
    source: "<verified-source-url>"
    reuse_status: "rights unclear; internal-use warning"
    layout: "content slide 다음의 독립 section bumper"
    risk: "낮음; 개인이나 부서를 조롱하지 않음"
```

Use `meme: null` when a slide has no humor job. Allowed status values:

- `provisional`: the narrative moment is selected but the asset may change
- `selected`: the asset, caption, source, and layout are ready to build
- `dropped`: the idea failed recognition, tone, rights, or layout review

When the user supplies a meme asset or instruction, add `origin: user-provided` and a `user_locked` map for asset, placement, caption, and layout. Do not run candidate search for a locked exact asset.

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
2. the audience is likely to recognize it within two seconds;
3. its established meaning matches the message;
4. the caption works without explaining the template;
5. the asset source and reuse status are recorded; and
6. the candidate slate contains concrete, sourced options from the required ecosystems;
7. novelty/fatigue and any ubiquity penalty have been recorded; and
8. the layout can survive the target and smaller viewport.

Drop the meme instead of forcing a weak candidate.

## Plan-to-HTML mapping

- Preserve the outline `id` as the stable slide identifier.
- Map `role` to `data-meme-role`.
- Map `source` to `data-meme-source`.
- Map `origin` to `data-meme-origin`.
- Put localized punchline text in HTML, not only inside the raster image.
- Keep `alt` text descriptive rather than duplicating the punchline.
- Store downloaded assets under a deck-local path such as `assets/memes/`.
- Embed the image as a Base64 `data:` URL only when producing a self-contained HTML file.
- Keep source metadata even when the image is embedded.

After rendering, update each planned placement to `selected` or `dropped` and report any changed candidate.
