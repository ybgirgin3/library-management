from services.connection import session
from typing import Union, List
from models import BookModel, PatronModel, CheckoutModel
from schemas import BookSchema, PatronSchema, CheckoutSchema


class ORM:
    def __init__(self, model: str):
        self.str_model = model

    @property
    def model(self):
        if self.str_model == "BookModel":
            return BookModel
        elif self.str_model == "PatronModel":
            return PatronModel
        else:
            return CheckoutModel

    @property
    def schema(self):
        if self.str_model == "BookModel":
            return BookSchema
        elif self.str_model == "PatronModel":
            return PatronSchema
        else:
            return CheckoutSchema

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

    def create(self, item: Union[BookModel, PatronModel, CheckoutModel]):
        try:
            with session() as sess:
                try:
                    item_to_save = self.schema(**item.dict())
                except:
                    item_to_save = item
                sess.add(item_to_save)
                sess.commit()
                # sess.refresh(item)
                return item_to_save

        except Exception as e:
            print(e)
            return None
