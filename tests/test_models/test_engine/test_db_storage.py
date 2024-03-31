#!/usr/bin/python3
"""
File: test_db_storage.py
Author: TheWatcher01
Date: 2024-03-31
Description: Unit tests for db_storage.py with a real database connection.
"""

from models.state import State
from models.city import City
from models import storage
from uuid import uuid4
import unittest
import MySQLdb
import os


class TestDBStorageMySQLDirect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Establish a direct connection to the MySQL database."""
        cls.connection = MySQLdb.connect(host="localhost",
                                         user=os.environ['HBNB_MYSQL_USER'],
                                         passwd=os.environ['HBNB_MYSQL_PWD'],
                                         db=os.environ['HBNB_MYSQL_DB'])
        cls.cursor = cls.connection.cursor()

    @classmethod
    def tearDownClass(cls):
        """Close the MySQL database connection."""
        cls.cursor.close()
        cls.connection.close()

    def setUp(self):
        """Reset database to a known state before each test."""
        TestDBStorageMySQLDirect.cursor.execute("START TRANSACTION;")

    def tearDown(self):
        """Clean up after each test."""
        TestDBStorageMySQLDirect.cursor.execute("ROLLBACK;")

    def get_table_count(self, table):
        """Helper method to count records in a given table."""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return self.cursor.fetchone()[0]

    def test_state_creation(self):
        """Test state creation using direct MySQL commands."""
        initial_count = self.get_table_count('states')
        new_state = State(name="TestState")
        storage.new(new_state)
        storage.save()
        new_count = self.get_table_count('states')
        self.assertEqual(new_count, initial_count + 1, "State creation failed")

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
