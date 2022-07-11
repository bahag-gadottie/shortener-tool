from app.db.db import database
from app.models import notes
from app.db.notes import notes_table


async def post(payload: notes.NoteSchema):
    query = notes_table.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = notes_table.select().where(id == notes_table.c.id)
    return await database.fetch_one(query=query)
