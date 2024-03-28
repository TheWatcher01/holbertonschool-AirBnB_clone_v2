#!/usr/bin/python3
"""
Module: review.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines Review class, which inherits from BaseModel
and represents a review in HBNB project.
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class represents a review. It inherits from BaseModel and Base
    (SQLAlchemy declarative base class for Table mapping).
    Attributes:
        place_id (str): id of place review is for.
        user_id (str): id of user who wrote review.
        text (str): text of review.
    """
    __tablename__ = 'reviews'
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
