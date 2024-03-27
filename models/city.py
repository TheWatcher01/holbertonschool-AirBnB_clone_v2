#!/usr/bin/python3
"""
Module: city.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the City class, which inherits from BaseModel
and represents a city in the HBNB project.
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """
    The City class represents a city. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        state_id (str): The state id to which the city belongs.
        name (str): The name of the city.
    """
    __tablename__ = 'cities'
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
