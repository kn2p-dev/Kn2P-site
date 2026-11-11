# K&2P 홈페이지 소스

정적 HTML 사이트(GitHub Pages). 한국어는 루트, 영어는 `/en/`, 일본어는 `/ja/`.

## 문구 수정
1. `_src/content.py`에서 해당 언어 문구를 고친다 (ko가 원문, en/ja는 번역).
2. `python3 _src/build.py` 실행 → 12개 HTML이 다시 생성된다 (외부 패키지 불필요).
3. 생성된 `*.html`, `en/*.html`, `ja/*.html`을 함께 커밋한다.

생성된 HTML을 직접 고치면 다음 빌드 때 덮어써진다.

## 디자인
- [Astryx](https://github.com/meta/astryx) (Meta, MIT) 디자인 시스템의 토큰·테마 체계를 사용한다.
  - `assets/css/kn2p-theme.css`: `astryx theme build`로 생성한 K&2P 테마 (시드 색: MoriPay 블루 `#029ED9`)
  - `assets/css/astryx-tokens.css`, `astryx-reset.css`: Astryx core의 기본 토큰과 리셋
  - 재생성: `_src/build_astryx_tokens.sh` (Node 필요)
- Astryx 컴포넌트는 React 19 기반이라 쓰지 않았다. 회사 소개 사이트는 정적 HTML이 SEO·속도·운영 면에서 낫기 때문이다.
- `assets/css/site.css`: 페이지 레이아웃. 브랜드 색은 로고(빨강 `#DB3528`, 회색 `#737D81`)와 MoriPay 카드 그라데이션(`#029ED9 → #98D4C8`)에서 가져왔다.
