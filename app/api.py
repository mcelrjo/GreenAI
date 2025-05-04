from fastapi import APIRouter
from pydantic import BaseModel
from app.services.openai_service import get_turf_response
from fastapi.responses import JSONResponse

router = APIRouter()

class Query(BaseModel):
    user_input: str


@router.options("/diagnose")
def options_handler():
    return JSONResponse(
        content={"message": "CORS preflight passed"},
        headers={
            "Access-Control-Allow-Origin": "https://lawncareassistant.netlify.app",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@router.post("/diagnose")
def diagnose(query: Query):
    try:
        result = get_turf_response(query.user_input)
    except Exception as e:
        print("Error in get_turf_response:", e)
        result = "An error occurred while generating a response."
    return {"response": result}