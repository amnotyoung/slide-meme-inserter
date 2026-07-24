# Slide Meme Inserter

HTML 슬라이드를 기획·생성하거나 기존 덱을 후처리하면서, 맥락과 청중에 맞는 유명 밈을 절제해 삽입하는 Codex 스킬입니다.

Claude Code와 Codex가 동일한 `SKILL.md`를 사용합니다. 제품별 매니페스트만 분리되어 있어 기능과 규칙이 서로 어긋나지 않습니다.

## 왜 만들었나

AI로 HTML 슬라이드를 만들기 시작하면서 PPT를 직접 만드는 일은 거의 사라졌습니다. 내용 구성도, 디자인도, 수정 속도도 만족스러웠지만 한 가지가 아쉬웠습니다. 발표에서 **나만의 웃음 코드가 사라졌습니다.**

완성된 HTML을 직접 고쳐 밈을 넣을 수는 있습니다. 하지만 사람 마음이 그렇듯, 한 번 귀찮아지면 “이번에는 그냥 빼자”가 되기 쉽습니다. 발표는 매끈해졌지만 점점 덜 나다워졌습니다.

저는 아직 AI가 인간을 따라오지 못하는 영역 중 하나가 **유머**라고 생각합니다. 그래서 AI에게 새로운 농담을 창작시키기보다, 사람들이 이미 알아보는 유명 밈을 넓게 찾고 발표의 맥락·타이밍·청중에 맞춰 제안하고 삽입하도록 이 스킬을 만들었습니다. 최종 웃음 코드와 판단은 여전히 사람의 몫입니다.

## 사용 전후

스킬은 기존 논리와 디자인을 억지로 밈으로 바꾸지 않습니다. 왼쪽의 문제 제시 슬라이드를 그대로 보존하고, 가장 효과적인 지점에 오른쪽과 같은 짧은 밈 브레이크를 추가합니다.

### 사례 1 — 반복 업무의 딜레마

| 사용 전 — 내용은 명확하지만 호흡이 없음 | 사용 후 — 공감되는 유명 밈으로 메시지를 회수 |
|---|---|
| ![밈 삽입 전: 기관마다 다른 양식 때문에 같은 일을 반복한다는 문제를 설명하는 슬라이드](docs/images/before-meme.jpg) | ![밈 삽입 후: 두 버튼 밈으로 어느 기관 양식을 선택해도 다시 작성해야 하는 상황을 표현한 슬라이드](docs/images/after-meme.jpg) |

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

> 예시 템플릿: [Two Buttons](https://imgflip.com/meme/Two-Buttons), [Is This a Pigeon?](https://imgflip.com/meme/Is-This-A-Pigeon), [One Does Not Simply](https://imgflip.com/memetemplate/One-Does-Not-Simply) · Imgflip. 문서용 저해상도 화면 예시이며, 실제 외부 배포 시에는 각 이미지의 이용 권리를 별도로 확인해야 합니다.

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

## 모드

- `postprocess`: 완성된 HTML의 논리와 디자인을 보존하며 밈을 삽입하거나 교체합니다.
- `plan-and-build`: 슬라이드 기획부터 밈의 역할·위치·후보·캡션을 함께 설계하고 HTML을 생성합니다.

사용자가 모드를 지정하면 그대로 따릅니다. 모드가 없으면 기존 HTML이 입력된 경우 `postprocess`, 주제·자료·구성안에서 새 덱을 만드는 경우 `plan-and-build`를 선택합니다.

두 모드 모두 사용자가 직접 제공한 밈 이미지, URL, 템플릿명, 캡션, 희망 위치를 받을 수 있습니다. 제공된 항목은 우선 보존하고, 비어 있는 항목만 스킬이 문맥에 맞게 보완합니다.

## 원칙

- 오리지널 밈보다 청중이 바로 알아보는 기존 밈을 우선합니다.
- 언어권을 제한하지 않고 문맥 적합성과 인지도를 기준으로 선택합니다.
- 밈은 논리를 대신하지 않고 반응, 비유, 콜백, 전환을 돕습니다.
- 이미지 출처와 재사용 상태를 기록하고, 공개 배포 시 권리를 별도로 확인합니다.
- 삽입 후 구조 감사와 실제 브라우저 렌더링을 모두 검증합니다.

## 구조

```text
skills/insert-slide-memes/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── meme-playbook.md
│   ├── plan-and-build.md
│   └── user-provided-memes.md
└── scripts/audit_memes.py
```

생성된 덱과 내려받은 이미지, QA 캡처는 `output/`에 두며 Git에는 포함하지 않습니다.

제품별 배포 메타데이터:

```text
.claude-plugin/  # Claude Code
.codex-plugin/   # Codex
```

## 감사

```bash
python3 skills/insert-slide-memes/scripts/audit_memes.py path/to/deck.html --strict
```

## 라이선스

MIT. 밈 이미지 자체의 권리는 각 원저작자 또는 권리자에게 있으며, 이 저장소의 라이선스가 밈 이미지에 대한 사용 권한을 부여하지는 않습니다.
