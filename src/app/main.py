# -*- coding: utf-8 -*-
# based on: https://testdriven.io/blog/fastapi-crud/

from fastapi import FastAPI
import os
import sys
sys.path.append(os.getcwd())
from app.api import abbreviations, ping
from app.db.db import database, engine, metadata

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(abbreviations.router, prefix="/abbreviations", tags=["abbreviations"])
