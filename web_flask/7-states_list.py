#!/usr/bin/python3

"""
File: 7-states_list.py
Author: TheWatcher01
Date: 2024-04-08
Description: This script initiates a Flask web application that listens on
0.0.0.0, port 5000. The routes are defined as follows:
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    states = list(storage.all(State).values())
    states.sort(key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
