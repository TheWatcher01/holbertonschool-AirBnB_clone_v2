#!/usr/bin/env python3
"""
File: __init__.py
Author: TheWatcher01
Date: 2024-03-27
Description: Initialize the storage engine
"""
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
