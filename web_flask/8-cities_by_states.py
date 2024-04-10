#!/usr/bin/python3

"""
File: 8-cities_by_states.py
Author: TheWatcher01
Date: 2024-04-10
Description: Script initiates Flask web application that listens on 0.0.0.0,
port 5000. It renders HTML page that displays all State objects from DBStorage,
sorted alphabetically (A->Z), along with their associated City objects,
also sorted alphabetically (A->Z). Route for this page is /cities_by_states.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Function fetches all State objects from storage, sorts them alphabetically,
    and also sorts each state's cities alphabetically before passing them
    to the template for rendering.
    """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda state: state.name)
    for state in states_sorted:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('8-cities_by_states.html', states=states_sorted)


@app.teardown_appcontext
def close_session(exception=None):
    """
    This function closes the SQLAlchemy session after each request to free up
    resources and prevent memory leaks.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
