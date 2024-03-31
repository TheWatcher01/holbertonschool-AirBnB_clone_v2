#!/usr/bin/python3
"""
Test module for the City class.
"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class TestCity(test_basemodel):
    """
    Test class for verifying the City model.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the tests for the City class by specifying the model
        name and class.
        """
        super().__init__(*args, **kwargs)
        self.model_name = "City"
        self.model_class = City

    def test_state_id_attribute(self):
        """
        Test that the 'state_id' attribute of a City instance is always a
        non-null string.
        """
        # Create a City instance with a valid state_id.
        city_with_state_id = self.model_class(state_id="some_state_id")
        # Verify that the 'state_id' attribute is a string and is not None.
        self.assertIsInstance(city_with_state_id.state_id, str,
                              "The 'state_id' attribute should be a string.")
        self.assertIsNotNone(city_with_state_id.state_id,
                             "The 'state_id' attribute should not be None.")

    def test_name_attribute(self):
        """
        Test that the 'name' attribute of a City instance is always a
        non-null string.
        """
        # Create a City instance with a valid name.
        city_with_name = self.model_class(name="Test City")
        # Verify that the 'name' attribute is a string and is not None.
        self.assertIsInstance(city_with_name.name, str,
                              "The 'name' attribute should be a string.")
        self.assertIsNotNone(city_with_name.name,
                             "The 'name' attribute should not be None.")
