from typing import List
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from auth import get_current_user
from auth import User
from models import PatronModel
from models import Response
from services.orm import ORM

router = APIRouter(prefix='/patrons', tags=['patrons'])

orm = ORM(model='PatronModel')


@router.get(
    '/all',
    response_description='get all patrons',
    status_code=status.HTTP_200_OK,
)
def find_all(current_user: User = Depends(get_current_user)) -> Response:
    """
    Retrieve all patrons.

    Args:
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing patrons or error message.
    """
    try:
        patrons: Union[List[PatronModel], None] = orm.find_all()
        if patrons is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Patron found',
            )
        return Response(
            status=status.HTTP_200_OK,
            message='Patrons Found',
            data=patrons,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No Patron found due to :{e}',
        )


@router.get(
    '/find',
    response_description='get a patron',
    status_code=status.HTTP_200_OK,
)
def find_one(patron: Union[str, int], current_user: User = Depends(get_current_user)) -> Response:
    """
    usage :0000/patrons/find?patron=1
    Retrieve a single patron.

    Args:
        patron: Patron ID, name, or email.
        current_user: The current authenticated user.

    Returns:
        Response: Response object containing the patron or error message.
    """
    try:
        # NOTE: run find_one value whether param is id or email or name
        key: str = ''
        if isinstance(patron, int) or patron.isnumeric():
            key = 'id'
            patron = int(patron)
        elif isinstance(patron, str):
            if '@' in patron:
                key = 'email'
            else:
                key = 'name'

        q_filter = {key: patron}

        found: Union[PatronModel, None] = orm.find_one(q_filter)
        if found is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Patron given id is not found',
            )
        return Response(
            status=status.HTTP_200_OK,
            message=f'Patron with {key}: {patron} found successfully',
            data=found,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Unable to get patron due to {e}',
        )


@router.post(
    '/create',
    response_description='create a patron',
    status_code=status.HTTP_201_CREATED,
)
def create(patron: PatronModel, current_user: User = Depends(get_current_user)) -> Response:
    """
    Create a new patron.

    Args:
        patron: PatronModel object containing patron details.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """
    try:
        saved = orm.create(patron)
        if saved is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=f'unable to create',
            )
        return Response(
            status=status.HTTP_201_CREATED,
            message='Patron Successfully Created',
            data=saved,
            reason=None
        ).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'unable to create patron due to {e}',
        )


@router.put(
    '/update',
    response_description='update a patron',
    status_code=status.HTTP_200_OK,
)
def update(patron: PatronModel, current_user: User = Depends(get_current_user)):
    """
    Update an existing patron.

    Args:
        patron: PatronModel object containing updated patron details.
        current_user: The current authenticated user.
    """
    pass


@router.delete(
    '/delete/{patron_id}',
    response_description='delete a patron',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(patron_id: int, current_user: User = Depends(get_current_user)):
    """
    Delete a patron by ID.

    Args:
        patron_id: The ID of the patron to be deleted.
        current_user: The current authenticated user.
    """
    pass


# for dev
@router.post('/seed')
def seed_patron(patron: PatronModel, current_user: User = Depends(get_current_user)):
    """
    Seed a patron.

    Args:
        patron: PatronModel object containing patron details.
        current_user: The current authenticated user.

    Returns:
        Response: Response object indicating success or failure.
    """

    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    # patron = PatronModel(
    #     name='Yusuf Berkay Girgin',
    #     email='berkay@girgin.com',
    # )
    return create(patron=patron)
