#!/usr/bin/python3
"""
Module: user.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the User class, which inherits from BaseModel
and represents a user in the HBNB project.
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """
    The User class represents a user. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        email (str): The email of the user. It cannot be null.
        password (str): The password of the user. It cannot be null.
        first_name (str): The first name of the user. It can be null.
        last_name (str): The last name of the user. It can be null.
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
