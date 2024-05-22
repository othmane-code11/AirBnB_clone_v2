#!/usr/bin/python3
""" Database storage module """
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """create tables in environmental."""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)
        env = getenv("HBNB_ENV")
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depend on the class name"""
        dictn = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            for obj in self.__session.query(cls).all():
                key = f"{type(obj).__name__}.{obj.id}"
                try:
                    cls_str = ['State', 'City', 'User', 'Place', 'Review', 'Amenity']
                    if obj.__class__.__name__ in cls_str:
                        del obj._sa_instance_state
                        dictn[key] = obj
                    else:
                        dictn[key] = obj
                except Exception:
                    pass

        else:
            classes = [State, City, User, Place, Review, Amenity]
            for clas in classes:
                for obj in self.__session.query(clas).all():
                    key = f"{type(obj).__name__}.{obj.id}"
                    try:
                        cls_strr = ['State', 'City', 'User', 'Place', 'Review', 'Amenity']
                        if obj.__class__.__name__ in cls_strr:
                            del obj._sa_instance_state
                            dictn[key] = obj
                        else:
                            dictn[key] = obj
                    except Exception:
                        pass
        return dictn

    def new(self, obj):
        """
        Add the new object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and initialize session
        """
        Base.metadata.create_all(self.__engine)
        s_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s_f)
        self.__session = Session()

    def close(self):
        """
        Close the session.
        """
        self.__session.close()
