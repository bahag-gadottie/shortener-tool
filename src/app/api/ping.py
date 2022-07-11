from fastapi import APIRouter
import logging

router = APIRouter()


@router.get("/ping", status_code=200, description="Check if the api is safe and sound")
async def pong():
    logging.info("Api is up and healthy")
    return {"ping": "pong!"}
