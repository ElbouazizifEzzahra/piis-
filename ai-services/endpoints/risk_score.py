from fastapi import APIRouter, HTTPException
from mock_data import MOCK_SEGMENTS
from services import calculate_risk_score

router = APIRouter(
    prefix="/ai",
    tags=["Risk Score"]
)

@router.get("/risk-score/{segment_id}")
def get_risk_score(segment_id: str):
    segment = next(
        (s for s in MOCK_SEGMENTS if s.id == segment_id),
        None
    )
    if not segment:
        raise HTTPException(status_code=404, detail="Segment non trouvé")

    result = calculate_risk_score(segment)

    return {
        "segment_id": segment.id,
        "name": segment.name,
        "risk_score": result["risk_score"],
        "status": result["status"],
        "detail": result["detail"]
    }

@router.get("/risk-score-all")
def get_all_scores():
    return [
        {
            "segment_id": s.id,
            "name": s.name,
            "risk_score": calculate_risk_score(s)["risk_score"],
            "status": calculate_risk_score(s)["status"]
        }
        for s in MOCK_SEGMENTS
    ]