#!/usr/bin/python3
"""
Module: city.py
Author: TheWatcher01
Date: 2024-03-27
Description: Defines the City class in the HBNB project. Represents cities
with name and state_id attributes, extending functionality from BaseModel.
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete")
