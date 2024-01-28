import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import schemas
# to return


class UnknownDBError(Exception):
    pass


SQL_ALCHEMY_ENGINES = {
    'library': create_engine(
        # f"sqlite:///{os.getcwd()}/library.db",
        f'sqlite:///./library.db',
        echo=False,
    )
}


def _create_table(model: str, db_engine: Engine):
    print('SQLALCHEMY ENGINES:', SQL_ALCHEMY_ENGINES)
    model = getattr(schemas, model)
    model.__table__.create(db_engine)


def engine(db_name: str = 'library') -> Engine:
    try:
        return SQL_ALCHEMY_ENGINES[f'{db_name}']
    except KeyError:
        raise UnknownDBError


def session(db_name: str = 'library') -> Session:
    return Session(engine(db_name), expire_on_commit=False)
