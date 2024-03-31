#!/usr/bin/python3
"""
Module: test_db_storage.py
Author: TheWatcher01
Date: 2024-03-31
Description: This module contains unit tests for the DBStorage class in the
storage module. It tests the methods all, new, save, delete, reload, and close.
"""

from models.base_model import Base
from models.state import State
from sqlalchemy import inspect
from models import storage
import unittest


class TestDBStorage(unittest.TestCase):
    """
    This class contains unit tests for the DBStorage class. It tests the
    methods all, new, save, delete, reload, and close.
    """

    @classmethod
    def setUpClass(cls):
        """
        This method sets up the class-level setup for the tests. It creates
        an instance of DBStorage for all test cases to use.
        """
        cls.storage = storage

    def test_all_no_class(self):
        """
        This test case checks that the all method returns all rows when no
        class is passed.
        """
        result = self.storage.all()
        self.assertIsInstance(result, dict)

    def test_all_with_class(self):
        """
        This test case checks that the all method returns all rows of the
        specified class.
        """
        result = self.storage.all(State)
        self.assertIsInstance(result, dict)

    def test_new(self):
        """
        This test case checks that the new method adds an object to the
        session.
        """
        state = State(name="California")
        self.storage.new(state)
        self.assertIn(state, self.storage._DBStorage__session)

    def test_save(self):
        """
        This test case checks that the save method correctly saves objects
        to the database.
        """
        state = State(name="Nevada")
        self.storage.new(state)
        self.storage.save()
        db_state = self.storage._DBStorage__session.query(State).get(state.id)
        self.assertEqual(state.id, db_state.id)

    def test_delete(self):
        """
        This test case checks that the delete method correctly deletes
        objects from the database.
        """
        state = State(name="Arizona")
        self.storage.new(state)
        self.storage.save()
        self.storage.delete(state)
        self.storage.save()
        db_state = self.storage._DBStorage__session.query(State).get(state.id)
        self.assertIsNone(db_state)

    def test_reload(self):
        """
        This test case checks that the reload method correctly creates all
        tables in the database.
        """
        Base.metadata.drop_all(self.storage._DBStorage__engine)
        self.storage.reload()
        inspector = inspect(self.storage._DBStorage__engine)
        tables = inspector.get_table_names()
        expected_tables = ['amenities', 'cities',
                           'places', 'reviews', 'states', 'users']
        self.assertCountEqual(tables, expected_tables)

    def test_close(self):
        """
        This test case checks that the close method correctly removes the
        session.
        """
        session = self.storage._DBStorage__session
        self.storage.close()
        self.assertNotEqual(session, self.storage._DBStorage__session)
