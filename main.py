from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as local_router
from app.api_s3 import router_s3 as s3_router
app = FastAPI(
    title="TurfAI Backend",
    description="Lawncare AI Assistant",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lawncareassistant.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(local_router)
app.include_router(s3_router)

@app.get("/")
def root():
    return {"message": "Backend is live"}
