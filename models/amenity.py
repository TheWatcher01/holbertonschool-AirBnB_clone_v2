#!/usr/bin/python3
"""
Module: amenity.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module updates the Amenity class to inherit from BaseModel
and Base. It represents an amenity in the HBNB project with a name attribute,
and maps it to a database table.
"""

# Importing necessary classes from SQLAlchemy and models
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

# Importing the association table for the many-to-many relationship between
# Place and Amenity. Make sure this import is correct.
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """
    Represents an amenity for places in the HBNB project. Instances of Amenity
    have a name attribute and are linked to places through a many-to-many
    relationship.
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Many-to-many relationship with Place
    # Make sure 'back_populates' matches exactly the property in Place
    place_amenities = relationship("Place", secondary=place_amenity,
                                   back_populates="amenities", viewonly=False)
