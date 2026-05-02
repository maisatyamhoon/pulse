from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qa import answer_question

router = APIRouter()


class AskRequest(BaseModel):
    records: list
    question: str


@router.post("/ask")
async def ask_pulse(payload: AskRequest):
    answer = answer_question(payload.records, payload.question)
    return {"answer": answer}