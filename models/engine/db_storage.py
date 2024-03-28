#!/usr/bin/python3
"""
Module: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: Defines the DBStorage class interacting with MySQL via SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from os import getenv


class DBStorage:
    """
    Handles interactions with the MySQL database through SQLAlchemy.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage instance, linking it to the MySQL database.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects of a class, or all types if none specified.
        """
        try:
            objects = self.__session.query(cls).all() if cls else [
                obj for cls in Base._decl_class_registry.values()
                if hasattr(cls, '__tablename__')
                for obj in self.__session.query(cls).all()
            ]
            return {f"{type(obj).__name__}.{obj.id}": obj
                    for obj in objects}
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Exception: {e}")
            return {}

    def new(self, obj):
        """
        Adds an object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            self.__session.rollback()
            print(f"SQLAlchemy Exception: {e}")

    def delete(self, obj=None):
        """
        Deletes an object from the current database session, if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Recreates all tables in the database and initializes the session.
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
        Closes the current session.
        """
        self.__session.close()
