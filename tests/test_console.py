#!/usr/bin/python3
"""
Fichier: test_console.py
Auteur: Teddy Deberdt
Date: 2024-03-25
Description: Tests pour vérifier les améliorations apportées à la console HBNB.
"""
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
import unittest
from models.engine.file_storage import FileStorage
from models import storage


class TestDoCreate(unittest.TestCase):

    def setUp(self):
        """Configuration avant chaque test."""
        self.patcher_out = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_out.start()
        self.addCleanup(self.patcher_out.stop)
        self.patcher_storage_new = patch.object(storage, 'new', autospec=True)
        self.patcher_storage_save = patch.object(
            storage, 'save', autospec=True)
        self.mock_storage_new = self.patcher_storage_new.start()
        self.mock_storage_save = self.patcher_storage_save.start()
        self.addCleanup(self.patcher_storage_new.stop)
        self.addCleanup(self.patcher_storage_save.stop)

    def test_create_missing_class_name(self):
        """Teste la réaction à l'absence du nom de classe."""
        HBNBCommand().do_create('')
        self.assertEqual("** class name missing **\n",
                         self.mock_stdout.getvalue())

    def test_create_class_does_not_exist(self):
        """Teste la réaction à un nom de classe invalide."""
        HBNBCommand().do_create('NonExistentClass')
        self.assertEqual("** class doesn't exist **\n",
                         self.mock_stdout.getvalue())

    def test_create_attribute_format_error(self):
        """Teste la réaction à un format d'attribut malformé."""
        HBNBCommand().do_create('User email="user@example.com" Password')
        expected_error = "** attribute format error **: Password"
        expected_error += " (expected key=value)"
        self.assertTrue(expected_error in self.mock_stdout.getvalue())

    def test_create_with_valid_attributes(self):
        """Teste la création avec des attributs valides."""
        cmd = 'Place city_id="0001" user_id="0001" name="My_little_house"'
        cmd += ' number_rooms=4 number_bathrooms=2 max_guest=10'
        cmd += ' price_by_night=300 latitude=37.773972 longitude=-122.431297'
        HBNBCommand().do_create(cmd)
        self.assertTrue(self.mock_storage_new.called)
        self.assertTrue(self.mock_storage_save.called)

    def test_create_with_mixed_types_attributes(self):
        """Teste la création avec des attributs de types mixtes."""
        cmd = 'Place name="My_little_house" number_rooms=4'
        cmd += ' latitude=37.773972 longitude=-122.431297'
        HBNBCommand().do_create(cmd)

    def test_create_with_complex_string_attributes(self):
        """Teste la création avec des chaînes complexes comme attributs."""
        cmd = 'Place name="\"My little house\""'
        HBNBCommand().do_create(cmd)

    def test_create_with_incomplete_attributes(self):
        """Teste la création avec des spécifications d'attributs incomplètes."""
        HBNBCommand().do_create('User email=')
        self.assertIn("** attribute format error **",
                      self.mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
