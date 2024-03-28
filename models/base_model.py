#!/usr/bin/python3
"""
Module: base_model.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module defines the BaseModel class, which serves as the base
class for all other model classes in the hbnb project.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid

# SQLAlchemy declarative base instance to construct models
Base = declarative_base()


class BaseModel:
    """
    BaseModel class for other classes to inherit from.
    Converts Python classes into SQLAlchemy Table objects with
    appropriate fields and relationships for database storage.
    """
    __abstract__ = True  # SQLAlchemy class isn't a database table itself
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Instantiate a new model. If kwargs are provided, they are used to set
        instance attributes. Otherwise, id, created_at, and updated_at are set.
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        for key, value in kwargs.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance.
        Format: [<class name>] (<id>) <dictionary of instance attributes>
        """
        cls_name = self.__class__.__name__
        return '[{}] ({}) {}'.format(
            cls_name, self.id,
            {k: v for k, v in self.__dict__.items() if k !=
             '_sa_instance_state'})

    def save(self):
        """
        Updates the updated_at attribute to the current time and saves the
        instance to the storage.
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
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
