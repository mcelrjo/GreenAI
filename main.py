from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
app = FastAPI(
    title="TurfAI Backend",
    description="Lawncare AI Assistant",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://greenai.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

