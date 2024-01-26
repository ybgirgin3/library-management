from fastapi import APIRouter, status, HTTPException
import datetime
from routers.books import find_one as find_book
from routers.patrons import find_one as find_patron
from services.orm import ORM
from models.checkout import CheckoutModel

router = APIRouter(prefix="/checkout", tags=["checkouts"])

book_orm = ORM(model="BookModel")
checkout_orm = ORM(model="CheckoutModel")


@router.post(
    "/patron={patron_id}&book={book_id}", response_description="checkout a book"
)
def checkout_book(patron_id: int, book_id: int):
    # find patron
    patron = find_patron(patron_id=patron_id)
    if patron is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="unable to get patrons"
        )

    # find book
    book = find_book(book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="unable to get patrons"
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
        patron_id=patron.id, book_id=book.id, checkout_date=datetime.datetime.utcnow()
    )
    create(checkout)


def create(checkout: CheckoutModel):
    return checkout_orm.create(checkout)
