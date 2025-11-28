# JK Boilerplate

이 프로젝트는 확장 가능한 Python 애플리케이션을 구축하기 위한 범용 템플릿입니다.

자세한 내용은 [프레임워크 가이드](docs/framework_guide.md)를 참조하세요.
현대적인 Python 스택(Typer, Pydantic, Loguru)을 기반으로 하며, 확장 가능한 구조를 제공합니다.

## 🚀 주요 기능

- **통합 CLI**: `Typer` 기반의 직관적인 커맨드 라인 인터페이스 (`app start`)
- **강력한 설정 관리**: `Pydantic Settings`를 이용한 타입 안전한 설정 및 `.env` 지원
- **구조화된 로깅**: `Loguru`를 이용한 컬러풀하고 상세한 로깅
- **모듈화된 구조**: 비즈니스 로직(`core`), 외부 서비스(`services`), 유틸리티(`utils`)의 명확한 분리
- **기본 내장 서비스**: Supabase, Telegram 연동 모듈 포함

## 🛠 설치 및 실행 (Installation & Usage)

### 1. uv 설치 및 프로젝트 설정

이 프로젝트는 [uv](https://github.com/astral-sh/uv)를 사용하여 의존성을 관리합니다.

```bash
# uv 설치 (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경 생성 및 의존성 동기화
uv venv
uv pip install -e .
```

### 2. 환경 설정

`.env` 파일을 생성하여 필요한 설정을 입력합니다.

```ini
# .env 예시
APP_ENV=dev
APP_NAME=my-awesome-app
LOG_LEVEL=INFO

# Telegram (선택사항)
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Supabase (선택사항)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 3. 실행 방법

`uv run`을 사용하여 등록된 스크립트(`app`, `batch`)를 실행합니다.

**도움말 확인:**
```bash
uv run app --help

```

**장기 실행 앱 시작 (예: my-app):**
```bash
uv run app my-app --env dev
```

**파라미터 설명:**
- `my-app`: 실행할 앱의 이름입니다. (코드 내 `app_name` 인자와 매핑됨)
- `--env`: 실행 환경을 지정합니다. (`dev` 또는 `prod`, 기본값: `.env` 파일 설정)



## 📦 다른 프로젝트에서 사용하기 (How to Reuse)

이 템플릿을 기반으로 새로운 프로젝트를 시작하려면 다음 절차를 따르세요.

1.  **템플릿 복사**: 이 저장소를 새로운 프로젝트 디렉토리로 복사합니다.
    ```bash
    git clone <this-repo-url> new-project
    cd new-project
    rm -rf .git  # 기존 git 히스토리 제거
    git init     # 새로운 git 초기화
    ```

2.  **프로젝트 정보 수정**: `pyproject.toml`에서 `name`, `description`, `authors` 정보를 수정합니다.
    ```toml
    [project]
    name = "new-project-name"
    # ...
    ```

3.  **비즈니스 로직 구현**:
    - **앱(App)**: `app/core/` 디렉토리에 새로운 앱 로직을 구현합니다 (예: `app/core/my_app.py`).
    - **배치(Batch)**: `app/core/` 디렉토리에 새로운 배치 로직을 구현합니다.

4.  **CLI 등록**: `app/main.py`를 수정하여 새로 만든 앱/배치를 연결합니다.
    ```python
    # app/main.py
    @app.command()
    def start(app_name: str, ...):
        if app_name == "my-new-app":
            from app.core.my_app import MyApp
            MyApp().run()
    ```

5.  **의존성 추가**: 필요한 라이브러리가 있다면 `pyproject.toml`의 `dependencies`에 추가하고 설치합니다.

## 📂 프로젝트 구조

```
.
├── app/
│   ├── main.py          # CLI 진입점
│   ├── config.py        # 설정 관리 (Pydantic)
│   ├── core/            # 핵심 비즈니스 로직 구현 위치
│   ├── services/        # 외부 서비스 연동 (Telegram, Supabase 등)
│   └── utils/           # 공통 유틸리티
├── config/              # YAML 설정 파일 (선택사항)
├── pyproject.toml       # 프로젝트 메타데이터 및 의존성
└── README.md            # 문서
```
