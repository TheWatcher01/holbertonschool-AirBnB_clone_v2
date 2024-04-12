#!/usr/bin/python3

"""
File: 10-hbnb_filters.py
Author: TheWatcher01
Date: 2024-04-10
Description: Initiates a Flask web application that listens on 0.0.0.0,
port 5000. It displays HTML page with all State, City, and Amenity objects
from DBStorage, sorted by name (A->Z), under the route /hbnb_filters.
"""

from flask import Flask, render_template
from models.amenity import Amenity
from models.state import State
from models.city import City
from models import storage

# Create a Flask web server instance
app = Flask(__name__, template_folder='templates')


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Fetch all State, City, & Amenity objects from storage, sort them by name,
    and pass them to the template for rendering.
    """
    # Fetch and sort all State objects by name
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    for state in states:
        # Sort cities of each state by name
        state.cities = sorted([city for city in state.cities],
                              key=lambda city: city.name)
    # Fetch and sort all City objects by name
    cities = sorted(storage.all(City).values(), key=lambda city: city.name)
    # Fetch and sort all Amenity objects by name
    amenities = sorted(storage.all(Amenity).values(),
                       key=lambda amenity: amenity.name)
    # Render the template with the fetched data
    return render_template('10-hbnb_filters.html', states=states,
                           cities=cities, amenities=amenities)


@app.teardown_appcontext
def close_session(exception=None):
    """
    Close the SQLAlchemy session after each request to free up resources
    and avoid database locks.
    """
    storage.close()


if __name__ == "__main__":
    # Run the Flask web server
    app.run(host="0.0.0.0", port=5000, debug=False)
