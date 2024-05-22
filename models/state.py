#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City
import models
import shlex


class State(BaseModel, Base):
    """ State class with attrbutes:
        name.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """
        getter for list of city instances related to the state
        """
        city_list = []
        for city in models.storage.all(City).values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
#        all_var = models.storage.all()
#        lst = []
#        for key in all_var:
#           city = key.replace('.', ' ')
#           city = shlex.split(city)
#            if (city[0] == 'City'):
#                lst.append(all_var[key])
#        res = []
#        for i in lst:
#            if (i.state_id == self.id):
#                res.append(i)
#        return (res)
