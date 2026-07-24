# Slide Meme Inserter

기존 HTML 슬라이드에 맥락과 청중에 맞는 유명 밈을 절제해 삽입하는 Codex 스킬입니다.

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
├── references/meme-playbook.md
└── scripts/audit_memes.py
```

생성된 덱과 내려받은 이미지, QA 캡처는 `output/`에 두며 Git에는 포함하지 않습니다.

## 감사

```bash
python3 skills/insert-slide-memes/scripts/audit_memes.py path/to/deck.html --strict
```
