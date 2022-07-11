from fastapi import APIRouter, HTTPException, Path
from app.models import notes
from app.api import crud

router = APIRouter()


@router.post("/", response_model=notes.NoteDB, status_code=201)
async def create_note(payload: notes.NoteSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=notes.NoteDB, status_code=200)
async def read_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
