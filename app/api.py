from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel
from app.services.openai_service import get_turf_response
from fastapi.responses import JSONResponse
from app.services.retrieval_service import retrieve_relevant_context, generate_response
from app.services.embedding_service import extract_text_from_pdf, extract_text_from_url, embed_and_store
from app.services.conversation_service import get_session_messages, add_message, clear_session
from app.services.image_service import handle_image_diagnosis
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
@router.post("/diagnose")
def diagnose(query: Query, session_id: str = "default"):
    result = get_turf_response(query.user_input, session_id)
    return {"response": result}

@router.post("/admin/reset-session")
def reset_session(session_id: str = "default"):
    clear_session(session_id)
    return {"status": f"Session '{session_id}' has been cleared."}

@router.post("/rag-diagnose")
def rag_diagnose(query: Query):
    context = retrieve_relevant_context(query.user_input)
    if not context:
        return {"response": "Sorry, no relevant information found in the knowledge base."}
    result = generate_response(query.user_input, context)
    return {"response": result}

@router.post("/admin/upload-pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source_id: str = Form(...)
):
    contents = await file.read()
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Schedule background processing
    background_tasks.add_task(process_pdf_background, temp_path, source_id)

    return {"status": "PDF received and processing started", "source_id": source_id}

def process_pdf_background(temp_path: str, source_id: str):
    text = extract_text_from_pdf(temp_path)
    embed_and_store(text, source_id)

@router.post("/admin/load-url")
def load_url(url: str, source_id: str):
    text = extract_text_from_url(url)
    embed_and_store(text, source_id)
    return {"status": "URL processed and embedded", "source_id": source_id}

@router.post("/diagnose-image")
async def diagnose_image(file: UploadFile = File(...)):
    # this is where you'll call a helper function
    result = await handle_image_diagnosis(file)
    return {"response": result}
