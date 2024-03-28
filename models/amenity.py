#!/usr/bin/python3
"""
Module: amenity.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the Amenity class, which inherits from BaseModel and Base,
representing an amenity in the HBNB project with a name attribute.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Represents an Amenity with its name and associated places."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity")
