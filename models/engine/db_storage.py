#!/usr/bin/python3
"""
Module: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: This module defines the DBStorage class for interactions with
MySQL databases using SQLAlchemy ORM. It supports initialization, CRUD
operations, and session management tailored to the hbnb project's requirements.
"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv


class DBStorage:
    """
    Class manages storage of hbnb models in MySQL database using SQLAlchemy.
    It encapsulates database engine and session management, providing methods
    to interact with the database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage instance."""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        conn_str = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(conn_str, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables for a clean test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries and returns all objects of a given class or all objects."""
        session = self.__session()
        if cls:
            objects = session.query(cls).all()
        else:
            classes = [State, City, User, Review, Amenity, Place]
            objects = [
                item for cls in classes for item in session.query(cls).all()]

        return {f'{obj.__class__.__name__}.{obj.id}': obj for obj in objects}

    def new(self, obj):
        """Adds a new object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database."""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            # Consider logging this exception as well
            print(f'SQLAlchemy Exception: {e}')

    def delete(self, obj=None):
        """Deletes an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all tables from the database and recreates the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Closes the current SQLAlchemy session."""
        self.__session.remove()
