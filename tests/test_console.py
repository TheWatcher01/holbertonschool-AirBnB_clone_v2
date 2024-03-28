#!/usr/bin/python3
"""
File: test_console.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: Tests for HBNB console command 'create' with improved test
coverage and practices.
"""
from unittest.mock import patch, MagicMock
from console import HBNBCommand
from models import storage
from io import StringIO
import unittest


class TestDoCreate(unittest.TestCase):
    """Test suite for the 'create' command in the HBNB console."""

    def setUp(self):
        """Set up common test resources and mock objects."""
        self.mock_stdout = patch('sys.stdout',
                                 new_callable=StringIO).start()
        self.mock_storage_new = patch(
            'models.storage.new', MagicMock()).start()
        self.mock_storage_save = patch(
            'models.storage.save', MagicMock()).start()

    def tearDown(self):
        """Clean up resources and stop all patches."""
        patch.stopall()

    def test_create_without_parameters(self):
        """Ensure error message for missing class name."""
        HBNBCommand().do_create('')
        self.assertEqual("** class name missing **\n",
                         self.mock_stdout.getvalue())

    def test_create_class_does_not_exist(self):
        """Ensure error message for non-existent class."""
        HBNBCommand().do_create('NonExistentClass')
        self.assertEqual("** class doesn't exist **\n",
                         self.mock_stdout.getvalue())

    def test_create_attribute_format_error(self):
        """Test for malformed attribute format."""
        HBNBCommand().do_create('User email="user@example.com" Password')
        self.assertIn(
            "** attribute format error **: Password "
            "(expected key=value)", self.mock_stdout.getvalue())

    def test_create_with_valid_attributes(self):
        """Validate object creation with correct attributes."""
        HBNBCommand().do_create(
            'Place city_id="0001" user_id="0001" name="My_little_house" '
            'number_rooms=4 number_bathrooms=2 max_guest=10 '
            'price_by_night=300 latitude=37.773972 longitude=-122.431297')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_mixed_types_attributes(self):
        """Test creation with attributes of mixed types."""
        HBNBCommand().do_create(
            'Place name="My_little_house" number_rooms=4 '
            'latitude=37.773972 longitude=-122.431297')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_complex_string_attributes(self):
        """Test creation with complex string attr containing escape sequence"""
        HBNBCommand().do_create('Place name="\"My little house\""')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_incomplete_attributes(self):
        """Ensure error message for incomplete attribute specifications."""
        HBNBCommand().do_create('User email=')
        self.assertIn("** attribute format error **",
                      self.mock_stdout.getvalue())

    def test_create_with_malformatted_parameters(self):
        """Test create command with malformatted parameters"""
        HBNBCommand().do_create('State name=California "population=800K"')
        self.assertIn("** attribute format error **",
                      self.mock_stdout.getvalue())

    def test_create_persistence(self):
        """Test create command persistence"""
        HBNBCommand().do_create('State name="Hawaii"')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)
        storage.reload()
        state = list(storage.all("State").values())[-1]
        self.assertEqual(state.name, "Hawaii")


if __name__ == "__main__":
    unittest.main()
