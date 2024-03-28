#!/usr/bin/python3
"""
Module: base_model.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module defines the BaseModel class, which serves as the base
class for all other model classes in the hbnb project.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DATETIME, Column, String, DateTime
from datetime import datetime
from models import models
import uuid

# SQLAlchemy declarative base instance to construct models
if models.is_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    BaseModel class for other classes to inherit from.
    BaseModel converts Python classes into SQLAlchemy Table objects with
    appropriate fields and relationships for database storage.
    """
    __abstract__ = True  # SQLAlchemy class isn't a database table itself
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DATETIME, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DATETIME, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Instantiate a new model.
        If no kwargs are provided, id, created_at and updated_at are set.
        If kwargs are provided, they are used to set instance attributes.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            # if os.getenv('HBNB_TYPE_STORAGE') in ('db'):
            if not hasattr(kwargs, 'id'):
                setattr(self, 'id', str(uuid.uuid4()))
            if not hasattr(kwargs, 'created_at'):
                setattr(self, 'created_at', datetime.now())
            if not hasattr(kwargs, 'updated_at'):
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """
        Returns a string representation of the instance.
        Format: [<class name>] (<id>) <dictionary of instance attributes>
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

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
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary
