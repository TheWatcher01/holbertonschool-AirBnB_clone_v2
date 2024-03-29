#!/usr/bin/python3
"""
Module: file_storage.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the FileStorage class. It is responsible for
serializing instances to a JSON file and deserializing JSON file to instances.
It manages a simple file-based storage system.
"""

import json


class FileStorage:
    """
    This class manages the storage of hbnb models in JSON format.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If a class is provided, it returns only instances of that class.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            return {k: v for k, v in FileStorage.__objects.items()
                    if isinstance(v, cls)}

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.
        If obj is None, the method does nothing.
        """
        if obj is not None:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]

    def new(self, obj):
        """
        Adds a new object to the storage dictionary after validating it.
        The object must have a 'required_fields' method/attribute.
        """
        if hasattr(obj, 'required_fields'):
            required_fields = obj.required_fields()
            obj_dict = obj.to_dict()
            if not all(field in obj_dict for field in required_fields):
                raise ValueError(
                    f"Object of type {type(obj).__name__} is missing "
                    "required fields.")
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            self.all().update({key: obj})
        else:
            raise ValueError(
                f"Object of type {type(obj).__name__} does not define "
                "required fields.")

    def save(self):
        """
        Saves the storage dictionary to a file.
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """
        Loads the storage dictionary from a file.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
