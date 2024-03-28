#!/usr/bin/python3
"""
File: test_init.py
Author: TheWatcher01
Date: 2024-03-28
Description: This file initializes the tests package.
"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from unittest.mock import patch
from models import storage
import unittest
import os


class TestInit(unittest.TestCase):
    """
    Test case for the initialization of storage engines.
    """

    def setUp(self):
        """
        Setup for tests. Initializes instances of FileStorage and DBStorage.
        """
        self.file_storage = FileStorage()
        self.db_storage = DBStorage()

    def tearDown(self):
        """
        Cleanup after tests. Deletes instances of FileStorage and DBStorage.
        """
        del self.file_storage
        del self.db_storage

    @patch.dict('os.environ', {'HBNB_TYPE_STORAGE': 'file'})
    def test_file_storage_selected_with_env_var(self):
        """
        Test if FileStorage is selected when HBNB_TYPE_STORAGE is 'file'.
        """
        from models import storage
        self.assertIsInstance(storage, FileStorage)

    @patch.dict('os.environ', {'HBNB_TYPE_STORAGE': 'db',
                               'HBNB_MYSQL_USER': 'root',
                               'HBNB_MYSQL_PWD': 'root',
                               'HBNB_MYSQL_HOST': 'localhost',
                               'HBNB_MYSQL_DB': 'hbnb_test_db'})
    def test_db_storage_selected_with_env_var(self):
        """
        Test if DBStorage is selected when HBNB_TYPE_STORAGE is 'db' and all
        required environment variables are set.
        """
        from models import storage
        self.assertIsInstance(storage, DBStorage)

    @patch.dict('os.environ', {'HBNB_TYPE_STORAGE': 'db'})
    def test_file_storage_selected_with_incomplete_env_vars(self):
        """
        Test if FileStorage is selected when HBNB_TYPE_STORAGE is 'db' but not
        all required environment variables are set.
        """
        from models import storage
        self.assertIsInstance(storage, FileStorage)

    def test_reload(self):
        """
        Test if storage.reload() works correctly.
        """
        from models import storage
        try:
            storage.reload()
        except Exception as e:
            self.fail(f"storage.reload() raised Exception unexpectedly: {e}")

    def test_storage_with_base_model(self):
        """Test if storage correctly handles BaseModel instances."""
        # Create a new BaseModel instance and add it to storage
        new_object = BaseModel()
        storage.new(new_object)
        storage.save()

        # Check if the new object is in storage
        self.assertIn(new_object, storage.all(BaseModel).values())

        # Delete the object from storage
        storage.delete(new_object)
        storage.save()

        # Check if the object has been deleted from storage
        self.assertNotIn(new_object, storage.all(BaseModel).values())


if __name__ == '__main__':
    unittest.main()
