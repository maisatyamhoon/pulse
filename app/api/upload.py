from fastapi import APIRouter, UploadFile, File, Form
from app.parsers.router import parse_file
from app.services.ingest import enrich_transactions
from app.services.insights import generate_insights
from app.services.recommend import generate_recommendations
from app.services.score import generate_financial_score

router = APIRouter()


@router.post("/upload")
async def upload_statement(
    file: UploadFile = File(...),
    password: str = Form(default="")
):
    try:
        file_bytes = await file.read()

        records = parse_file(file_bytes, password=password or None)


        records = enrich_transactions(records)

        insights = generate_insights(records)
        recommendations = generate_recommendations(records)
        score = generate_financial_score(records)

        return {
            "records": records,
            "insights": insights,
            "recommendations": recommendations,
            "score": score
        }

    except Exception as e:
        return {
            "error": str(e)
        }