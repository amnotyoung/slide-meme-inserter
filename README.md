# Slide Meme Inserter

HTML 슬라이드를 기획·생성하거나 기존 덱을 후처리하면서, 맥락과 청중에 맞는 유명 밈을 절제해 삽입하는 Codex 스킬입니다.

Claude Code와 Codex가 동일한 `SKILL.md`를 사용합니다. 제품별 매니페스트만 분리되어 있어 기능과 규칙이 서로 어긋나지 않습니다.

## 사용 전후

스킬은 기존 논리와 디자인을 억지로 밈으로 바꾸지 않습니다. 왼쪽의 문제 제시 슬라이드를 그대로 보존하고, 가장 효과적인 지점에 오른쪽과 같은 짧은 밈 브레이크를 추가합니다.

| 사용 전 — 내용은 명확하지만 호흡이 없음 | 사용 후 — 공감되는 유명 밈으로 메시지를 회수 |
|---|---|
| ![밈 삽입 전: 기관마다 다른 양식 때문에 같은 일을 반복한다는 문제를 설명하는 슬라이드](docs/images/before-meme.jpg) | ![밈 삽입 후: 두 버튼 밈으로 어느 기관 양식을 선택해도 다시 작성해야 하는 상황을 표현한 슬라이드](docs/images/after-meme.jpg) |

이 예시에서는 `Two Buttons`의 익숙한 딜레마 문법을 사용해 “내용은 같은데 양식만 다르다”는 문제를 한눈에 기억하게 만듭니다. 원래 콘텐츠는 삭제하거나 축약하지 않았습니다.

> 예시 템플릿: [Two Buttons · Imgflip](https://imgflip.com/meme/Two-Buttons). 문서용 저해상도 화면 예시이며, 실제 외부 배포 시에는 각 이미지의 이용 권리를 별도로 확인해야 합니다.

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
