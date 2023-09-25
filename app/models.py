from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModelClass(Base):
    __abstract__ = True
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, onupdate=func.now())


class Post(BaseModelClass):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)

    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')


class Author(BaseModelClass):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    