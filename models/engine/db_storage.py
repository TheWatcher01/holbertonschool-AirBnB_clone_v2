#!/usr/bin/python3
"""
Module: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: This module defines the DBStorage class, which interacts with the
MySQL database via SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from os import getenv


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
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables if in test environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects of a given class. If cls=None, query all types of
        objects.
        """
        try:
            objects = []
            if cls:
                objects = self.__session.query(cls).all()
            else:
                for cls in Base._decl_class_registry.values():
                    if hasattr(cls, '__tablename__'):
                        objects.extend(self.__session.query(cls).all())
            return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects}
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Exception: {e}")
            return {}

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
        except SQLAlchemyError as e:
            self.__session.rollback()
            print(f"SQLAlchemy Exception: {e}")

    def delete(self, obj=None):
        """
        Delete obj from current database session if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and create current database session.
        """
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(session_factory)
            self.__session = Session()
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Exception: {e}")

    def close(self):
        """
        Dispose current Session.
        """
        if self.__session:
            self.__session.close()
