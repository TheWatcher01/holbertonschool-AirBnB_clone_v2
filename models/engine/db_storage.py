#!/usr/bin/python3
"""
Module: db_storage.py
Author: TheWatcher01
Date: 2024-03-25
Description: This module defines the DBStorage class for interactions with
MySQL databases using SQLAlchemy ORM. It supports initialization, CRUD
operations, and session management tailored to the hbnb project's requirements.
"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from models.amenity import Amenity
from models.base_model import Base
from models.review import Review
from models.state import State
from models.place import Place
from models.user import User
from models.city import City
from venv import logger
from os import getenv
import logging

logger = logging.getLogger(__name__)


class DBStorage:
    """
    Class manages storage of hbnb models in MySQL database using SQLAlchemy.
    It encapsulates database engine and session management, providing methods
    to interact with the database.
    """
    __engine = None  # SQLAlchemy engine instance
    __session = None  # SQLAlchemy session instance

    def __init__(self):
        """
        Initializes the DBStorage instance by creating an engine linked to
        MySQL database specified via environment variables. It conditionally
        drops all tables if the environment is set to 'test'.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        conn_str = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(conn_str, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def _query_cls(self, cls):
        """
        Helper method to query objects of given class from database.
        """
        return {f'{obj.__class__.__name__}.{obj.id}': obj
                for obj in self.__session.query(cls).all()}

    def all(self, cls=None):
        """
        Queries and returns all objects of a given class from database.
        If no class is specified, it returns all objects/cls in database.
        """
        class_dict = {"State": State, "City": City, "User": User,
                      "Review": Review, "Amenity": Amenity, "Place": Place}
        if cls:
            # If cls is string, convert it to correspondant class/object
            if isinstance(cls, str):
                cls = class_dict.get(cls, None)
            # Query database for all objects of the class
            if cls is not None:
                return self._query_cls(cls)
        else:
            # If no class specified, return all objects/cls in database
            result = {}
            for cls in class_dict.values():
                result.update(self._query_cls(cls))
            return result

    def new(self, obj):
        """
        Adds a new object to the current database session, ready for commit.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session to the database.
        If error occurs during commit, it rolls back session to previous state,
        logs the error, and re-raises the exception.
        """
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            logger.error(f'SQLAlchemy Exception during commit: {e}')
            raise e

    def delete(self, obj=None):
        """
        Deletes an object from the current database session, if it's not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Recreates the database schema and initializes a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """
        Closes the current SQLAlchemy session, ensuring clean-up.
        """
        self.__session.remove()
