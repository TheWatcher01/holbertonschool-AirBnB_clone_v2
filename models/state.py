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


class State(BaseModel, Base):
    """
    The State class is a representation of a state in the HBNB project. It
    inherits from the BaseModel and Base classes.
    """
    __tablename__ = 'states'  # Table name in the database for States.

    id = Column(String(60), primary_key=True, nullable=False)  # State id.
    name = Column(String(128), nullable=False)  # State name.

    # 'cities' attribute represents a relationship with the City class. It
    # allows for the management of cities that belong to a state. The 'backref'
    # argument allows access to the State from a City object. The 'cascade'
    # argument ensures that operations performed on a State are also performed
    # on its associated City objects.
    cities = relationship('City', backref='state',
                          cascade='all, delete, delete-orphan')
