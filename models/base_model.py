#!/usr/bin/python3
"""
Module: base_model.py
Author: TheWatcher01
Date: 2024-03-27
Description: Defines the BaseModel class, serving as the base class for all
other model classes in the hbnb project, facilitating the conversion of Python
classes into SQLAlchemy Table objects for database storage.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import uuid

Base = declarative_base()


class BaseModel:
    """
    Serves as the base class for model classes, converting Python classes into
    SQLAlchemy Table objects with appropriate fields and relationships.
    """
    __abstract__ = True  # Indicates class is abstract for SQLAlchemy
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a new BaseModel instance."""
        if 'id' not in kwargs:
            self.id = str(uuid.uuid4())
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at', '__class__']:
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls_name = self.__class__.__name__
        attrs = {key: value for key, value in self.__dict__.items()
                 if key != '_sa_instance_state'}
        return f"[{cls_name}] ({self.id}) {attrs}"

    def save(self):
        """Updates 'updated_at' to the current time and saves the instance."""
        from models import storage
        self.updated_at = datetime.utcnow()
        if self not in storage._DBStorage__session:
            storage.new(self)
        try:
            storage._DBStorage__session.commit()
        except SQLAlchemyError as e:
            storage._DBStorage__session.rollback()
            print(f"SQLAlchemy Exception: {e}")

    def delete(self):
        """Deletes the instance from storage."""
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Converts instance into a dictionary for JSON serialization."""
        dict_repr = {key: value.isoformat() if isinstance(value, datetime)
                     else value for key, value in self.__dict__.items()
                     if key != '_sa_instance_state'}
        dict_repr['__class__'] = self.__class__.__name__
        dict_repr['id'] = self.id
        dict_repr['created_at'] = self.created_at.isoformat()
        dict_repr['updated_at'] = self.updated_at.isoformat()
        return dict_repr
