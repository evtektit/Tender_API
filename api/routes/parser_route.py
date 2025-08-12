from fastapi import APIRouter
from api.schemas import ParseRequest, ParseResponse
from parser.run_all import run_all  # важно: у нас run_all — async

router = APIRouter(tags=["parser"])

@router.post("/parse", response_model=ParseResponse)
async def parse(req: ParseRequest):
    data = await run_all(req.query, req.sources, req.limit)
    return ParseResponse(**data)
