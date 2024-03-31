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


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            # Use isinstance() for checking the object's type
            return {k: v for k, v in FileStorage.__objects.items()
                    if isinstance(v, cls)}

    def delete(self, obj=None):
        """Deletes obj from __objects if it’s inside"""
        if obj is not None:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]

    def new(self, obj):
        """Adds new object to storage dictionary"""
        obj_dict = obj.to_dict()
        key = '{}.{}'.format(obj_dict['__class__'], obj.id)
        self.all().update({key: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
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
                    if val['__class__'] in classes:
                        # Create a copy of val to manipulate
                        val_copy = val.copy()
                        val_class = val_copy.pop('__class__', None)
                        if val_class:
                            self.all()[key] = classes[val_class](**val_copy)
                    else:
                        print(f"Warning: Class {val['__class__']} not found.")
        except FileNotFoundError:
            pass
