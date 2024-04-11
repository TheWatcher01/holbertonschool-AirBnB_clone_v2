#!/usr/bin/python3

"""
File: 10-hbnb_filters.py
Author: TheWatcher01
Date: 2024-04-10
Description: Initiates a Flask web application that listens on 0.0.0.0,
port 5000. It displays a HTML page with all State, City, and Amenity objects
from DBStorage, sorted by name (A->Z), under the route /hbnb_filters.
"""

from flask import Flask, render_template
from models.amenity import Amenity
from models.state import State
from models.city import City
from models import storage


app = Flask(__name__, template_folder='templates')


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Fetche all State, City, & Amenity objects from storage, sorts them by name,
    and passes them to the template for rendering.
    """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    cities = sorted(storage.all(City).values(), key=lambda city: city.name)
    amenities = sorted(storage.all(Amenity).values(),
                       key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html', states=states,
                           cities=cities, amenities=amenities)


@app.teardown_appcontext
def close_session(exception=None):
    """Closes the SQLAlchemy session after each request."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
