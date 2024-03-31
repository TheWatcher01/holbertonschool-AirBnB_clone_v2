#!/usr/bin/python3
"""
Test module for the City class.
Improvements include validation against foreign
key constraints and enhanced checks.
"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.state import State
from models import storage


class TestCity(test_basemodel):
    """
    Test class for verifying the City model with improved checks.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize tests for City class by specifying the class.
        """
        super().__init__(*args, **kwargs)
        self.model_class = City

    def setUp(self):
        """
        Set up method to create State instance as prerequisite for City tests.
        """
        self.test_state = State(name="Test State")
        storage.new(self.test_state)
        storage.save()

    def tearDown(self):
        """
        Tear down method to clean up after tests.
        """
        storage.delete(self.test_state)
        storage.save()

    def test_state_id_attribute(self):
        """
        Test that 'state_id' attribute of City instance correctly references
        existing State.
        """
        # Create a City instance with a valid state_id from setUp State.
        city_with_state_id = self.model_class(
            state_id=self.test_state.id, name="Test City")
        storage.new(city_with_state_id)
        storage.save()
        # Verify that the 'state_id' attribute references the valid State.
        self.assertEqual(
            city_with_state_id.state_id,
            self.test_state.id,
            "The 'state_id' attribute should reference an existing State ID."
        )

    def test_name_attribute(self):
        """
        Test that 'name' attribute of City instance is always non-null string.
        """
        city_with_name = self.model_class(
            name="Test City", state_id=self.test_state.id)
        self.assertIsInstance(city_with_name.name, str,
                              "The 'name' attribute should be a string.")
        self.assertIsNotNone(city_with_name.name,
                             "The 'name' attribute should not be None.")
