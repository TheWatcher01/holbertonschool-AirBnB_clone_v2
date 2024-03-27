#!/usr/bin/python3
"""
Module: file_storage.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module defines the FileStorage class, which serializes
instances to a JSON file and deserializes JSON file to instances.
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
    """
    A class to manage the storage of all instances in JSON format.
    Attributes:
        __file_path (str): The file path to the JSON file.
        __objects (dict): The dictionary of objects.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If a class is specified, it returns a dictionary of instances of that
        class currently in storage.
        """
        if cls is None:
            return FileStorage.__objects
        else:
            return {k: v for k, v in FileStorage.__objects.items()
                    if type(v) == cls}

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.
        """
        if obj is not None:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]
                self.save()

    def new(self, obj):
        """
        Adds new object to storage dictionary.
        """
        obj_dict = obj.to_dict()
        key = '{}.{}'.format(obj_dict['__class__'], obj.id)
        self.all().update({key: obj})

    def save(self):
        """
        Saves storage dictionary to file in JSON format.
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """
        Loads storage dictionary from file.
        """
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
