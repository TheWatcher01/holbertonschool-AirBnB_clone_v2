#!/usr/bin/python3
""" Place Module for HBNB project """

from sqlalchemy.sql.schema import ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy import *
from models.review import Review
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review', backref='place')
    amenities = relationship(
        'Amenity', secondary=place_amenity, viewonly=False)

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def reviews(self):
            """ getter attribute reviews that returns the list of Review
            instances with place_id equals to the current Place.id"""
            from models import storage
            from models.review import Review
            list = []
            reviews = storage.all(Review)
            for value in reviews.values():
                if value.place_id == self.id:
                    list.append(value)
            return list

        @property
        def amenities(self):
            """ getter attribute amenities that returns the list of Amenity
            instances with place_id equals to the current Place.id"""
            from models import storage
            from models.amenity import Amenity
            list = []
            amenities = storage.all(Amenity)
            for value in amenities.values():
                if value.id in self.amenity_ids:
                    list.append(value)
            return list

        @amenities.setter
        def amenities(self, obj):
            """ setter attribute amenities.id that append on the list of
            Amenity instances """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)