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

# Determine the storage type from the 'HBNB_TYPE_STORAGE' environment variable
storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    # Use the database storage engine if 'HBNB_TYPE_STORAGE' is 'db'
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # Default to file storage if 'HBNB_TYPE_STORAGE' is not 'db'
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Initialize the storage engine to load any pre-existing data
storage.reload()
