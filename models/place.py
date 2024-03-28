#!/usr/bin/python3
"""
Module: place.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the Place class, inheriting from BaseModel and Base,
representing a place in the HBNB project with attributes for location,
accommodation details, and associated amenities.
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from os import getenv

# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel, Base):
    """Represents a Place with details and associated amenities."""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenities = relationship(
        "Amenity", secondary=place_amenity, viewonly=False)
