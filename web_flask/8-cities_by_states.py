#!/usr/bin/python3

"""
File: 8-cities_by_states.py
Author: TheWatcher01
Date: 2024-04-10
Description: Initiates a Flask web application that listens on 0.0.0.0,
port 5000. It displays a HTML page with all State objects from DBStorage,
sorted by name (A->Z), and their associated City objects, also sorted by
name (A->Z), under the route /cities_by_states.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Fetches all State objects from storage, sorts them by name,
    and also sorts each state's cities by name before passing them
    to the template for rendering.
    """
    states = list(storage.all(State).values())
    states.sort(key=lambda state: state.name)
    for state in states:
        state.cities.sort(key=lambda city: city.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_session(exception=None):
    """Closes the SQLAlchemy session after each request."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
