from __future__ import annotations

import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from models import Response
from routers.books import find_one as find_book
from services.orm import ORM


router = APIRouter(prefix='/refund', tags=['refund'])

book_orm = ORM(model='BookModel')
checkout_orm = ORM(model='CheckoutModel')


@router.post(
    '/',
    response_description='refund a book',
)
def refund(checkout_id: int, patron_id: Optional[int], book_id: Optional[int]) -> Response:
    try:
        # create query filter
        # search for unavailable books
        q_filter: dict = {'checkout_id': checkout_id,
                          'patron_id': patron_id, 'book_id': book_id, 'is_active': 1}

        # find checkout
        checkout = checkout_orm.find_one(q_filter=q_filter)
        if checkout is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'unable to get checkout with id: {checkout_id}',
            )

        # find book
        book = book_orm.find_one({'book_id': book_id})
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'unable to get book with id: {book_id}',
            )

        # update checkout -> set is_active=False
        checkout.is_active = False
        book.available = True

        checkout_orm.create(checkout)
        book_orm.create(book)

        return Response(
            status=status.HTTP_200_OK,
            message=f'Book Successfully Refunded',
            data=None,
            reason=None
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'unable to perform refund due to :{e}',
        )
