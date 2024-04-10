#!/usr/bin/python3

"""
File: 7-states_list.py
Author: TheWatcher01
Date: 2024-04-08
Description: This script initiates a Flask web application that listens on
0.0.0.0, port 5000. The route '/states_list' is defined to display a HTML page
with a list of all State objects from DBStorage, sorted alphabetically (A->Z).
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Fetches all State objects from storage, sorts them alphabetically,
    and passes them to the template for rendering.
    """
    states = list(storage.all(State).values())
    states_sorted = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=states_sorted)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the SQLAlchemy session after each request to free up resources
    and prevent memory leaks.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
