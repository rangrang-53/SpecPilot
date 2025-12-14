"""FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.presentation.api.routes import session_routes, srs_routes

app = FastAPI(
    title="SpecPilot API",
    description="AI-based SRS Automation Agent",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(session_routes.router)
app.include_router(srs_routes.router)


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "Welcome to SpecPilot API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "healthy"}
