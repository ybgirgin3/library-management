import datetime
from typing import List
from typing import Optional
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from auth import get_current_user
from auth import User
from models import CheckoutModel
from models import Response
from services.orm import ORM

# from routers.books import find_one as find_book
# from routers.patrons import find_one as find_patron

router = APIRouter(prefix='/checkout', tags=['checkouts'])

book_orm = ORM(model='BookModel')
patron_orm = ORM(model='PatronModel')
checkout_orm = ORM(model='CheckoutModel')


@router.get('/all', response_description='get all checkouts')
def find_all(overdue: Optional[int] = 0, current_user: User = Depends(get_current_user)):
    """
    Retrieve all checkouts.

    Args:
        overdue: Flag indicating whether to retrieve only overdue checkouts.
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing checkouts or error message.
    """

    def _find_overdue(_checkouts: List[CheckoutModel]) -> List[CheckoutModel]:
        today = datetime.datetime.utcnow()
        return [checkout for checkout in checkouts if checkout.refund_date <= today]

    try:
        checkouts: Union[List[CheckoutModel], None] = checkout_orm.find_all()
        if not len(checkouts) or checkouts is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Checkout Found',
            )
        if bool(overdue):
            found = _find_overdue(checkouts)
        else:
            found = checkouts
        return Response(
            status=status.HTTP_200_OK,
            message='All Checkouts Got Successfully',
            data=found,
            reason=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Unable to get checkouts due to {e}',
        )


@router.get(
    '/find',
    response_description='get single checkout',
)
def find_one(
        checkout: Optional[int] = None,
        # ===  patron param ===
        patron: Optional[int] = None,
        # ===  book param ===
        book: Optional[int] = None,
        # === is active param ===
        is_active: Optional[int] = None,
        current_user: User = Depends(get_current_user)
):
    """
    usage: :0000/find?book=1&patron=3&is_active=1
    Retrieve a single checkout.

    Args:
        checkout: Checkout ID.
        patron: Patron ID.
        book: Book ID.
        is_active: Flag indicating whether the checkout is active.
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing the checkout or error message.
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
        checkout = checkout_orm.find_one(q_filter=q_filter)
        return Response(
            status=status.HTTP_200_OK,
            message='checkout found successfully',
            data=checkout,
            reason=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Unable to get checkout due to {e}',
        )


@router.post(
    '/new',
    response_description='checkout a book',
)
def checkout_book(patron_id: int, book_id: int, current_user: User = Depends(get_current_user)):
    """
    usage :0000/new?patron_id=1&book_id=199
    Checkout a book.

    Args:
        patron_id: Patron ID.
        book_id: Book ID.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """

    try:
        is_exists = checkout_orm.find_one(
            {'patron_id': patron_id, 'book_id': book_id})
        if is_exists:
            raise HTTPException(
                status_code=status.HTTP_302_FOUND,
                detail=f'a checkout for book with id: {book_id} with patron with id:{patron_id} is already exists..',
            )

        # find patron
        patron = patron_orm.find_one({'id': patron_id})
        if patron is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='unable to get patrons',
            )

        # find book
        # book = find_book(book=book_id)
        book = book_orm.find_one({'id': book_id})
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
        # is_exists = find_one(patron=patron_id, book=book_id)

        is_created = checkout_orm.create(checkout)
        return Response(
            status=status.HTTP_201_CREATED,
            message='Book Checkout Successfully',
            data=is_created,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to create checkout due to {e}',
        )


@router.post('/seed', response_description='create a overdue checkout')
def create_overdue(checkout: CheckoutModel):
    """
    Create an overdue checkout.

    Args:
        checkout: CheckoutModel object containing checkout details.

    Returns:
        Response: Response object indicating success or failure.
    """
    checkout.checkout_date = datetime.datetime.utcnow()
    checkout.refund_date = datetime.datetime.utcnow()
    create(checkout)


# @router.post(
#     '/create',
#     response_description='create a patron',
#     status_code=status.HTTP_201_CREATED,
# )
def create(checkout: CheckoutModel, current_user: User = Depends(get_current_user)) -> Response:
    """
    Create a checkout.

    Args:
        checkout: CheckoutModel object containing checkout details.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """
    try:
        saved = checkout_orm.create(checkout)
        if saved is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f'unable to create checkout',
            )
        return Response(
            status=status.HTTP_201_CREATED,
            message='Checkout Successfully Created',
            data=saved,
            reason=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to create checkout due to {e}',
        )
