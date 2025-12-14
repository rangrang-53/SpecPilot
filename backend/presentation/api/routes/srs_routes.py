"""SRS Routes"""
from fastapi import APIRouter, HTTPException, Query
from backend.presentation.api.schemas.response_schemas import SRSResponse
from backend.application.use_cases.get_srs_use_case import GetSRSUseCase

router = APIRouter(prefix="/api/srs", tags=["srs"])


@router.get("/{session_id}", response_model=SRSResponse)
def get_srs(
    session_id: str,
    format: str = Query("json", description="문서 형식 (json, markdown)")
):
    """SRS 문서 조회"""
    use_case = GetSRSUseCase()
    result = use_case.execute(session_id, format)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return SRSResponse(**result)
