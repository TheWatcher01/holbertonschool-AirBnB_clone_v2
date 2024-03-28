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

# Define required environment variables for DBStorage
required_vars = ['HBNB_MYSQL_USER', 'HBNB_MYSQL_PWD',
                 'HBNB_MYSQL_HOST', 'HBNB_MYSQL_DB']

if storage_type == 'db':
    # Check if all required configurations for DBStorage are present
    missing_vars = [var for var in required_vars if not getenv(var)]
    if missing_vars:
        print(
            f"Missing env. variables for DBStorage: {', '.join(missing_vars)}")
        print("Falling back to FileStorage.")
        from models.engine.file_storage import FileStorage
        storage = FileStorage()
    else:
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

try:
    # Initialize the storage engine to load any pre-existing data
    storage.reload()
except Exception as e:
    print(f"Error loading storage: {e}")
    if storage_type == 'db':
        print("Make sure database is accessible & credentials are correct.")
    else:
        print("Check the integrity of your JSON file.")
