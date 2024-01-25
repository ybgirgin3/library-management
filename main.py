from dotenv import dotenv_values
from services.connection import _create_table, SQL_ALCHEMY_ENGINES

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.books import router as book_routers

app = FastAPI()

origins = ['*']  # NOTE: for dev purpose allowed all
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

try:
    _create_table("BookSchema", SQL_ALCHEMY_ENGINES["library"])
    _create_table("PatronSchema", SQL_ALCHEMY_ENGINES["library"])
except: pass

app.include_router(book_routers)
