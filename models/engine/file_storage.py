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
        elif isinstance(cls, str):
            cls = eval(cls) if cls in FileStorage.classes() else None
        return {
            k: v for k, v in FileStorage.__objects.items() if
            isinstance(v, cls)}

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.
        """
        if obj:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects.pop(obj_key, None)
            self.save()

    def new(self, obj):
        """
        Adds new object to storage dictionary.
        """
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

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
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    if cls_name in FileStorage.classes():
                        cls = eval(cls_name)
                        self.new(cls(**val))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error: Unable to decode the JSON file.")

    @staticmethod
    def classes():
        """
        Returns a dictionary of valid classes and their references.
        """
        return {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
