# Helper Scripts

이 디렉토리는 개발 편의를 위한 헬퍼 스크립트들을 포함하고 있습니다.

## 사용 가능한 스크립트

### 1. `create_app.sh`

새로운 장기 실행 애플리케이션(App)을 생성합니다.

**사용법:**
```bash
# Run from project root
./scripts/create_app.sh <app_name>
# Or use the Python wrapper (requires Python 3.9+)
./scripts/create_app.py <app_name>
```

**예시:**
```bash
./scripts/create_app.sh upbit
```

**동작:**
- `app/core/<app_name>.py` 파일을 생성합니다.
- `app.utils.app.App`을 상속받는 기본 클래스 코드를 작성합니다.
- `app/main.py`에 등록해야 할 코드를 안내합니다.

### 2. `create_batch.sh`

새로운 배치 작업(Batch)을 생성합니다.

**사용법:**
```bash
./scripts/create_batch.sh <batch_name>
```

**예시:**
```bash
./scripts/create_batch.sh my-batch
```

**동작:**
- `app/core/<batch_name>.py` 파일을 생성합니다.
- `app.utils.batch.BatchJob`을 상속받는 기본 클래스 코드를 작성합니다.
- `app/main.py`에 등록해야 할 코드를 안내합니다.
