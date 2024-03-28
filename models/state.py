#!/usr/bin/python3
"""
Module: state.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Module defines State class, which inherits from BaseModel
and represents a state in the HBNB project.
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_t  # Import storage_t from models


class State(BaseModel, Base):
    """
    State class represents a state. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        name (str): The name of the state.
    """
    __tablename__ = 'states'
    if storage_t == 'db':  # Use storage_t in condition
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """Returns the list of City instances with state_id equal to
            the current State.id for FileStorage"""
            from models.city import City
            city_list = models.storage.all(City).values()
            return [city for city in city_list if city.state_id == self.id]
