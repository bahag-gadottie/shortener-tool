from app.db.db_definitions import database
from app.models import abbreviations
from app.db.abbreviations import abbreviations_table


async def post(payload: abbreviations.AbbreviationsSchema):
    query = abbreviations_table.insert()\
        .values(
            long_term=payload.long_term,
            abbreviation=payload.abbreviation,
            assortment=payload.assortment if payload.assortment else "none"
    )
    return await database.execute(query=query)


async def get(id: int):
    query = abbreviations_table.select().where(id == abbreviations_table.c.id)
    return await database.fetch_one(query=query)
