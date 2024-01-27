from __future__ import annotations

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.books import router as book_routers
from routers.checkout import router as checkout_routers
from routers.patrons import router as patron_routers
from routers.refund import router as refund_routers
from services.connection import _create_table
from services.connection import SQL_ALCHEMY_ENGINES

app = FastAPI()

origins = ['*']  # NOTE: for dev purpose allowed all
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

try:
    _create_table('BookSchema', SQL_ALCHEMY_ENGINES['library'])
    _create_table('PatronSchema', SQL_ALCHEMY_ENGINES['library'])
    _create_table('CheckoutSchema', SQL_ALCHEMY_ENGINES['library'])
except:
    pass

app.include_router(book_routers)
app.include_router(patron_routers)
app.include_router(checkout_routers)
app.include_router(refund_routers)
