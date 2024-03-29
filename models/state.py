#!/usr/bin/python3
"""
Module: state.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the State class in the HBNB project, representing states
with a name attribute and managing cities through a relationship or property.
"""

from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    name = ""
