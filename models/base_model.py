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
import datetime
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

    def __init__(self, **kwargs):
        """
        Initializes a new model instance using kwargs to set attributes,
        defaulting to generating a unique id and setting created_at and
        updated_at to the current datetime if not provided.
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        datetime_fields = ['created_at', 'updated_at']
        for field in datetime_fields:
            setattr(self, field, kwargs.get(field, datetime.utcnow()))
        for key, value in kwargs.items():
            if key not in datetime_fields + ['id']:
                setattr(self, key, value)

    def __str__(self):
        """
        Returns a string representation of the instance, excluding the
        SQLAlchemy internal state attribute '_sa_instance_state'.
        """
        cls_name = self.__class__.__name__
        attrs = {key: value for key, value in self.__dict__.items()
                 if key != '_sa_instance_state'}
        return f"[{cls_name}] ({self.id}) {attrs}"

    def save(self):
        """
        Updates 'updated_at' to the current time and saves the instance to
        the storage, utilizing the storage engine's 'new' and 'save' methods.
        """
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """
        Deletes the instance from storage by invoking the storage engine's
        'delete' method.
        """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """
        Converts instance into a dictionary format for JSON serialization,
        including class name and converting datetime attributes to ISO format.
        """
        dict_repr = self.__dict__.copy()
        dict_repr['__class__'] = self.__class__.__name__
        for field in ['created_at', 'updated_at']:
            dict_repr[field] = getattr(self, field).isoformat()
        dict_repr.pop('_sa_instance_state', None)
        return dict_repr
