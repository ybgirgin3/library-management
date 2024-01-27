from typing import Union

from models import BookModel
from models import CheckoutModel
from models import PatronModel
from schemas import BookSchema
from schemas import CheckoutSchema
from schemas import PatronSchema
from services.connection import session


class ORM:
    def __init__(self, model: str):
        self.str_model = model

    @property
    def model(self):
        if self.str_model == 'BookModel':
            return BookModel
        elif self.str_model == 'PatronModel':
            return PatronModel
        else:
            return CheckoutModel

    @property
    def schema(self):
        if self.str_model == 'BookModel':
            return BookSchema
        elif self.str_model == 'PatronModel':
            return PatronSchema
        else:
            return CheckoutSchema

    def find_all(self):
        """
        find all of the item whether it active or inactive
        :return:
        """
        try:
            with session() as sess:
                results = sess.query(self.schema).all()
            return results
        except Exception as e:
            print(e)
            return None

    def find_one(self, q_filter: dict):
        if 'is_active' not in q_filter:
            q_filter['is_active'] = 1
        try:
            with session() as sess:
                result = sess.query(self.schema)

                for k, v in q_filter.items():
                    if hasattr(self.schema, k):
                        result = result.filter(getattr(self.schema, k) == v)
                return result.first()
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
