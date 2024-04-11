#!/usr/bin/python3

"""
File: 9-states.py
Author: TheWatcher01
Date: 2024-04-10
Description: Initiates a Flask web application that listens on 0.0.0.0,
port 5000. It displays a HTML page with all State objects from DBStorage,
sorted by name (A->Z), and their associated City objects, also sorted by
name (A->Z), under the route /states.
"""

from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__, template_folder='templates')


@app.route('/states', strict_slashes=False)
def states():
    """
    Fetches all State objects from storage, sorts them by name,
    and also sorts each state's cities by name before passing them
    to the template for rendering.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state(id):
    """
    Fetches a State object with the given id from storage, sorts its cities
    by name, and passes it to the template for rendering.
    """
    for state in storage.all(State).values():
        if state.id == id:
            state.cities = sorted(state.cities, key=lambda city: city.name)
            return render_template('9-states.html', state=state)
    return render_template('9-states.html'), 404


@app.teardown_appcontext
def close_session(exception):
    """Closes the SQLAlchemy session after each request."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
