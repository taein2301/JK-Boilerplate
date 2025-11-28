# Helper Scripts

이 디렉토리는 개발 편의를 위한 헬퍼 스크립트들을 포함하고 있습니다.

## 사용 가능한 스크립트

### 1. `create_app.sh`

새로운 장기 실행 애플리케이션(App)을 생성하고 자동으로 설정합니다.

**사용법:**
```bash
# Run from project root
./scripts/create_app.sh <app_name>
```

**예시:**
```bash
./scripts/create_app.sh upbit-trader
```

**자동 수행 작업:**
1. `app/core/<app_name>.py` 파일 생성 (snake_case)
   - 케밥 케이스 → snake_case 변환 (예: `upbit-trader` → `upbit_trader.py`)
   - `App` 클래스 상속하는 기본 코드 생성
   - 클래스명은 CamelCase (예: `UpbitTraderApp`)
2. `.env` 파일 생성 (없는 경우 `env.example`에서 복사)
3. `app/main.py`에 라우팅 코드 자동 추가
4. Git commit 및 push
   - GitHub 프라이빗 저장소 자동 생성 (gh CLI 필요)
   - Origin remote 설정 (최초 1회)

**실행 후 바로 사용 가능:**
```bash
uv run app upbit-trader --env dev
```



### 3. `update_main.py`

`app/main.py`에 새 앱 라우팅을 자동 추가하는 Python 헬퍼 스크립트입니다.
(일반적으로 직접 호출할 필요 없음 - `create_app.sh`에서 자동 사용)

## 주의사항

- **케밥 케이스 권장**: 앱 이름은 케밥 케이스(`my-app`)로 지정하세요.
- **자동 변환**: 파일명은 `snake_case`, 클래스명은 `CamelCase`로 자동 변환됩니다.
- **gh CLI 필요**: GitHub 저장소 자동 생성을 사용하려면 `gh` CLI가 설치되어 있어야 합니다.
- **커밋 자동화**: 스크립트가 자동으로 git commit 및 push를 수행하므로, 변경사항을 확인한 후 실행하세요.
