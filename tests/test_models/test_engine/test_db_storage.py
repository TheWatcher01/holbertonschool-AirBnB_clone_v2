#!/usr/bin/python3
"""
File: test_db_storage.py
Author: TheWatcher01
Date: 2024-03-31
Description: Unit tests for db_storage.py with a real database connection.
"""

import unittest
import os
from models import storage
from models.state import State
from models.city import City


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the database environment before all tests."""
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test_user'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        os.environ['HBNB_ENV'] = 'test'
        storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database environment after all tests."""
        storage._DBStorage__session.close()
        storage._DBStorage__engine.dispose()

    def setUp(self):
        """Setup test environment before each test."""
        storage.reload()

    def tearDown(self):
        """Cleanup after each test."""
        storage._DBStorage__session.rollback()
        storage._DBStorage__session.close()

    def test_all(self):
        """
        all() returns dictionary of all objects when no class is specified.
        """
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)

    def test_all_with_class(self):
        """all() method returns a dictionary of objects of a specific class."""
        all_states = storage.all(State)
        self.assertTrue(all(isinstance(obj, State)
                        for obj in all_states.values()))

    def test_new(self):
        """Test that new() correctly adds an object to the session."""
        new_state = State(name="TestState")
        storage.new(new_state)
        self.assertIn(new_state, storage._DBStorage__session.new)

    def test_save(self):
        """Test that save() correctly commits changes to the database."""
        new_city = City(name="TestCity", state_id="TestStateId")
        storage.new(new_city)
        storage.save()
        # Assuming id is not None if committed
        self.assertIsNotNone(new_city.id)

    def test_delete(self):
        """Test that delete() correctly removes an object from the session."""
        new_state = State(name="ToDeleteState")
        storage.new(new_state)
        storage.save()
        storage.delete(new_state)
        self.assertNotIn(new_state, storage.all(State).values())

    def test_reload(self):
        """That reload() correctly loads objects from database into session."""
        new_state = State(name="TestState")
        storage.new(new_state)
        storage.save()
        storage._DBStorage__session.expunge(new_state)
        storage.reload()
        self.assertIn(new_state, storage.all(State).values())


if __name__ == "__main__":
    unittest.main()
