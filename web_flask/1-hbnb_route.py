#!/usr/bin/python3

"""
File: 1-hbnb_route.py
Author: TheWatcher01
Date: 2024-04-08
Description: This is a script that starts a Flask web application
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Return a string with a message Hello HBNB!
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Return a string with a message HBNB
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
