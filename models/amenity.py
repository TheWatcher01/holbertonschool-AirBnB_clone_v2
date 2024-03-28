#!/usr/bin/python3
"""
Module: amenity.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Module defines the Amenity class, which inherits from BaseModel
and represents an amenity in the HBNB project.
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """
    The Amenity class represents an amenity for a place.
    It inherits from BaseModel and Base (SQLAlchemy declarative base class
    for Table mapping).
    Attributes:
        name (str): The name of the amenity.
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity")
