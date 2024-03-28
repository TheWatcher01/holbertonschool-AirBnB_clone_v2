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
from os import getenv


class State(BaseModel, Base):
    """
    State class represents a state. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        name (str): The name of the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", back_populates="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Get a list of all related City objects."""
            from models import storage
            from models.city import City
            return [city for city in storage.all(City).values()
                    if city.state_id == self.id]
