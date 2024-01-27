import dataclasses
from typing import Optional, Union, List
from models import BookModel, PatronModel


@dataclasses.dataclass
class Response:
    status: int
    message: Optional[Union[str, None]] = None
    data: Optional[Union[BookModel, PatronModel, List[BookModel], List[PatronModel]]] = None
    reason: Optional[List[str]] = None

    def to_dict(self):
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