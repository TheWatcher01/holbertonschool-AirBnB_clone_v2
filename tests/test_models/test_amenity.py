#!/usr/bin/python3
"""
Test module for the Amenity class.
"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


class TestAmenity(test_basemodel):
    """
    Test class for verifying the Amenity model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the tests for the Amenity class by specifying the model
        name and class.
        """
        super().__init__(*args, **kwargs)
        self.model_name = "Amenity"
        self.model_class = Amenity

    def test_name_attribute(self):
        """
        Test that the 'name' attribute of an Amenity instance is always a
        non-null string.
        """
        # Create an Amenity instance with a valid name.
        amenity_with_name = self.model_class(name="Wifi")
        # Verify that the 'name' attribute is a string and is not None.
        self.assertIsInstance(amenity_with_name.name, str,
                              "The 'name' attribute should be a string.")
        self.assertIsNotNone(amenity_with_name.name,
                             "The 'name' attribute should not be None.")
