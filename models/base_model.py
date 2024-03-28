#!/usr/bin/python3
"""
Module: base_model.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module defines the BaseModel class, which serves as the base
class for all other model classes in the hbnb project.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String
from datetime import datetime
import uuid

# SQLAlchemy declarative base instance to construct models
Base = declarative_base()


class BaseModel:
    """
    BaseModel class for other classes to inherit from.
    BaseModel converts Python classes into SQLAlchemy Table objects with
    appropriate fields and relationships for database storage.
    """
    __abstract__ = True  # Indicate that BaseModel isn't a database table itself
    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """
        Instantiate a new model.
        If kwargs are provided, they are used to set instance attributes.
        Otherwise, id, created_at, and updated_at are set to their default values.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            kwargs.setdefault('id', str(uuid.uuid4()))
            kwargs.setdefault('created_at', datetime.utcnow())
            kwargs.setdefault('updated_at', datetime.utcnow())
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at') and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance.
        Format: [<class name>] (<id>) <dictionary of instance attributes>
        """
        cls_name = self.__class__.__name__
        return '[{}] ({}) {}'.format(cls_name, self.id, self.__dict__)

    def save(self):
        """
        Updates the updated_at attribute to the current time and saves the
        instance to the storage.
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.save()

    def delete(self):
        """
        Deletes the current instance from the storage.
        """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """
        Converts the instance into a dictionary format for JSON serialization.
        """
        dictionary = {**self.__dict__, '__class__': self.__class__.__name__}
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary
