from typing import Any
from fastapi import APIRouter, HTTPException, Path
from app.models import abbreviations
from app.infra import abbreviations as crud

router = APIRouter()


@router.post("/", response_model=Any, status_code=201)
async def create_abbreviation(payload: abbreviations.AbbreviationsSchema):
    abbreviation_id = await crud.post(payload)

    response_object = {
        "id": abbreviation_id,
        "long_term": payload.long_term,
        "abbreviation": payload.abbreviation,
    }
    return response_object


@router.get("/{id}/", response_model=abbreviations.AbbreviationsModel, status_code=200)
async def read_abbreviation(id: int = Path(..., gt=0)):
    abbr = await crud.get(id)
    if not abbr:
        raise HTTPException(status_code=404, detail="Abbreviation not found")
    return abbr
