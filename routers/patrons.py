from fastapi import APIRouter, status, HTTPException
import datetime
from typing import List, Union
from models import PatronModel
from services.orm import ORM

router = APIRouter(prefix="/patrons", tags=["patrons"])

orm = ORM(model="PatronModel")


@router.get(
    "/all", response_description="get all patrons", status_code=status.HTTP_200_OK
)
def find_all() -> List[PatronModel]:
    try:
        patrons: Union[List[PatronModel], None] = orm.find_all()
        if not len(patrons) or patrons is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Patron found"
            )
        return patrons
    except Exception as e:
        raise e


@router.get(
    "/find/{patron_id}",
    response_description="get a patron",
    status_code=status.HTTP_200_OK,
)
def find_one(patron_id: int) -> PatronModel:
    try:
        patron: Union[PatronModel, None] = orm.find_one(id=patron_id)
        if patron is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patron given id is not found",
            )
        return patron
    except Exception as e:
        raise e


@router.post(
    "/create",
    response_description="create a patron",
    status_code=status.HTTP_201_CREATED,
)
def create(patron: PatronModel):
    return orm.create(patron)


@router.put(
    "/update", response_description="update a patron", status_code=status.HTTP_200_OK
)
def update(patron: PatronModel):
    pass


@router.delete(
    "/delete/{patron_id}",
    response_description="delete a patron",
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(patron_id: int):
    pass


# for dev
@router.post("/seed")
def seed_patron():
    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    patron = PatronModel(
        name="Yusuf Berkay Girgin",
        email="berkay@girgin.com",
    )
    return create(patron=patron)
