import os
import sys
import logging

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)

from databases import Database

# TODO: improve the way I handle different environments
# with open('/Users/gadotte/bahag/shortener-tool/src/.env') as f:
#     param_list = f.read().split('\n')
#     kv_params = {}
#     [kv_params.update({x.split('=')[0]:x.split('=')[1]})
#         for x in param_list]
#
# if "DATABASE_URL" in kv_params.keys():
#     DATABASE_URL = kv_params["DATABASE_URL"]
# else:
#     DATABASE_URL = os.getenv("DATABASE_URL")

# docker
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # localhost:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:54320/shortener_db"

logging.warning(f'\n\n\nLogged in with the following database_url: "{DATABASE_URL}"')


# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# databases query builder
database = Database(DATABASE_URL)
