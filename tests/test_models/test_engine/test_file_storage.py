#!/usr/bin/python3
"""
Module for testing file storage
Author: TheWatcher01
Date: 2024-03-31
Description: Unit tests for the FileStorage class.
"""

import unittest
from models.base_model import BaseModel
from models import storage
import os


class TestFileStorage(unittest.TestCase):
    """Class to test the file storage method"""

    def setUp(self):
        """Set up test environment"""
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """Remove storage file at end of tests"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """__objects is initially empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """New object is correctly added to __objects"""
        new = BaseModel()
        self.assertIn(f"BaseModel.{new.id}", storage.all())

    def test_all(self):
        """__objects is properly returned"""
        new = BaseModel()
        self.assertIsInstance(storage.all(), dict)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel save without calling save()"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """Data is saved to file"""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """FileStorage save method"""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        storage.save()
        storage.reload()
        self.assertIn(f"BaseModel.{new.id}", storage.all())

    def test_reload_empty(self):
        """Load from an empty file does not raise error"""
        with open('file.json', 'w') as f:
            f.write("{}")
        storage.reload()
        self.assertEqual(len(storage.all()), 0)

    def test_reload_from_nonexistent(self):
        """Nothing happens if file does not exist"""
        if os.path.exists('file.json'):
            os.remove('file.json')
        storage.reload()
        self.assertEqual(len(storage.all()), 0)

    def test_base_model_save(self):
        """BaseModel save method calls storage save"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """Confirm __file_path is string"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """Key is properly formatted"""
        new = BaseModel()
        key = f"BaseModel.{new.id}"
        self.assertIn(key, storage.all().keys())

    def test_storage_var_created(self):
        """FileStorage object storage created"""
        from models.engine.file_storage import FileStorage
        self.assertIsInstance(storage, FileStorage)


if __name__ == "__main__":
    unittest.main()
