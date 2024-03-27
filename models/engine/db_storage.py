#!/usr/bin/python3
"""
Module: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: This module defines the DBStorage class, which interacts with the
MySQL database via SQLAlchemy.
"""
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

MODEL_CLASSES = [Amenity, City, Place, Review, State, User]

class DBStorage:
    """
    DBStorage class for interacting with the MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize DBStorage instance with engine linked to the MySQL database.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables if in test environment
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """
        Query all objects of a given class. If cls=None, query all types of objects.
        """
        objects = []
        if cls:
            objects.extend(self.__session.query(cls).all())
        else:
            for model_cls in MODEL_CLASSES:
                objects.extend(self.__session.query(model_cls).all())
        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects}


    def new(self, obj):
        """
        Add object to current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of current database session.
        """
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            print(f"Error saving to database: {e}")

    def delete(self, obj=None):
        """
        Delete obj from current database session if not None.
        """
        if obj:
            try:
                self.__session.delete(obj)
                self.__session.commit()
            except Exception as e:
                self.__session.rollback()
                print(f"Error deleting from database: {e}")

    def reload(self):
        """
        Create all tables in the database and create current database session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Dispose current Session.
        """
        self.__session.close()
