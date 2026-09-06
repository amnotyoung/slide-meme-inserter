# Slide Meme Inserter

HTML 슬라이드를 기획·생성하거나 기존 덱을 후처리하면서, 맥락과 청중에 맞는 유명 밈을 절제해 삽입하는 Codex 스킬입니다.

Claude Code와 Codex가 동일한 `SKILL.md`를 사용합니다. 제품별 매니페스트만 분리되어 있어 기능과 규칙이 서로 어긋나지 않습니다.

## 최근 변경

- 한국 밈 정적 이미지 출처 계층과 사용자 제공 이미지 대안을 추가했습니다.
- 특정 유명 밈의 반복 선택을 줄이는 다양성 기준을 추가했습니다.
- 널리 유통되는 인터넷 밈은 `common-use`로 기본 활용합니다. 라이선스 증빙이나 건별 승인을 요구하지 않으며, `strict` 권리 검토는 요청할 때 적용합니다.
- 실제 밈을 적용한 저해상도 전후 사례와 출처·이용 판단 기록을 복원했습니다.
- 글로벌 밈 후보는 Imgflip에서 먼저 찾고, Know Your Meme는 의미·유래 검증에 사용하도록 출처 역할을 분리했습니다.

전체 변경 내역은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

## 왜 만들었나

AI로 HTML 슬라이드를 만들기 시작하면서 PPT를 직접 만드는 일은 거의 사라졌습니다. 내용 구성도, 디자인도, 수정 속도도 만족스러웠지만 한 가지가 아쉬웠습니다. 발표에서 **나만의 웃음 코드가 사라졌습니다.**

완성된 HTML을 직접 고쳐 밈을 넣을 수는 있습니다. 하지만 사람 마음이 그렇듯, 한 번 귀찮아지면 “이번에는 그냥 빼자”가 되기 쉽습니다. 발표는 매끈해졌지만 점점 덜 나다워졌습니다.

저는 아직 AI가 인간을 따라오지 못하는 영역 중 하나가 **유머**라고 생각합니다. 그래서 AI에게 새로운 농담을 창작시키기보다, 사람들이 이미 알아보는 유명 밈을 넓게 찾고 발표의 맥락·타이밍·청중에 맞춰 제안하고 삽입하도록 이 스킬을 만들었습니다. 최종 웃음 코드와 판단은 여전히 사람의 몫입니다.

## 사용 전후

스킬은 기존 논리와 디자인을 억지로 밈으로 바꾸지 않습니다. 왼쪽의 문제 제시 슬라이드를 그대로 보존하고, 가장 효과적인 지점에 오른쪽과 같은 짧은 밈 브레이크를 추가합니다.

### 사례 1 — 반복 업무의 딜레마

| 사용 전 — 내용은 명확하지만 호흡이 없음 | 사용 후 — 공감되는 유명 밈으로 메시지를 회수 |
|---|---|
| ![밈 삽입 전: 기관마다 다른 양식 때문에 같은 일을 반복한다는 문제를 설명하는 슬라이드](docs/images/before-meme.png) | ![밈 삽입 후: 두 버튼 밈으로 어느 기관 양식을 선택해도 다시 작성해야 하는 상황을 표현한 슬라이드](docs/images/after-meme.jpg) |

이 예시에서는 `Two Buttons`의 익숙한 딜레마 문법을 사용해 “내용은 같은데 양식만 다르다”는 문제를 한눈에 기억하게 만듭니다. 원래 콘텐츠는 삭제하거나 축약하지 않았습니다.

### 사례 2 — 챗봇과 에이전트의 차이

| 사용 전 — 개념 차이를 문장으로 설명 | 사용 후 — 익숙한 오인 밈으로 개념을 각인 |
|---|---|
| ![밈 삽입 전: 채팅과 에이전트의 차이를 텍스트로 설명하는 교육 슬라이드](docs/images/wezon-before.jpg) | ![밈 삽입 후: Is This a Pigeon 밈으로 채팅창을 에이전트로 오해하는 상황을 표현한 슬라이드](docs/images/wezon-after.jpg) |

`Is This a Pigeon?`의 “잘못 알아보기” 문법을 사용해 “ChatGPT 채팅창이 곧 에이전트인가?”라는 교육 현장의 흔한 오해를 짧은 질문으로 바꿉니다. 다음 실습으로 넘어가기 전에 청중의 개념을 맞추는 `reaction` 역할입니다.

### 사례 3 — 같은 AI가 자기 작업을 검수할 때

| 사용 전 — 이종 AI 교차검증의 필요성을 설명 | 사용 후 — 불가능에 가까운 자기검수를 밈으로 회수 |
|---|---|
| ![밈 삽입 전: 서로 다른 AI의 관점이 서로 다른 맹점을 잡는다고 설명하는 슬라이드](docs/images/week8-before.jpg) | ![밈 삽입 후: One Does Not Simply 밈으로 자기 초안을 스스로 교차검증하기 어렵다는 점을 표현한 슬라이드](docs/images/week8-after.jpg) |

`One Does Not Simply`의 “말처럼 간단하지 않다”는 문법을 사용해 자기검수의 한계를 회수합니다. 원래 협업 방식 설명은 보존하고, 회고 슬라이드로 넘어가기 직전에 `analogy` 역할의 밈 슬라이드를 추가했습니다.

> **예시 이미지 이용 기록.** 이 파일들은 밈 원본이나 빈 템플릿을 제공하기 위한 것이 아니라, 스킬의 적용 전후와 밈 문법을 설명·비평하는 960×540 슬라이드 화면입니다. 필요한 장면을 슬라이드 구성의 일부로만 사용하고 원본 시장을 대체하지 않는다고 판단하여 `strict` 모드에서 대한민국 저작권법 제28조와 제35조의5의 판단 요소를 검토했으며, 제37조에 따라 아래와 같이 출처를 표시합니다.
>
> - 템플릿·제작 도구: [Two Buttons](https://imgflip.com/meme/Two-Buttons), [Is This a Pigeon?](https://imgflip.com/meme/Is-This-A-Pigeon), [One Does Not Simply](https://imgflip.com/memetemplate/One-Does-Not-Simply) · Imgflip
> - 형식·유래 확인: [Daily Struggle / Two Buttons](https://knowyourmeme.com/memes/daily-struggle-two-buttons), [Is This a Pigeon?](https://knowyourmeme.com/memes/is-this-a-pigeon), [One Does Not Simply Walk into Mordor](https://knowyourmeme.com/memes/one-does-not-simply-walk-into-mordor) · Know Your Meme
> - 법적 판단 기준: [저작권법 제28조·제35조의5·제37조](https://www.law.go.kr/법령/저작권법)
>
> 출처 표시만으로 이용허락이 생기는 것은 아니며, 예외 적용 여부는 구체적인 이용 맥락에 따라 달라집니다. 위 슬라이드에 포함된 제3자 이미지 요소에는 저장소의 MIT 라이선스가 적용되지 않습니다. 권리자가 수정이나 삭제를 요청하려면 [GitHub 이슈](https://github.com/amnotyoung/slide-meme-inserter/issues)를 이용해 주세요.

## 설치

### Claude Code

```text
/plugin marketplace add amnotyoung/slide-meme-inserter
/plugin install slide-meme-inserter@slide-meme-inserter
```

### Codex

Codex에 다음과 같이 요청할 수 있습니다.

```text
Install the insert-slide-memes skill from
https://github.com/amnotyoung/slide-meme-inserter
```

수동 설치 시 저장소의 `skills/insert-slide-memes` 폴더를 Codex 스킬 디렉터리에 복사합니다.

## 두 종류의 모드

이 스킬에는 서로 독립적인 **워크플로 모드**와 **권리 모드**가 있습니다.

### 워크플로 모드

- `postprocess`: 완성된 HTML의 논리와 디자인을 보존하며 밈을 삽입하거나 교체합니다.
- `plan-and-build`: 슬라이드 기획부터 밈의 역할·위치·후보·캡션을 함께 설계하고 HTML을 생성합니다.

사용자가 모드를 지정하면 그대로 따릅니다. 지정하지 않으면 기존 HTML이 있는 경우 `postprocess`, 주제·자료·구성안에서 새 덱을 만드는 경우 `plan-and-build`를 선택합니다.

### 권리 모드

| 모드 | 적용 상황 | 필요한 기록 |
|---|---|---|
| `common-use` **기본값** | 일반적인 인터넷 밈 활용. 내부·고객·유료 발표, 파일 공유, PDF·녹화·공개 게시 포함 | 널리 쓰이는 밈이라는 근거, 실제 출처, `common-use-unverified` 상태 |
| `strict` 선택 사항 | 사용자가 권리 정리된 이미지를 요청하거나 명시된 프로젝트 요건이 있을 때 | 라이선스·허락·퍼블릭도메인 또는 구체적인 법정 예외 검토 |
| `practical` 기존 선택 사항 | 사용자가 일회성 사내 현장 발표용 간이 심사를 명시적으로 요청할 때 | 기존 간이 심사와 무녹화·무배포 확인 |

**남들도 널리 쓰는 밈이면 기본적으로 활용합니다.** 원저작자나 라이선스를 찾지 못했다는 이유만으로 중단하거나, 밈마다 사용자 승인을 다시 받지 않습니다. 공개·고객·유료라는 이유만으로 `strict`으로 전환하지도 않습니다.

이는 사용 방침이며 이용허락이나 분쟁 면제를 뜻하지 않습니다. 출처와 확인 상태를 정직하게 기록하고, 실제 권리자 이의 제기·명시적 이용 제한·허위 보증 암시 같은 구체적인 문제가 발견되면 해당 문제를 다룹니다.

알려진 사용 방식은 `use_modes`에 모두 기록하고 가장 넓은 범위에 맞춰 `distribution`을 정합니다. common-use에서 용도가 미정이면 두 필드를 함께 생략해도 됩니다. 용도를 확정하기 위한 질문 때문에 작업을 멈추지 않습니다. `practical`에서 사용 범위가 넓어지면 일반 밈은 `common-use`, 권리 확인을 요청받았다면 `strict`으로 전환하며 이전 간이 심사가 새 범위까지 포괄한다고 표시하지 않습니다.

> 명령행의 `--strict` 옵션은 경고도 실패로 처리하는 **감사기 실행 옵션**입니다. 계획의 `rights_mode: "strict"`과는 별개입니다.

## 빠른 사용 예시

기존 HTML에 밈을 넣는 경우:

```text
Use $insert-slide-memes in postprocess mode.
Add the supplied meme to slides.html.
```

새 덱을 기획하면서 공개 PDF까지 만들 경우:

```text
Use $insert-slide-memes in plan-and-build mode.
Use familiar internet memes with common-use defaults.
Plan restrained meme beats and build the HTML deck and a public PDF.
```

사용자가 직접 제공한 이미지·URL·템플릿명·캡션·희망 위치는 두 워크플로 모드에서 모두 우선 보존합니다. 비어 있는 항목만 문맥에 맞게 보완합니다. 권리 확인이 필요한 작업은 `Use strict rights mode; use only cleared assets.`처럼 별도로 지정합니다.

## 밈을 찾는 순서

재미있는 후보를 찾는 일과 출처·권리를 검증하는 일을 분리합니다.

1. **Imgflip 우선 탐색:** 글로벌하게 알려진 형식은 Imgflip의 템플릿과 현재 캡션 변주를 먼저 살펴봅니다. 실제로 어떤 리듬과 대비가 웃기는지 비교하되 다른 사용자의 독창적인 캡션을 그대로 복사하지 않습니다.
2. **의미 검증:** 후보를 좁힌 뒤 Know Your Meme 또는 유지되는 맥락 자료로 형식의 통상적 의미와 확산 이력을 확인합니다.
3. **출처 기록:** 실제 이미지와 게시 페이지를 기록하고, 원출처는 확인 가능한 경우에 덧붙입니다. common-use에서는 원출처 미확인이 사용을 막지 않습니다.
4. **사용 모드 적용:** 기본은 `common-use-unverified`로 활용합니다. 엄격한 검토를 요청받은 경우에만 법적 근거나 간이 심사 기록을 추가합니다.

검색 후보의 JSON 계획에는 `discovery_route`, `discovery_source`, `humor_evidence`를 기록합니다. 기본값은 `imgflip-first`입니다. 한국 고유 밈처럼 Imgflip의 대표성이 낮으면 `regional-first`, 적합한 결과가 없으면 `fallback-other`를 사용하고 `discovery_fallback_reason`을 추가합니다.

## 계획의 권리 필드

새 JSON 계획은 루트에 `rights_mode: common-use`를 기록합니다. 생략해도 감사기는 common-use로 처리하며, 기존의 명시적인 strict/practical 계획은 유지합니다. 아래는 관련 필드만 발췌한 예시입니다. 전체 배치 스키마는 [`plan-and-build.md`](skills/insert-slide-memes/references/plan-and-build.md)를 참고하세요.

```json
{
  "plan_version": 2,
  "audience": "사내 교육 참석자",
  "rights_mode": "common-use",
  "placements": [
    {
      "id": "m01",
      "status": "selected",
      "rights_status": "common-use-unverified",
      "asset_kind": "meme-template",
      "recognition_evidence": "같은 양자택일 문법으로 반복되는 템플릿 변주 확인",
      "original_source": null,
      "distribution": "public",
      "use_modes": ["public-pdf"],
      "attribution_location": "credits-slide",
      "attribution_text": "Two Buttons — Imgflip template page",
      "attribution_url": "https://imgflip.com/meme/Two-Buttons",
      "source": "https://imgflip.com/meme/Two-Buttons"
    }
  ]
}
```

권리 상태의 전환은 다음과 같습니다.

- 미심사 사용자 이미지: `status: provisional`, `rights_status: user-provided-unverified`
- 널리 유통되는 밈으로 확인: `status: selected`, `rights_status: common-use-unverified` — 라이선스는 미확인 상태여도 사용
- practical 심사 통과: `status: selected`, `rights_status: practical-reviewed`
- 라이선스·허락·퍼블릭도메인 확인: `status: selected`, `rights_status: cleared`
- 법정 예외 검토 완료: `status: selected`, `rights_status: exception-reviewed`

common-use에는 별도의 `legal_basis`, `practical_review`, `additional_rights` 양식이 필요하지 않습니다. 기존 밈 선택 기록을 사용하며, 미확인 라이선스만으로 경고나 점수 감점을 주지 않습니다. `cleared` 또는 `exception-reviewed`라고 표시하려면 모드와 무관하게 그 근거가 있어야 합니다.

## 출처 위치

- `strict`: `on-slide` 또는 `credits-slide`
- `common-use`와 `practical`: `on-slide`, `credits-slide` 또는 `speaker-notes`

common-use에서는 실제 템플릿·재게시 페이지도 출처로 사용할 수 있습니다. 출처는 크레딧이나 발표자 노트에 모아도 되며, 노트가 빠지는 PDF에는 크레딧을 포함합니다. 재게시자를 원저작자로 표시하거나 확인하지 않은 라이선스를 붙이지 않습니다.

`on-slide` 출처는 해당 `.slide-meme` figure 안에 둡니다. `credits-slide`는 `credits`, `credits-slide`, `references`, `sources` 중 하나의 클래스를 가진 슬라이드에 둡니다. `speaker-notes`는 `speaker-notes` 클래스 또는 `data-speaker-notes` 속성을 가진 요소에 둡니다. figure 밖의 출처 링크에는 `data-meme-plan-id`와 `data-meme-attribution-location`을 기록해야 하며, HTML 감사기가 실제 컨테이너와 계획을 대조합니다.

## 한국 밈 검색의 한계와 대안

한국 밈은 후보명, 의미, 유래와 원영상·원게시물까지 찾을 수 있어도 발표에 바로 삽입할 이미지 파일을 안정적으로 확보하기 어렵습니다.

- Imgflip처럼 템플릿과 원본 이미지가 한곳에 정리된 대표 저장소가 없습니다.
- 검색 결과의 상당수가 커뮤니티 재게시물, 방송·유튜브 캡처 또는 출처가 잘린 이미지입니다.
- 방송사 VOD나 제작자 영상을 찾았더라도 특정 화면을 재사용할 권리가 자동으로 생기지는 않습니다.
- `strict`에서는 원출처 또는 법적 이용 근거를 확인하지 못한 후보가 `provisional` 상태에 머뭅니다.
- 기본 `common-use`에서는 널리 유통되는 실제 짤과 출처를 확보하면 `common-use-unverified`로 활용합니다. 원저작자나 허락 증빙은 필수가 아닙니다.
- `practical`에서는 일회성 사내 현장 발표에 한해 간이 위험심사를 통과한 후보를 `practical-reviewed`로 전환할 수 있습니다.

원하는 짤이 있다면 사용자가 이미지 파일을 직접 제공해도 됩니다. common-use에서는 파일과 밈의 맥락을 확인해 활용합니다. 예를 들어:

```text
my-deck/
├── slides.html
└── meme-input/
    ├── operation-later.jpg
    └── move-on.png
```

Claude Code 또는 Codex에는 다음처럼 요청합니다.

```text
Use $insert-slide-memes to add memes to slides.html.

- ./meme-input/operation-later.jpg
  - 위치: 운영과 유지보수 섹션 앞
  - 캡션: "운영 담당은… 다음에 정하죠."
- ./meme-input/move-on.png
  - 위치: 실패한 실습 결과 다음
  - 캡션: "이 결과는 넘어갈게요."
```

파일명과 위치만 줘도 스킬이 문맥에 맞는 배치를 제안할 수 있습니다. 더 정확한 처리를 원하면 이미지마다 다음 정보를 함께 제공합니다.

- 원본을 찾은 페이지 또는 제작자 URL
- 원하는 슬라이드나 섹션
- 사용할 캡션
- 내부 교육용인지 공개 배포용인지
- 알고 있는 라이선스 또는 사용 허가

스킬은 제공된 원본 파일을 보존하고, 최종 덱의 `assets/memes/` 아래에 ASCII 파일명으로 복사하거나 단일 HTML 요청 시 Base64로 포함합니다. 널리 쓰이는 밈은 라이선스 미확인 상태로도 선택할 수 있으며, strict/practical을 요청한 경우에만 해당 심사를 먼저 수행합니다.

### 한국 밈은 정적 이미지로 가져옵니다

한국 밈은 먼저 밈 형식·의미·청중 인지도·발표자 정체성 위험을 심사합니다. 이 게이트를 모두 통과한 후보만 정적 이미지를 찾습니다. 영상에서 장면을 찾고 캡처하지 않습니다.

1. 정확한 대사나 후보명에 `짤`, `이미지`, `PNG`, `JPG`를 붙여 이미지 검색합니다.
2. 검색 썸네일이 아니라 해당 페이지에 포함된 실제 정적 이미지 URL을 찾습니다.
3. 이미지가 실제 밈 템플릿인지 확인합니다. 문구만 연상되는 월페이퍼·홍보 이미지·팬덤 이미지는 탈락시킵니다.
4. 기본 common-use로 활용하고 실제 출처와 `common-use-unverified` 상태를 기록합니다. strict/practical을 요청받은 경우 해당 검토를 수행합니다.
5. 알려진 현장 발표·공유·공개 범위를 기록합니다. 미정인 용도를 억지로 추정하지 않습니다.
6. 계획 감사를 통과한 뒤에만 JPG·PNG·WebP·GIF 파일을 내려받고 크기와 내용을 확인합니다.
7. 의미 출처, 확인 가능한 원출처, 이미지 URL과 출처 위치를 분리해 기록합니다.
8. 실제 이미지 확보나 문맥 적합성에 문제가 있으면 후보를 보류하거나 교체합니다. common-use에서는 라이선스 미확인만으로 중단하지 않습니다.

사용자가 이미 원하는 짤을 알고 있다면 이미지와 원하는 위치·캡션을 제공하면 됩니다. 출처 URL은 알고 있는 경우 함께 받으며, 필요한 출처는 스킬이 보완합니다. common-use 작업에 별도 허락 증빙을 요구하지 않습니다.

## 선택적인 권리 확인

기본 common-use는 널리 유통되는 밈을 사용하는 작업 방침입니다. 아래 양식은 엄격한 확인을 요청받았거나 실제로 권리 정리가 되었다고 표시할 때 사용합니다.

`strict`의 `selected` 상태에는 다음 중 하나가 필요합니다.

- 라이선스
- 개별 이용허락
- 퍼블릭도메인 근거
- 대한민국 저작권법 제28조 인용, 제35조의5 공정이용 또는 제25조 학교교육 목적 이용에 대한 구체적 검토

`practical`의 `selected` 상태에는 일회성 `live-internal`, 내부 배포, 무녹화·무배포 확인과 간이 위험심사가 필요합니다. 스킬은 사용 범위와 심사 필드의 존재를 감사하지만 법률 의견이나 법원의 판단을 대신하지 않습니다.

각 근거와 심사의 전체 필드는 [`rights-clearance.md`](skills/insert-slide-memes/references/rights-clearance.md)를 참고하세요.

## 원칙

- 오리지널 밈보다 청중이 바로 알아보는 기존 밈을 우선합니다.
- 글로벌 후보는 Imgflip의 활발한 변주에서 먼저 찾고, Know Your Meme는 의미와 유래 검증에 사용합니다.
- 언어권을 제한하지 않고 문맥 적합성과 인지도를 기준으로 선택합니다.
- 월페이퍼·홍보 이미지·팬덤 이미지는 문구가 맞더라도 검색 밈으로 사용하지 않습니다.
- 게임·스포츠·정치 등 발표자의 취향이나 정체성을 암시하는 후보는 청중 근거와 사용자 승인이 없으면 탈락시킵니다.
- 점수 합계 전에 필수 게이트를 적용하며, 적합한 후보가 없으면 밈을 넣지 않습니다.
- 밈은 논리를 대신하지 않고 반응, 비유, 콜백, 전환을 돕습니다.
- 전체 최대 개수는 고정하지 않습니다. 발표 톤과 콘텐츠 길이에 따른 밀도를 소프트 상한으로 사용하고, 밈 사이에는 보통 콘텐츠 슬라이드 5장 이상의 간격을 둡니다.
- 널리 쓰이는 밈은 common-use로 기본 활용하고 출처와 권리 미확인 상태를 기록합니다.
- 외부 발표·공유·녹화·공개를 이유로 자동 차단하거나 strict 검토를 요구하지 않습니다.
- 실제 이용 제한·권리자 이의 제기·허위 보증 암시가 발견되면 그 문제를 구체적으로 다룹니다.
- 삽입 전 계획 감사, 삽입 후 HTML 대조와 실제 브라우저 렌더링을 모두 검증합니다.

## 구조

```text
skills/insert-slide-memes/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── meme-playbook.md
│   ├── plan-and-build.md
│   ├── rights-clearance.md
│   └── user-provided-memes.md
└── scripts/
    ├── audit_meme_plan.py
    └── audit_memes.py
```

생성된 덱과 내려받은 이미지, QA 캡처는 `output/`에 두며 Git에는 포함하지 않습니다.

제품별 배포 메타데이터:

```text
.claude-plugin/  # Claude Code
.codex-plugin/   # Codex
```

## 감사

계획 감사는 모드·상태·사용 범위·심사 필드를 확인하고, HTML 감사는 계획 ID·이미지·접근성·출처 링크와 실제 출처 컨테이너를 대조합니다.

```bash
python3 skills/insert-slide-memes/scripts/audit_meme_plan.py path/to/meme-plan.json --strict
python3 skills/insert-slide-memes/scripts/audit_memes.py \
  path/to/deck.html --plan path/to/meme-plan.json --strict
python3 -m unittest discover -s tests -v
```

## 라이선스

MIT. 템플릿명과 설명은 제3자 밈 이미지에 대한 이용허락을 부여하지 않습니다.
