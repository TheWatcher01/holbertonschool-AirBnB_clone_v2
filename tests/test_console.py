#!/usr/bin/python3
"""
File: test_console.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: Tests for HBNB console improvements, focusing on 'create' command.
"""
from models.engine.file_storage import FileStorage
from unittest.mock import patch, create_autospec
from console import HBNBCommand
from io import StringIO
import unittest


class TestDoCreate(unittest.TestCase):
    """Defines tests for the 'create' command of the HBNB console."""

    def setUp(self):
        """Set up mocks for sys.stdout and storage methods before each test."""
        self.mock_stdout = patch('sys.stdout', new_callable=StringIO).start()
        self.mock_storage_new = patch(
            'models.storage.new', autospec=True).start()
        self.mock_storage_save = patch(
            'models.storage.save', autospec=True).start()

    def tearDown(self):
        """Stop all patches."""
        patch.stopall()

    def test_create_missing_class_name(self):
        """Test 'create' command with missing class name."""
        HBNBCommand().do_create('')
        self.assertEqual("** class name missing **\n",
                         self.mock_stdout.getvalue())

    def test_create_class_does_not_exist(self):
        """Test 'create' command with a non-existent class."""
        HBNBCommand().do_create('NonExistentClass')
        self.assertEqual("** class doesn't exist **\n",
                         self.mock_stdout.getvalue())

    def test_create_attribute_format_error(self):
        """Test 'create' command with incorrectly formatted attribute."""
        HBNBCommand().do_create('User email="user@example.com" Password')
        self.assertIn(
            "** attribute format error **: Password (expected key=value)",
            self.mock_stdout.getvalue())

    def test_create_with_valid_attributes(self):
        """Test 'create' command with valid attributes."""
        HBNBCommand().do_create(
            'Place city_id="0001" user_id="0001" name="My_little_house" '
            'number_rooms=4 number_bathrooms=2 max_guest=10 '
            'price_by_night=300 latitude=37.773972 longitude=-122.431297')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_mixed_types_attributes(self):
        """Test 'create' command with attributes of mixed types."""
        HBNBCommand().do_create(
            'Place name="My_little_house" number_rooms=4 '
            'latitude=37.773972 longitude=-122.431297')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_complex_string_attributes(self):
        """Test 'create' command with complex string attributes."""
        HBNBCommand().do_create('Place name="\"My little house\""')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_incomplete_attributes(self):
        """Test 'create' command with incomplete attribute specifications."""
        HBNBCommand().do_create('User email=')
        self.assertIn("** attribute format error **",
                      self.mock_stdout.getvalue())

    def test_create_with_invalid_attribute_format(self):
        """Test 'create' command reaction to an invalid attribute format."""
        HBNBCommand().do_create('User email=user@example.com')
        self.assertIn(
            "** attribute format error **: email=user@example.com "
            "(expected key=value)", self.mock_stdout.getvalue())

    def test_create_with_special_characters_in_attribute_values(self):
        """Test 'create' command with special characters in attribute values."""
        HBNBCommand().do_create('User password="p@ssw0rd"')
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)


if __name__ == "__main__":
    unittest.main()
