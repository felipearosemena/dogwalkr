from contextlib import ContextDecorator
from typing import Any, List, Optional, Tuple

from sqlalchemy import func, desc, Column, ForeignKey, Integer, String
from sqlalchemy.types import DateTime

from .constants import TOY_ORDER_QUERY_PARAM_MAP
from ..common.db import Session
from ..common.models import Base


class ToyDAO(Base):
    __tablename__ = "toys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    dog_owner_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ToysContextManager(ContextDecorator):
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        try:
            if exc_type:
                self.session.rollback()
                return False
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_toys(
        self,
        name: Optional[str] = None,
        owner_ids: Optional[List[int]] = None,
        sort: Optional[str] = "created_at",
        order: Optional[str] = "desc",
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> Tuple[List[ToyDAO], int]:
        """
        Gets Toy objects based on parameters passed in.
        :param name str:                      Name of toy.
        :param owner_ids list(int):           List of owner IDs.
        :param sort str:                      Attribute to sort by.
        :param order str:                     Sort order ('asc' or 'desc').
        :param limit int:                     Limit for results in response.
        :param offset int:                    Offset for results in response.
        :rtype: list(ToyDAO), int
        """
        if not (name or owner_ids):
            raise Exception("A parameter must be passed.")

        query = self.session.query(ToyDAO)
        if name:
            query = query.filter(ToyDAO.name == name)
        if owner_ids:
            query = query.filter(ToyDAO.dog_owner_id.in_(owner_ids))

        # count
        count = self._get_count(query)

        # prep query for meta preferences
        sort_order = TOY_ORDER_QUERY_PARAM_MAP[order]
        if sort:
            query = query.order_by(sort_order(getattr(ToyDAO, sort)))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        daos = query.all()
        return daos, count

    def _get_count(self, query: Any) -> int:
        count_q = query.statement.with_only_columns([func.count()]).order_by(None)
        count = query.session.execute(count_q).scalar()
        return count
