import dataclasses
from typing import List
from typing import Optional
from typing import Union

from models import BookModel
from models import PatronModel


@dataclasses.dataclass
class Response:
    status: int
    message: Optional[Union[str, None]] = None
    data: Optional[Union[BookModel, PatronModel, List[BookModel], List[PatronModel]]] = None
    reason: Optional[List[str]] = None

    def to_dict(self):
        """
        Convert the Response object to a dictionary.

        Returns:
            dict: A dictionary representation of the Response object.
        """
        if isinstance(self.data, list):
            return {
                'status':   self.status,
                'message':  self.message,
                'data':  [item.to_dict() for item in self.data],
                'reason':   self.reason
            }
        elif self.data is not None:
            return {
                'status': self.status,
                'message': self.message,
                'data': self.data.to_dict(),
                'reason': self.reason
            }
