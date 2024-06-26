#!/usr/bin/python3
"""
Module: test_base_model.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module contains the unit tests for the BaseModel class.
"""

from models.base_model import BaseModel
from datetime import datetime
import unittest
import json
import time
import re
import os


class test_basemodel(unittest.TestCase):
    """
    Defines a class to test the BaseModel class.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the test class.
        """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """
        Setup function to prepare the environment for each test.
        """
        pass

    def tearDown(self):
        """
        Teardown function to clean up after each test.
        """
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """
        Test case for creating a default BaseModel instance.
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
        Test case for creating a BaseModel instance with kwargs.
        """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
        Test case for creating a BaseModel instance with kwargs of wrong type.
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """
        Test case for the save method of BaseModel.
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        try:
            with open('file.json', 'r') as f:
                j = json.load(f)
                self.assertEqual(j[key], i.to_dict())
        except FileNotFoundError:
            self.fail("file.json not found")

    def test_str(self):
        """
        Test case for the __str__ method of BaseModel.
        """
        i = self.value()
        expected_str = '[{}] ({}) {}'.format(self.name, i.id, i.__dict__)
        expected_str = re.sub(
            r"'_sa_instance_state': <sqlalchemy.orm.state.InstanceState "
            r"object at 0x[0-9a-fA-F]+>, ", "", expected_str)
        self.assertEqual(str(i), expected_str)

    def test_todict(self):
        """
        Test case for the to_dict method of BaseModel.
        """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """
        Test case for creating a BaseModel instance with None kwargs.
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Test case for creating a BaseModel instance with extra kwargs."""
        kwargs = {'id': '123', 'created_at': '2024-06-28T14:00:00',
                  'updated_at': '2024-06-28T14:00:00'}
        new = BaseModel(**kwargs)
        self.assertFalse(hasattr(new, 'nonexistent'))

    def test_id(self):
        """
        Test case for the id attribute of BaseModel.
        """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """
        Test case for the created_at attribute of BaseModel.
        """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Test case for the updated_at attribute of BaseModel."""
        new = self.value()
        updated_at = new.updated_at
        new.save()  # This should update the `updated_at` attribute
        self.assertNotEqual(updated_at, new.updated_at)


if __name__ == "__main__":
    unittest.main()
