from fastapi import APIRouter, status
from typing import List
from models import Book

router = APIRouter(prefix='/books', tags=['books'])

@router.get('/all', response_description='get all books', response_model=List[Book], status_code=status.HTTP_200_OK)
def get(): pass

@router.post('/find/{book_id}', response_description='get a book', response_model=Book, status_code=status.HTTP_200_OK)
def findone(book_id:int): pass

@router.get('/create', response_description='create a book', response_model=Book, status_code=status.HTTP_201_CREATED)
def create(book:Book): pass

@router.put('/update', response_description='update a book', response_model=Book, status_code=status.HTTP_200_OK)
def update(book:Book): pass

@router.delete('/delete/{book_id}', response_description='delete a book', status_code=status.HTTP_301_MOVED_PERMANENTLY)
def delete(book_id:int): pass
