from services.connection import session
from typing import Union, List
from models import BookModel, PatronModel
from schemas import BookSchema, PatronSchema


class ORM:
    def __init__(self, model: str):
        self.model = BookModel if model == "BookModel" else PatronModel
        self.schema = BookSchema if model == "BookModel" else PatronSchema

    def find_all(self):
        try:
            with session() as sess:
                books = sess.query(self.schema).all()
            return books
        except Exception as e:
            print(e)
            return None

    def find_one(self, id: int):
        try:
            with session() as sess:
                book = sess.query(self.schema).where(self.schema.id).first()
                return book
        except Exception as e:
            print(e)
            return None

    def create(self, item: Union[BookModel, PatronModel]):
        try:
            with session() as sess:
                item_to_save = self.schema(**item.dict())
                sess.add(item_to_save)
                sess.commit()
                # sess.refresh(item)
                return item_to_save

        except Exception as e:
            print(e)
            return None
