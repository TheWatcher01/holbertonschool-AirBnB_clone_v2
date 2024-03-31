#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """Tests for the Place model."""

    def __init__(self, *args, **kwargs):
        """Initialize test case."""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test city_id attribute."""
        new = self.value()
        self.assertIsNone(new.city_id)

    def test_user_id(self):
        """Test user_id attribute."""
        new = self.value()
        self.assertIsNone(new.user_id)

    def test_name(self):
        """Test name attribute."""
        new = self.value()
        self.assertIsNone(new.name)

    def test_description(self):
        """Test description attribute."""
        new = self.value()
        self.assertIsNone(new.description)

    def test_number_rooms(self):
        """Test number_rooms attribute."""
        new = self.value()
        self.assertEqual(new.number_rooms, 0)

    def test_number_bathrooms(self):
        """Test number_bathrooms attribute."""
        new = self.value()
        self.assertEqual(new.number_bathrooms, 0)

    def test_max_guest(self):
        """Test max_guest attribute."""
        new = self.value()
        self.assertEqual(new.max_guest, 0)

    def test_price_by_night(self):
        """Test price_by_night attribute."""
        new = self.value()
        self.assertEqual(new.price_by_night, 0)

    def test_latitude(self):
        """Test latitude attribute."""
        new = self.value()
        self.assertIsNone(new.latitude)

    def test_longitude(self):
        """Test longitude attribute."""
        new = self.value()
        self.assertIsNone(new.longitude)

    def test_amenity_ids(self):
        """Test amenity_ids attribute."""
        new = self.value()
        self.assertEqual(new.amenity_ids, [])
