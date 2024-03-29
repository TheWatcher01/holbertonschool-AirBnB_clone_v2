#!/usr/bin/python3
"""
Module: __init__.py
Author: Teddy Deberdt
Date: 2024-03-27
Description: This module initializes the storage engine based on the
HBNB_TYPE_STORAGE environment variable and the HBNB_ENV for environment
management. It supports 'db' for DBStorage (database storage) and 'file' for
FileStorage (file storage). Configurations differ based on whether the
environment is development, test, or production.
"""

import os
import subprocess

# Determine the running environment. Default to 'dev' if not specified.
env = os.getenv('HBNB_ENV', 'dev')

# Define the paths to the configuration files for each environment.
config_files = {
    'dev': ('/home/thewatcher/Holberton/'
            'holbertonschool-AirBnB_clone_v2/setup_mysql_dev.sql'),
    'test': ('/home/thewatcher/Holberton/'
             'holbertonschool-AirBnB_clone_v2/setup_mysql_test.sql'),
    'prod': ('/home/thewatcher/Holberton/'
             'holbertonschool-AirBnB_clone_v2/setup_mysql_prod.sql'),
}

# Initialize the storage engine based on the HBNB_TYPE_STORAGE variable.
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Set the root password for initial execution.
root_password = 'hbnb_root_pwd'

# Execute the SQL configuration script for the current environment.
config_file = config_files.get(env)
if config_file:
    try:
        # Execute the script as root.
        subprocess.run(['mysql', '-u', 'root', f'-p{root_password}', '-e',
                        f"source {config_file}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {config_file}: {e}")

# Reload the storage engine to apply the new configuration.
storage.reload()
