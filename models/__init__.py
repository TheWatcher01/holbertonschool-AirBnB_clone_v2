#!/usr/bin/python3
"""
Module: __init__.py
Author: TheWatcher01
Date: 2024-03-27
Description: This module is responsible for initializing the storage engine.
The type of storage engine is determined by the 'HBNB_TYPE_STORAGE' environment
variable. It supports 'db' for DBStorage (database storage) and 'file' for
FileStorage (file storage).
"""

# Importing the getenv function from the os module. This function is used to
# read the environment variable.
from os import getenv

# Checking the value of the 'HBNB_TYPE_STORAGE' environment variable. If it's
# 'db', DBStorage engine is used. Otherwise, FileStorage engine is used.
if getenv('HBNB_TYPE_STORAGE') == 'db':
    # Importing the DBStorage class from the models.engine.db_storage module.
    from models.engine.db_storage import DBStorage
    # Creating an instance of the DBStorage class.
    storage = DBStorage()
else:
    # Importing FileStorage class from models.engine.file_storage module.
    from models.engine.file_storage import FileStorage
    # Creating an instance of the FileStorage class.
    storage = FileStorage()

# Calling the reload method of the storage instance. This method is responsible
# for deserializing the JSON file to objects.
storage.reload()
