from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.sql import func
metadata = MetaData()

abbreviations_table = Table(
    "abbreviations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("long_term", String(120)), # SAP size
    Column("abbreviation", String(50)),
    Column("assortment", String(40)),
    Column("created_at", DateTime, default=func.now(), nullable=False),
)