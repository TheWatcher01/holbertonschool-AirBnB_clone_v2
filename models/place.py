#!/usr/bin/python3
"""
Module: place.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines Place class, which inherits from BaseModel
and represents a place in HBNB project.
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from os import getenv

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """
    Place class represents a place to stay. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        city_id (str): id of city place is in.
        user_id (str): id of user who owns place.
        name (str): name of place.
        description (str): description of place.
        number_rooms (int): number of rooms in place.
        number_bathrooms (int): number of bathrooms in place.
        max_guest (int): maximum number of guests place can accommodate.
        price_by_night (int): price per night to stay at place.
        latitude (float): latitude of place.
        longitude (float): longitude of place.
        amenity_ids (list): A list of amenity ids associated with place.
    """
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
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def amenities(self):
            from models import storage
            return [storage.all(Amenity)[amenity_id]
                    for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
