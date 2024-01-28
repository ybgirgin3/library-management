from typing import Union

from models import BookModel
from models import CheckoutModel
from models import PatronModel
from schemas import BookSchema
from schemas import CheckoutSchema
from schemas import PatronSchema
from services.connection import session


class ORM:
    """
    Object-Relational Mapping class for database operations.
    """
    def __init__(self, model: str):
        self.str_model = model

    @property
    def model(self):
        """
        Get the model corresponding to the ORM instance.

        Returns:
            Union[BookModel, PatronModel, CheckoutModel]: The corresponding model instance.
        """
        if self.str_model == 'BookModel':
            return BookModel
        elif self.str_model == 'PatronModel':
            return PatronModel
        else:
            return CheckoutModel

    @property
    def schema(self):
        """
        Get the schema corresponding to the ORM instance.

        Returns:
            Union[BookSchema, PatronSchema, CheckoutSchema]: The corresponding schema instance.
        """
        if self.str_model == 'BookModel':
            return BookSchema
        elif self.str_model == 'PatronModel':
            return PatronSchema
        else:
            return CheckoutSchema

    def find_all(self):
        """
         Find all items of the specified model.

         Returns:
             list: A list of items of the specified model.
         """
        try:
            with session() as sess:
                results = sess.query(self.schema).all()
            return results
        except Exception as e:
            print(e)
            return None

    def find_one(self, q_filter: dict):
        """
        Find one item based on the provided query filter.

        Args:
            q_filter (dict): The query filter.

        Returns:
            Union[BookModel, PatronModel, CheckoutModel]: The found item, if any.
        """

        # if 'is_active' not in q_filter:
        #     q_filter['is_active'] = 1
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
        """
        Create an item of the specified model.

        Args:
            item (Union[BookModel, PatronModel, CheckoutModel]): The item to create.

        Returns:
            Union[BookModel, PatronModel, CheckoutModel]: The created item.
        """
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
