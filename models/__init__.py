#!/usr/bin/python3
"""
Module: __init__.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: Initializes the storage engine based on the environment variable
'HBNB_TYPE_STORAGE'. Supports 'db' for database storage using DBStorage and
'file' for file storage using FileStorage.
"""

from os import getenv

# Map storage types to their corresponding classes
storage_types = {
    'db': 'models.engine.db_storage.DBStorage',
    'file': 'models.engine.file_storage.FileStorage'
}

# Determine the storage type from the 'HBNB_TYPE_STORAGE' environment variable
storage_type = getenv('HBNB_TYPE_STORAGE', 'file')

# Use the specified storage type, or default to file storage
try:
    storage_class = __import__(storage_types[storage_type], fromlist=[''])
    storage = storage_class()
except KeyError:
    raise Exception("Invalid storage type: {}".format(storage_type))

# Initialize the storage engine to load any pre-existing data
storage.reload()
