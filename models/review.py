#!/usr/bin/python3
"""
Module: review.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the Review class in the HBNB project, inheriting from
BaseModel and Base. Represents a review with attributes including place_id,
user_id, and text, mapped to a database table.
"""

from sqlalchemy import Column, String, ForeignKey
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """
    Review class defines review attributes for the HBNB project, mapping to
    the 'reviews' table in the database. It includes essential attributes such
    as place_id, user_id, and the review text.
    """
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
