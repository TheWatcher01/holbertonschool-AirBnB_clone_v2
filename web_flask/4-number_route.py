#!/usr/bin/python3

"""
File: 4-number_route.py
Author: TheWatcher01
Date: 2024-04-08
Description: This script initiates a Flask web application that listens on
0.0.0.0, port 5000, with five routes. The routes are defined as follows:
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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text):
    """
    This function returns a string that starts with "Python ", followed by the
    value of the text variable, with underscores replaced by spaces, or "is
    cool" if text is not provided, when the route '/python/(<text>)?' is
    requested.
    """
    return "Python " + text.replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """
    This function returns a string that starts with "n is a number" only if n
    is an integer, when the route '/number/<n>' is requested.
    """
    return "{} is a number".format(n)


if __name__ == "__main__":
    """
    This conditional ensures that the Flask application only runs if the script
    is executed directly and not used as an imported module.
    """
    app.run(host='0.0.0.0', port=5000)