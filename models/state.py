#!/usr/bin/python3
"""
Module: state.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the State class, which inherits from BaseModel
and represents a state in the HBNB project.
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """
    The State class represents a state. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        name (str): The name of the state.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")
