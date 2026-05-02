from fastapi import APIRouter
from pydantic import BaseModel
from app.services.compare_llm import compare_with_llm

router = APIRouter()


class CompareRequest(BaseModel):
    records_a: list
    records_b: list


@router.post("/compare")
async def compare(payload: CompareRequest):
    result = compare_with_llm(payload.records_a, payload.records_b)
    return result