# Multi-Project Workflow Guide

이 문서는 `jk-boilerplate`를 공통 기반으로 하여 여러 프로젝트(`upbit`, `bithumb`, `kis-ko`, `kis-usa`, `kiwoom`)를 관리하고 동기화하는 방법을 설명합니다.

## 1. 기본 전략: Upstream Remote

모든 프로젝트는 `jk-boilerplate`를 **Upstream(상류)** 저장소로 두고, 각자의 프로젝트를 **Origin(기원)** 저장소로 가집니다.

- **Upstream (`jk-boilerplate`)**: 공통 프레임워크 코드가 관리되는 곳입니다. (`app/utils`, `app/main.py` 등)
- **Origin (`upbit`, `bithumb`...)**: 각 프로젝트의 고유한 비즈니스 로직이 저장되는 곳입니다. (`app/core/` 내의 파일들)

## 2. 프로젝트 초기 설정 (최초 1회)

각 프로젝트(예: `upbit`)를 시작할 때 다음과 같이 설정합니다.

```bash
# 1. Boilerplate Clone
git clone https://github.com/taein2301/jk-boilerplate.git upbit
cd upbit

# 2. Remote 설정 변경
# 기존 origin(boilerplate)을 upstream으로 이름 변경
git remote rename origin upstream

# 3. 내 프로젝트용 새 Repository 연결 (미리 생성 필요)
git remote add origin https://github.com/my-account/upbit.git

# 4. 확인
git remote -v
# origin   https://github.com/my-account/upbit.git (fetch/push)
# upstream https://github.com/taein2301/jk-boilerplate.git (fetch/push)
```

이 과정을 `bithumb`, `kis-ko`, `kis-usa`, `kiwoom` 각각에 대해 반복합니다.

## 3. 개발 및 동기화 워크플로우

### 상황 A: 개별 프로젝트 개발 (예: `upbit` 로직 작성)

`app/core/` 디렉토리에 `upbit` 관련 코드를 작성하고 `origin`에 푸시합니다.

```bash
# upbit 기능 개발
touch app/core/upbit_strategy.py

# 커밋 및 푸시
git add .
git commit -m "Add upbit strategy"
git push origin main
```

### 상황 B: 공통 기능 수정 및 전파 (예: `jk-boilerplate` 업데이트)

`upbit` 개발 중에 `app/utils/logger.py`에 버그가 있어 수정했다고 가정합시다. 이 수정사항을 다른 프로젝트(`bithumb` 등)에도 적용하고 싶습니다.

#### 1. 수정사항을 Upstream에 반영

```bash
# (upbit 프로젝트 내에서)
# 1. 공통 코드 수정 (app/utils/logger.py)
# 2. 커밋
git add app/utils/logger.py
git commit -m "Fix: logger bug in utils"

# 3. Upstream에 푸시 (권한 필요)
git push upstream main
# 4. Origin에도 푸시 (내 프로젝트에도 반영)
git push origin main
```

#### 2. 다른 프로젝트에서 업데이트 받기

이제 `bithumb` 프로젝트로 이동하여 업데이트를 받습니다.

```bash
cd ../bithumb

# 1. Upstream 변경사항 가져오기
git fetch upstream

# 2. 내 코드와 병합
git merge upstream/main

# 3. (충돌 시 해결 후) Origin에 푸시
git push origin main
```

## 4. 구조적 이점

최근 진행한 **Core to Utils 리팩토링**(`app.py`, `batch.py`를 `utils`로 이동) 덕분에 이 구조가 더욱 견고해졌습니다.

- **`app/utils/`**: 공통 영역 (Upstream 관리)
- **`app/core/`**: 프로젝트별 영역 (Origin 관리)

서로의 영역이 명확히 분리되어 있어, `git merge` 시 충돌 가능성이 매우 낮습니다.
