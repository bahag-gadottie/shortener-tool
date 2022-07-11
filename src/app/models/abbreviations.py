from pydantic import BaseModel


class AbbreviationsSchema(BaseModel):
    long_term: str
    abbreviation: str
    assortment: str


class AbbreviationsModel(AbbreviationsSchema):
    id: int
