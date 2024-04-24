#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import tuple_


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''
        Creates a new user for DB
        '''
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by filtering the users table with the given arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter the users table

        Returns:
            User: The first User object found matching the filter criteria

        Raises:
            NoResultFound: If no user is found matching the filter criteria
            InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except (NoResultFound, InvalidRequestError) as e:
            self._session.rollback()
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes in the database

        Args:
            user_id: ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating user attributes

        Raises:
            ValueError: If an invalid argument is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            if not user:
                raise NoResultFound
            for attr, value in kwargs.items():
                if hasattr(User, attr):
                    setattr(user, attr, value)
                else:
                    raise ValueError(f"Invalid attribute '{attr}'")

            self._session.commit()
        except (NoResultFound, InvalidRequestError, ValueError) as e:
            self._session.rollback()
            raise e
