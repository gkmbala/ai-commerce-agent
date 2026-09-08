from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database import init_db
from .agent import run_agent


app = FastAPI(
    title="SmartShop Agent",
    description="Agentic Commerce POC"
)


class ChatRequest(BaseModel):
    message: str


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = run_agent(request.message)

    return {
        "message": request.message,
        "answer": answer
    }


app.mount(
    "/",
    StaticFiles(
        directory="static",
        html=True
    ),
    name="static"
)