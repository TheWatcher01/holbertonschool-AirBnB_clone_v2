#!/usr/bin/python3
"""
Module: place.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Updates the Place class to inherit from BaseModel and Base,
mapping it to a database table with attributes for location, accommodation
details, and associated amenities in the HBNB project.
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship

# Table d'association pour la relation many-to-many entre Place et Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey(
        'places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey(
        'amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ Représente un lieu d'hébergement dans le projet HBNB. """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []  # Pour compatibilité avec FileStorage

    # Relation SQLAlchemy many-to-many avec Amenity
    amenities = relationship(
        "Amenity", secondary=place_amenity, back_populates="place_amenities")
