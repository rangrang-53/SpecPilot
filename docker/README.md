# Docker 배포 (선택사항)

Docker를 사용한 배포가 필요한 경우 이 폴더의 파일들을 사용하세요.

## 사용 방법

### 1. Docker 파일 루트로 복사
```bash
cp docker/Dockerfile.backend ./
cp docker/Dockerfile.frontend ./
cp docker/docker-compose.yml ./
```

### 2. Docker Compose 실행
```bash
# 전체 스택 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 종료
docker-compose down
```

## 파일 설명

- **Dockerfile.backend**: FastAPI 백엔드 컨테이너
- **Dockerfile.frontend**: Streamlit 프론트엔드 컨테이너
- **docker-compose.yml**: 전체 스택 오케스트레이션

## 환경 변수

`.env` 파일에 다음 환경 변수를 설정하세요:
```
GOOGLE_API_KEY=your-google-api-key-here
MODEL_NAME=gemini-3-pro
```

## 참고

Streamlit Community Cloud 배포 시에는 Docker 파일이 필요 없습니다.
로컬 개발이나 자체 서버 배포 시에만 사용하세요.
