from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="TurfAI Backend",
    description="API for Turfgrass GenAI Assistant",
    version="0.1"
)

app.include_router(router)
