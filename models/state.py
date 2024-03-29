#!/usr/bin/python3
"""
Module: state.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the State class for the HBNB project. The
State class represents states with a 'name' attribute and manages cities
through a relationship or property.
"""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City  # Import City class


class State(BaseModel, Base):
    """
    The State class is a representation of a state in the HBNB project. It
    inherits from the BaseModel and Base classes.
    """
    __tablename__ = 'states'

    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete')
    else:
        @property
        def cities(self):
            from models import storage
            return [city for city in storage.all(City)
                    .values() if city.state_id == self.id]
