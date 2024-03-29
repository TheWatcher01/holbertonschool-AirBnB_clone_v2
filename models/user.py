#!/usr/bin/python3
"""
Module: user.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the User class in the HBNB project, inheriting from
BaseModel and Base. It represents a user with attributes like email,
password, first_name, and last_name, mapped to a database table.
"""
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String



class User(BaseModel, Base):
    """
    User class defines user attributes for the HBNB project, mapping to
    the 'users' table in the database. It includes essential attributes
    such as email and password, along with optional first and last names.
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    reviews = relationship("Review", backref="user", cascade="all, delete")
