from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from app.services.openai_service import get_turf_response
from fastapi.responses import JSONResponse
from app.services.retrieval_service import retrieve_relevant_context, generate_response
from app.services.embedding_service import extract_text_from_pdf, extract_text_from_url, embed_and_store

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

@router.post("/rag-diagnose")
def rag_diagnose(query: Query):
    context = retrieve_relevant_context(query.user_input)
    if not context:
        return {"response": "Sorry, no relevant information found in the knowledge base."}
    result = generate_response(query.user_input, context)
    return {"response": result}

@router.post("/admin/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), source_id: str = Form(...)):
    contents = await file.read()
    with open(f"/tmp/{file.filename}", "wb") as f:
        f.write(contents)

    text = extract_text_from_pdf(f"/tmp/{file.filename}")
    embed_and_store(text, source_id)
    return {"status": "PDF processed and embedded", "source_id": source_id}

@router.post("/admin/load-url")
def load_url(url: str, source_id: str):
    text = extract_text_from_url(url)
    embed_and_store(text, source_id)
    return {"status": "URL processed and embedded", "source_id": source_id}