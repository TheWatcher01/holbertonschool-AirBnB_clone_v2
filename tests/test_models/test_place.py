#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.city_id) == str or new.city_id is None)

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.user_id) == str or new.user_id is None)

    def test_name(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.name) == str or new.name is None)

    def test_description(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.description) ==
                        str or new.description is None)

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.number_rooms) ==
                        int or new.number_rooms is None)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.number_bathrooms) ==
                        int or new.number_bathrooms is None)

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.max_guest) == int or new.max_guest is None)

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertTrue(
            type(new.price_by_night) == int or new.price_by_night is None
        )

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.latitude) == float or new.latitude is None)

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertTrue(type(new.longitude) == float or new.longitude is None)

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)
