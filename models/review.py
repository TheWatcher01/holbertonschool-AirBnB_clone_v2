#!/usr/bin/python3
"""
Module: review.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Module defines Review class, which inherits from BaseModel
and represents a review in the HBNB project.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """ Review classto store review information """
    place_id = ""
    user_id = ""
    text = ""
