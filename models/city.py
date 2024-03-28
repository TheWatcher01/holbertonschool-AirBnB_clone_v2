#!/usr/bin/python3
"""
Module: city.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the City class in the HBNB project. Represents cities
with name and state_id attributes, extending functionality from BaseModel.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """
    Represents a city with related state information in the database.

    Attributes:
        __tablename__: Explicit table name definition for SQLAlchemy.
        state_id (Column): State id, indicating which state city belongs to.
        name (Column): The city's name.
    """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
