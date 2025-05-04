from fastapi import APIRouter
from pydantic import BaseModel
from app.services.openai_service import get_turf_response

router = APIRouter()

class Query(BaseModel):
    user_input: str

@router.post("/diagnose")
def diagnose(query: Query):
    result = get_turf_response(query.user_input)
    return {"response": result}
