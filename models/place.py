#!/usr/bin/python3
"""
Module: place.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the Place class, inheriting from BaseModel and Base,
representing a place in the HBNB project with attributes for location,
accommodation details, and associated amenities.
"""

from models.base_model import BaseModel


class Place(BaseModel):
    """ A place to stay """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
