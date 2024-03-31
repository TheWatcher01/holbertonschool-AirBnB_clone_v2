#!/usr/bin/python3
"""
File: test_db_storage.py
Author: TheWatcher01
Date: 2024-03-31
Description: Unit tests for db_storage.py with a real database connection.
"""

import MySQLdb
import unittest
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

    def test_state_creation(self):
        """Test state creation using direct MySQL commands."""
        # Get the initial number of records in the 'states' table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Create a new State using SQLAlchemy to simulate normal operation
        from models import storage
        from models.state import State
        new_state = State(name="TestStateDirect")
        storage.new(new_state)
        storage.save()

        # Verify that the number of records has increased by 1
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]
        self.assertEqual(final_count, initial_count + 1,
                         "A new state record should have been added.")

        # Cleanup: delete the newly created state
        self.cursor.execute(
            "DELETE FROM states WHERE name = 'TestStateDirect'")
        storage.save()


if __name__ == "__main__":
    unittest.main()
