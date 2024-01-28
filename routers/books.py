from typing import List
from typing import Optional
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from auth import get_current_user
from auth import User
from models import BookModel
from models import Response
from services.orm import ORM

router = APIRouter(prefix='/books', tags=['books'])

orm = ORM(model='BookModel')


@router.get(
    '/all',
    response_description='get all books',
    status_code=status.HTTP_200_OK,
    # response_model=Response
)
def find_all(current_user: User = Depends(get_current_user)) -> Response:
    """
    Retrieve all books.

    Args:
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing books or error message.
    """
    try:
        books: Union[List[BookModel], None] = orm.find_all()
        if not len(books) or books is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'unable to find books',
            )
        return Response(
            status=status.HTTP_200_OK,
            message='Books successfully found',
            data=books,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to find checkout due to {e}',
        )


@router.get(
    '/find',
    response_description='get a book',
    status_code=status.HTTP_200_OK,
)
def find_one(book: Union[str, int], available: Optional[int] = 1,
             current_user: User = Depends(get_current_user)) -> Response:
    """
    Retrieve a book by ID or name.

    Args:
        book: Book ID or name.
        available: Flag indicating if the book is available.
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing the book or error message.
    """
    try:
        # NOTE: run find_one value whether param is id or email or name
        key: str = None
        if isinstance(book, int) or book.isnumeric():
            key = 'id'
        elif isinstance(book, str):
            key = 'name'

        q_filter = {key: book, 'available': bool(available)}

        found: Union[BookModel, None] = orm.find_one(q_filter)
        if found is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'no book found',
            )

        return Response(
            status=status.HTTP_200_OK,
            message=f'Book with {key}: {book} successfully found',
            data=found,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'unable to find book due to {e}',
        )


@router.get(
    '/create',
    response_description='create a book',
    status_code=status.HTTP_201_CREATED,
)
def create(book: BookModel, current_user: User = Depends(get_current_user)) -> Response:
    """
    Create a new book.

    Args:
        book: BookModel object containing book details.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """
    try:
        saved = orm.create(book)
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
            detail=f'unable to create book due to {e}',
        )


@router.put(
    '/update',
    response_description='update a book',
    status_code=status.HTTP_200_OK,
)
def update(book: BookModel, current_user: User = Depends(get_current_user)):
    """
    Update an existing book.

    Args:
        book: BookModel object containing updated book details.
        current_user: The current authenticated user.
    """
    pass


@router.delete(
    '/delete/{book_id}',
    response_description='delete a book',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(book_id: int, current_user: User = Depends(get_current_user)):
    """
    Delete a book by ID.

    Args:
        book_id: The ID of the book to be deleted.
        current_user: The current authenticated user.
    """
    pass


# for dev
@router.post('/seed')
def seed_book(book: BookModel, current_user: User = Depends(get_current_user)):
    """
    Seed a book.

    Args:
        book: BookModel object containing book details.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """

    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    # class BookModel(BaseModel):
    #     title: str
    #     short_description: str
    #     author: str
    #     available: bool

    # book = BookModel(
    #     title='Demo Book 2',
    #     short_description='A Nice Book 2',
    #     author='Yusuf Berkay Girgin 2',
    #     available=True,
    #     checkout_date=None,
    # )
    return create(book=book)
