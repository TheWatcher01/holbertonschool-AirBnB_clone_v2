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
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4


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
        del os.environ['HBNB_MYSQL_USER']
        del os.environ['HBNB_MYSQL_PWD']
        del os.environ['HBNB_MYSQL_HOST']
        del os.environ['HBNB_MYSQL_DB']
        del os.environ['HBNB_ENV']

    def setUp(self):
        """Setup test environment before each test."""
        storage.reload()

    def tearDown(self):
        """Cleanup after each test."""
        storage._DBStorage__session.rollback()
        storage._DBStorage__session.close()

    def test_all(self):
        """all() returns dict of all objects when no class is specified."""
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)

    def test_all_with_class(self):
        """all() method returns a dictionary of objects of a specific class."""
        all_states = storage.all(State)
        self.assertTrue(all(isinstance(obj, State)
                        for obj in all_states.values()))

    def test_new(self):
        """Test that new() correctly adds an object to the session."""
        new_state = State(name=f"TestState_{uuid4()}")
        storage.new(new_state)
        storage.save()
        all_states = storage.all(State)
        self.assertIn(
            new_state.id, [state.id for state in all_states.values()])

    def test_save(self):
        """Test that save() correctly commits changes to the database."""
        new_city = City(name=f"TestCity_{uuid4()}",
                        state_id=f"TestStateId_{uuid4()}")
        storage.new(new_city)
        storage.save()
        # Assuming id is not None if committed
        self.assertIsNotNone(new_city.id)

    def test_delete(self):
        """Test that delete() correctly removes an object from the session."""
        new_state = State(name=f"ToDeleteState_{uuid4()}")
        storage.new(new_state)
        storage.save()
        storage.delete(new_state)
        storage.save()
        all_states = storage.all(State)
        self.assertNotIn(
            new_state.id, [state.id for state in all_states.values()])

    def test_reload(self):
        """That reload() correctly loads objects from database into session."""
        new_state = State(name=f"TestState_{uuid4()}")
        storage.new(new_state)
        storage.save()
        storage._DBStorage__session.expunge(new_state)
        storage.reload()
        reloaded_state = storage.all(State).get(f"State.{new_state.id}")
        self.assertIsNotNone(reloaded_state)
        self.assertEqual(reloaded_state.name, new_state.name)


if __name__ == "__main__":
    unittest.main()
