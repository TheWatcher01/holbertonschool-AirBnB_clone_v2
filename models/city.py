#!/usr/bin/python3
"""
Module: city.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the City class in the HBNB project. Represents cities
with name and state_id attributes, extending functionality from BaseModel.
"""
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    state_id = ""
    name = ""
