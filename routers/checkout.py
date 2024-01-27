from __future__ import annotations

import datetime
from typing import List
from typing import Optional
from typing import Union

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from models.checkout import CheckoutModel
from routers.books import find_one as find_book
from routers.patrons import find_one as find_patron
from services.orm import ORM

router = APIRouter(prefix='/checkout', tags=['checkouts'])

book_orm = ORM(model='BookModel')
checkout_orm = ORM(model='CheckoutModel')


@router.get('/all', response_description='get all checkouts')
def find_all():
    try:
        checkouts: Union[List[CheckoutModel], None] = checkout_orm.find_all()
        if not len(checkouts) or checkouts is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Checkout Found',
            )
        return checkouts
    except Exception as e:
        raise e


@router.get(
    '/find',
    response_description='get single checkout',
)
def find_one(
    checkout: Optional[int] = None,
    # ===  patron section ===
    patron: Optional[int] = None,
    # ===  book section ===
    book: Optional[int] = None,
    # === is active section ===
    is_active: Optional[int] = None,
):
    """
    usage: :0000/find?book=1&patron=3&is_active=1
    :param checkout:  checkout id
    :param patron:    patron id
    :param book:      book id
    :param is_active: is active?
    :return:
    """
    q_filter: dict = {}
    try:
        if checkout is not None:
            q_filter['checkout'] = checkout
        if patron is not None:
            q_filter['patron'] = patron
        if book is not None:
            q_filter['book'] = book
        if is_active is not None:
            q_filter['is_active'] = is_active
        return checkout_orm.find_one(q_filter=q_filter)
    except Exception as e:
        raise e


@router.post(
    '/new',
    response_description='checkout a book',
)
def checkout_book(patron_id: int, book_id: int):
    """
    usage :0000/new?patron_id=1&book_id=199
    :param patron_id: patron id
    :param book_id:   book id
    :return:
    """

    # find patron
    patron = find_patron(patron=patron_id)
    if patron is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='unable to get patrons',
        )

    # find book
    book = find_book(book=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='unable to get patrons',
        )

    # update book to unavailable
    book.available = False
    book.checkout_date = datetime.datetime.utcnow()
    book_orm.create(book)

    # create checkout
    # class CheckoutModel(BaseModel):
    #     patron_id: int
    #     book_id: int
    #     checkout_date: Optional[datetime] = None

    checkout = CheckoutModel(
        patron_id=patron.id,
        book_id=book.id,
        checkout_date=datetime.datetime.utcnow(),
    )
    # if checkout is exists pass
    is_exists = find_one(patron=patron_id, book=book_id)
    if is_exists:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail=f'a checkout for book with id: {book_id} with patron with id:{patron_id} is already exists..',
        )

    create(checkout)


def create(checkout: CheckoutModel):
    return checkout_orm.create(checkout)
