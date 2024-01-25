from fastapi import APIRouter, status
from typing import List
from models import Book

router = APIRouter(prefix='/patrons', tags=['books'])

@router.get('/all', response_description='get all patrons', response_model=List[Book], status_code=status.HTTP_200_OK)
def get(): pass

@router.post('/find/{book_id}', response_description='get a patron', response_model=Book, status_code=status.HTTP_200_OK)
def findone(book_id:int): pass

@router.get('/create', response_description='create a patron', response_model=Book, status_code=status.HTTP_201_CREATED)
def create(book:Book): pass

@router.put('/update', response_description='update a patron', response_model=Book, status_code=status.HTTP_200_OK)
def update(book:Book): pass

@router.delete('/delete/{book_id}', response_description='delete a patron', status_code=status.HTTP_301_MOVED_PERMANENTLY)
def delete(book_id:int): pass
