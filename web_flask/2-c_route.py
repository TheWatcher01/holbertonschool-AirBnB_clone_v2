#!/usr/bin/python3

"""
File: 2-c_route.py
Author: TheWatcher01
Date: 2024-04-08
Description: This script initiates a Flask web application that listens on
0.0.0.0, port 5000, with three routes. The first route, '/', displays the
message "Hello HBNB!". The second route, '/hbnb', displays the message "HBNB".
The third route, '/c/<text>', displays the message "C " followed by the value
of the text variable, with underscores replaced by spaces.
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    This function returns the string "Hello HBNB!" when the route '/' is
    requested.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    This function returns the string "HBNB" when the route '/hbnb' is
    requested.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_c(text):
    """
    This function returns a string that starts with "C ", followed by the
    value of the text variable, with underscores replaced by spaces, when the
    route '/c/<text>' is requested.
    """
    return "C " + text.replace("_", " ")


if __name__ == "__main__":
    """
    This conditional ensures that the Flask application only runs if the script
    is executed directly and not used as an imported module.
    """
    app.run(host='0.0.0.0', port=5000)
