# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Integer, LargeBinary, Table, Text, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(Text(500))
    work = Column(Integer)
    activity_order = Column(Integer)
    deleted = Column(Integer)
    category_id = Column(Integer)
    search_name = Column(Text)
    facts = relationship("Fact", back_populates="activity")


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(Text(500))
    color_code = Column(Text(50))
    category_order = Column(Integer)
    search_name = Column(Text)


t_fact_index = Table(
    'fact_index', metadata,
    Column('id', NullType),
    Column('name', NullType),
    Column('category', NullType),
    Column('description', NullType),
    Column('tag', NullType)
)


class FactIndexContent(Base):
    __tablename__ = 'fact_index_content'

    docid = Column(Integer, primary_key=True)
    c0id = Column(NullType)
    c1name = Column(NullType)
    c2category = Column(NullType)
    c3description = Column(NullType)
    c4tag = Column(NullType)


class FactIndexSegdir(Base):
    __tablename__ = 'fact_index_segdir'

    level = Column(Integer, primary_key=True, nullable=False)
    idx = Column(Integer, primary_key=True, nullable=False)
    start_block = Column(Integer)
    leaves_end_block = Column(Integer)
    end_block = Column(Integer)
    root = Column(LargeBinary)


class FactIndexSegment(Base):
    __tablename__ = 'fact_index_segments'

    blockid = Column(Integer, primary_key=True)
    block = Column(LargeBinary)


t_fact_tags = Table(
    'fact_tags', metadata,
    Column('fact_id', ForeignKey("facts.id"), primary_key=True),
    Column('tag_id', ForeignKey("tags.id"), primary_key=True)
)


class Fact(Base):
    __tablename__ = 'facts'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activity", back_populates="facts")
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(Text)

    tags = relationship("Tag", secondary=t_fact_tags, back_populates="facts")

    @property
    def duration(self):
        return self.end_time - self.start_time


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, index=True)
    autocomplete = Column(Boolean, server_default=text("true"))
    facts = relationship("Fact", secondary=t_fact_tags, back_populates="tags")


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


t_version = Table(
    'version', metadata,
    Column('version', Integer)
)
