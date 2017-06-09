import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Layout(Base):
    __tablename__ = 'layout'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Building(Base):
    __tablename__ = 'building'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    category = Column(String(50))
    description = Column(String(250))
    level = Column(String(50))
    layout_id = Column(Integer, ForeignKey('layout.id'))
    layout = relationship(Layout)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    #Serialize function added send JSON objects
    @property
    def serialize(self):

        return {
            'name': self.name,
            'id': self.id,
            'category': self.category,
            'description': self.description,
            'level': self.level,
        }


engine = create_engine('sqlite:///cocbuildingwithuser.db')


Base.metadata.create_all(engine)
