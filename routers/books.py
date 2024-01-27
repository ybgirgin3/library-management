from __future__ import annotations

from typing import List
from typing import Union

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from models import BookModel
from services.orm import ORM

router = APIRouter(prefix='/books', tags=['books'])

orm = ORM(model='BookModel')


@router.get(
    '/all',
    response_description='get all books',
    status_code=status.HTTP_200_OK,
)
def find_all() -> List[BookModel]:
    try:
        books: Union[List[BookModel], None] = orm.find_all()
        if not len(books) or books is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Book found',
            )
        return books
    except Exception as e:
        raise e


@router.post(
    '/find',
    response_description='get a book',
    status_code=status.HTTP_200_OK,
)
def find_one(book: Union[str, int]) -> Union[BookModel, None]:
    """
    usage: :0000/books/find?book=1
    :param book: book id or name
    :return:
    """
    try:
        # NOTE: run find_one value whether param is id or email or name
        key: str = None
        if isinstance(book, int):
            key = 'id'
        elif isinstance(book, str):
            key = 'name'

        q_filter = {key: book, 'available': 1}

        found: Union[BookModel, None] = orm.find_one(q_filter)
        if found is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Book with given id is not found',
            )
        return found
    except Exception as e:
        raise e


@router.get(
    '/create',
    response_description='create a book',
    status_code=status.HTTP_201_CREATED,
)
def create(book: BookModel):
    return orm.create(book)


@router.put(
    '/update',
    response_description='update a book',
    status_code=status.HTTP_200_OK,
)
def update(book: BookModel):
    pass


@router.delete(
    '/delete/{book_id}',
    response_description='delete a book',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(book_id: int):
    pass


# for dev
@router.post('/seed')
def seed_book():
    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    # class BookModel(BaseModel):
    #     title: str
    #     short_description: str
    #     author: str
    #     available: bool

    book = BookModel(
        title='Demo Book 2',
        short_description='A Nice Book 2',
        author='Yusuf Berkay Girgin 2',
        available=True,
        checkout_date=None,
    )
    return create(book=book)
