#!/usr/bin/python3
"""
Module: db_storage.py
Author: Teddy Deberdt
Date: 2024-03-25
Description: This module defines the DBStorage class for interactions with
MySQL databases using SQLAlchemy ORM. It supports initialization, CRUD
operations, and session management tailored to the hbnb project's requirements.
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from models.base_model import Base
from os import getenv
from contextlib import closing


class DBStorage:
    """
    Class manages storage of hbnb models in MySQL database using SQLAlchemy.
    It encapsulates database engine and session management, providing methods
    to interact with the database.
    """
    __engine = None
    __session = None

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

    def all(self, cls=None):
        """
        Queries and returns all objects of a given class from the database.
        If no class is specified, it returns all objects in the database.
        """
        query_result = {}
        with closing(self.__session()) as session:
            if cls:
                objects = session.query(cls).all()
                query_result = {
                    f'{inspect(obj).class_.__name__}.{obj.id}': obj
                    for obj in objects}
            else:
                for cls in Base._decl_class_registry.values():
                    if hasattr(cls, '__tablename__'):
                        objects = session.query(cls).all()
                        for obj in objects:
                            key = f'{inspect(obj).class_.__name__}.{obj.id}'
                            query_result[key] = obj
        return query_result

    def new(self, obj):
        """
        Adds a new object to the current database session, ready for commit.
        """
        with closing(self.__session()) as session:
            session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session to the database.
        Handles exceptions by rolling back the session to the previous state.
        """
        with closing(self.__session()) as session:
            try:
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(f'SQLAlchemy Exception: {e}')

    def delete(self, obj=None):
        """
        Deletes an object from the current database session, if it's not None.
        """
        if obj:
            with closing(self.__session()) as session:
                session.delete(obj)

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
