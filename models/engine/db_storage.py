#!/usr/bin/python3
"""
File: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: Module that defines the DBStorage class
"""
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from os import getenv


class DBStorage:
    """Defines the DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization of DBStorage instance"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables if in test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending of the class name (cls)"""
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [State, City, User]  # Add other classes here
            objects = []
            for cls in classes:
                objects.extend(self.__session.query(cls).all())
        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Dispose the current Session"""
        self.__session.close()
