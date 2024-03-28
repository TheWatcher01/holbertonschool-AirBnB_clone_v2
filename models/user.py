#!/usr/bin/python3
"""
Module: user.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the User class, inheriting from BaseModel and Base,
representing a user in the HBNB project with email, password, first_name,
and last_name attributes.
"""

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Represents a User with email, password, and optionally, names."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
