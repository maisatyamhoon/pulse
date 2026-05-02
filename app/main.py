from fastapi import FastAPI
from app.services.qa import answer_question
from pydantic import BaseModel
from app.api.upload import router as upload_router
from app.api.ask import router as ask_router
from app.api.compare import router as compare_router

app = FastAPI(title="Pulse Finance AI")

app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(compare_router)


@app.get("/health")
def health():
    return {"status": "ok"}


class AskRequest(BaseModel):
    records: list
    question: str


@app.post("/ask")
def ask_question(payload: AskRequest):
    answer = answer_question(payload.records, payload.question)
    return {"answer": answer}