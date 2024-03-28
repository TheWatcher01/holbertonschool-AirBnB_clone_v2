#!/usr/bin/python3
"""
Module: state.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the State class in the HBNB project, representing states
with a name attribute and managing cities through a relationship or property.
"""

from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """
    Represents a state, holding cities within it, either via database
    relationships in DBStorage or through a property in FileStorage.

    Attributes:
        __tablename__: Explicit table name definition for SQLAlchemy.
        name (Column): The state's name.
        cities (relationship/property): Collection of city instances associated
                                         with the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equal to
            the current State.id for FileStorage.
            """
            from models import storage
            all_cities = storage.all(City)
            return [city for city in all_cities.values()
                    if city.state_id == self.id]
