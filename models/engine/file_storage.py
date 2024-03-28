#!/usr/bin/python3
"""
Module: file_storage.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Defines the FileStorage class for serializing instances to a JSON
file and deserializing JSON file to instances, managing a simple file-based
storage system.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Manages storage of hbnb models in JSON format."""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns objects of a specific type, if specified, or all objects."""
        if cls:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects[key] = obj

    def save(self):
        """Saves the storage dictionary to a file in JSON format."""
        obj_dict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f)

    def delete(self, obj=None):
        """Deletes an object from storage if it exists."""
        if obj:
            key = f'{type(obj).__name__}.{obj.id}'
            self.__objects.pop(key, None)

    def reload(self):
        """Loads the storage dictionary from the file, if it exists."""
        try:
            with open(self.__file_path) as f:
                obj_dict = json.load(f)
            for obj_data in obj_dict.values():
                cls_name = obj_data['__class__']
                if cls_name in self.classes():
                    cls = self.classes()[cls_name]
                    self.new(cls(**obj_data))
        except FileNotFoundError:
            pass

    @staticmethod
    def classes():
        """Returns a dictionary of valid classes for serialization."""
        return {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review
        }
