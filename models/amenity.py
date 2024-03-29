#!/usr/bin/python3
"""
Module: amenity.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Updates the Amenity class to inherit from BaseModel and Base,
representing an amenity in the HBNB project with a name attribute, mapped to
a database table.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel
# Import the association table for many-to-many relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """
    Represents an amenity for places in the HBNB project. Amenity instances
    have a name attribute and are linked to places through a many-to-many
    relationship.
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Establishing a many-to-many relationship to Place through place_amenity
    places = relationship("Place", secondary=place_amenity,
                          back_populates="amenities", viewonly=True)
