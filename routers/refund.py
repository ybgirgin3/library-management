from __future__ import annotations

import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from models.book import BookModel
from models.checkout import CheckoutModel
from routers.books import find_one as find_book
from routers.patrons import find_one as find_patron
from services.orm import ORM


router = APIRouter(prefix='/refund', tags=['refund'])

book_orm = ORM(model='BookModel')
checkout_orm = ORM(model='CheckoutModel')


@router.post(
    '/checkout={checkout_id}&patron={patron_id}&book={book_id}',
    response_description='refund a book',
)
def refund(checkout_id: int, patron_id: Optional[int], book_id: Optional[int]):
    # find book
    book = find_book(book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to get book with id: {book_id}',
        )

    # find checkout
    checkout = checkout_orm.find_one(_id=checkout_id)
    if checkout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to find checkout with id: {checkout_id}',
        )

    # update checkout -> set is_active=False
