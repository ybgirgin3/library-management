from sqlalchemy import create_engine
import schemas

import os

# to return
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine


class UnknownDBError(Exception):
    pass


SQL_ALCHEMY_ENGINES = {
    "library": create_engine(
        f"sqlite:///{os.getcwd()}/library.db",
        echo=False,
    )
}


def _create_table(model: str, db_engine: Engine):
    model = getattr(schemas, model)
    model.__table__.create(db_engine)


def engine(db_name: str = "library") -> Engine:
    try:
        return SQL_ALCHEMY_ENGINES[f"{db_name}"]
    except KeyError:
        raise UnknownDBError


def session(db_name: str = "library") -> Session:
    return Session(engine(db_name), expire_on_commit=False)
