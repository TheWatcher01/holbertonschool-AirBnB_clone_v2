#!/usr/bin/python3
"""Test module for the Amenity class."""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """Tests for the Amenity class."""

    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test that name attribute of Amenity can only be non-empty string."""
        new = self.value(name="WiFi")
        self.assertTrue(isinstance(new.name, str) and new.name != "")
