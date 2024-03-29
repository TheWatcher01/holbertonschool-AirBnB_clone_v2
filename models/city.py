#!/usr/bin/python3
"""
Module: city.py
Author: Teddy Deberdt
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

    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    state = relationship('State', back_populates='cities')
