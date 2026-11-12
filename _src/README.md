# K&2P 홈페이지 소스

정적 HTML 사이트(GitHub Pages). 한국어는 루트, 영어는 `/en/`, 일본어는 `/ja/`.

## 문구 수정
1. `_src/content.py`에서 해당 언어 문구를 고친다 (ko가 원문, en/ja는 번역).
2. `python3 _src/build.py` 실행 → 12개 페이지와 `404.html`, `robots.txt`, `sitemap.xml`, `llms.txt`가 다시 생성된다 (Python 3.9 이상, 외부 패키지 불필요).
3. 생성된 파일을 `_src/content.py`와 함께 커밋한다.

생성된 HTML을 직접 고치면 다음 빌드 때 덮어써진다.

## 로컬 미리보기
저장소 루트에서 `python3 -m http.server 8000` 실행 후 http://localhost:8000 을 연다.

## 배포
GitHub Pages가 `main` 브랜치 루트를 그대로 서비스한다(`CNAME` = kn2p.co.kr). 작업 브랜치에서 PR을 만들고 `main`에 병합하면 몇 분 안에 반영된다. 되돌릴 때는 병합된 PR의 Revert를 쓴다. `_src/`는 Jekyll 규칙(밑줄 폴더 제외)에 따라 공개되지 않는다.

## 아이콘
Google Material Symbols를 쓴다. 빌드할 때 페이지에 쓰인 아이콘 이름만 모아 폰트 요청(`icon_names=`)에 넣으므로, `build.py`의 `icon("이름")`으로 추가하면 자동 반영된다.

## 디자인
- [Astryx](https://github.com/meta/astryx) (Meta, MIT) 디자인 시스템의 토큰·테마 체계를 사용한다.
  - `assets/css/kn2p-theme.css`: `astryx theme build`로 생성한 K&2P 테마 (시드 색: MoriPay 블루 `#029ED9`)
  - `assets/css/astryx-tokens.css`, `astryx-reset.css`: Astryx core의 기본 토큰과 리셋
  - 재생성: `_src/build_astryx_tokens.sh` (Node 필요)
- Astryx 컴포넌트는 React 19 기반이라 쓰지 않았다. 회사 소개 사이트는 정적 HTML이 SEO·속도·운영 면에서 낫기 때문이다.
- `assets/css/site.css`: 페이지 레이아웃. 브랜드 색은 로고(빨강 `#DB3528`, 회색 `#737D81`)와 MoriPay 카드 그라데이션(`#029ED9 → #98D4C8`)에서 가져왔다.

## 약관 (microCMS 연동)
서비스 이용약관·외국인 서비스 이용약관·개인정보처리방침(한·영·일)은 microCMS(`moripay-production` 서비스, `terms` API)에서 가져와 `/legal/`, `/en/legal/`, `/ja/legal/` 페이지로 만든다. 콘텐츠 ID는 `_src/content.py`의 `LEGAL_DOCS`에 있다.

1. 처음 한 번: GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret, 이름 `MICROCMS_API_KEY`, 값은 microCMS의 GET 전용 API 키.
2. microCMS에서 약관을 고친 뒤: 저장소 Actions 탭 → "Update legal pages" → Run workflow. 약관을 받아 `_src/legal/*.json`에 저장하고 사이트를 다시 빌드해 `main`에 커밋한다(=운영 반영). 바뀐 내용이 없으면 커밋하지 않는다.
3. 로컬에서 받으려면 `MICROCMS_API_KEY=키 python3 _src/fetch_legal.py && python3 _src/build.py`. 키는 저장소나 파일에 적지 않는다.

받은 적 없는 문서는 페이지를 만들지 않고, 푸터에서 moripay.com의 해당 약관으로 연결한다. 본문 HTML은 `_src/sanitize.py`가 허용 목록 방식으로 정리한다(스크립트·iframe·인라인 스타일 제거).
