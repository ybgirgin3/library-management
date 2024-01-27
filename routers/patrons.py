from __future__ import annotations

import datetime
from typing import List
from typing import Union

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from models import PatronModel
from services.orm import ORM

router = APIRouter(prefix='/patrons', tags=['patrons'])

orm = ORM(model='PatronModel')


@router.get(
    '/all',
    response_description='get all patrons',
    status_code=status.HTTP_200_OK,
)
def find_all() -> List[PatronModel]:
    try:
        patrons: Union[List[PatronModel], None] = orm.find_all()
        if patrons is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Patron found',
            )
        return patrons
    except Exception as e:
        raise e


@router.get(
    '/find',
    response_description='get a patron',
    status_code=status.HTTP_200_OK,
)
def find_one(patron: Union[str, int]) -> Union[PatronModel, None]:
    """
    usage :0000/patrons/find?patron=1
    :param patron: patron id or name or email
    :return:
    """
    try:
        # NOTE: run find_one value whether param is id or email or name
        key: str = ''
        if isinstance(patron, int):
            key = 'id'
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
        return found
    except Exception as e:
        raise e


@router.post(
    '/create',
    response_description='create a patron',
    status_code=status.HTTP_201_CREATED,
)
def create(patron: PatronModel):
    return orm.create(patron)


@router.put(
    '/update',
    response_description='update a patron',
    status_code=status.HTTP_200_OK,
)
def update(patron: PatronModel):
    pass


@router.delete(
    '/delete/{patron_id}',
    response_description='delete a patron',
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(patron_id: int):
    pass


# for dev
@router.post('/seed')
def seed_patron():
    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    patron = PatronModel(
        name='Yusuf Berkay Girgin',
        email='berkay@girgin.com',
    )
    return create(patron=patron)
