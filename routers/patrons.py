from fastapi import APIRouter, status
import datetime
from typing import List
from models import PatronModel
from services.orm import ORM

router = APIRouter(prefix="/patrons", tags=["patrons"])

orm = ORM(model="PatronModel")


@router.get(
    "/all", response_description="get all patrons", status_code=status.HTTP_200_OK
)
def get():
    return orm.find_all()


@router.post(
    "/find/{book_id}",
    response_description="get a patron",
    status_code=status.HTTP_200_OK,
)
def findone(book_id: int):
    pass


@router.get(
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
    "/delete/{book_id}",
    response_description="delete a patron",
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def delete(patron_id: int):
    pass


# for dev
@router.get("/seed")
def seed_book():
    # book = BookModel(title='Demo Book', short_description='A Nice Book', author='Yusuf Berkay Girgin')
    patron = PatronModel(
        name="Yusuf Berkay Girgin",
        email="berkay@girgin.com",
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    return create(patron=patron)
