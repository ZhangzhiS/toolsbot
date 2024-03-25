#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import inspect, Column, Integer, DateTime
from sqlalchemy.orm import declared_attr, declarative_base


BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True

    id = Column(Integer(), primary_key=True)
    create_time = Column(DateTime(), default=datetime.now, comment='添加时间')
    update_time = Column(DateTime(), comment='更新时间')

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self, exclude=None) -> dict:
        if exclude is None:
            exclude = {}
        res = dict()
        for c in inspect(self).mapper.column_attrs:
            if c.key in exclude:
                continue
            res[c.key] = getattr(self, c.key)
        return res

