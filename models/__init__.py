#!/usr/bin/python3
"""
Module: __init__.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module initializes the storage engine based on the
environment variable 'HBNB_TYPE_STORAGE'.
"""
from os import getenv

# Check the environment variable 'HBNB_TYPE_STORAGE' to determine the type
# of storage to use.
if getenv('HBNB_TYPE_STORAGE') == 'db':
    # If 'HBNB_TYPE_STORAGE' is 'db', use the DBStorage engine.
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # If 'HBNB_TYPE_STORAGE' is not 'db', use the FileStorage engine.
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Call the reload method on the storage engine to load any existing data.
storage.reload()
