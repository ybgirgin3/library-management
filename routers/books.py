from fastapi import APIRouter, Depends, status
import datetime
from typing import List
from models import BookModel

from services.orm import ORM

router = APIRouter(prefix="/books", tags=["books"])

orm = ORM(model="BookModel")


@router.get(
    "/all", response_description="get all books", status_code=status.HTTP_200_OK
)
def get():
    return orm.find_all()


@router.post(
    "/find/{book_id}", response_description="get a book", status_code=status.HTTP_200_OK
)
def findone(book_id: int):
    pass


@router.get(
    "/create", response_description="create a book", status_code=status.HTTP_201_CREATED
)
def create(book: BookModel):
    return orm.create(book)


@router.put(
    "/update", response_description="update a book", status_code=status.HTTP_200_OK
)
def update(book: BookModel):
    pass


@router.delete(
    "/delete/{book_id}",
    response_description="delete a book",
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(book_id: int):
    pass


# for dev
@router.post("/seed")
def seed_book():
    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    book = BookModel(
        title="Demo Book",
        short_description="A Nice Book",
        author="Yusuf Berkay Girgin",
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    return create(book=book)
