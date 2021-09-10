
import os
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from flask_sqlalchemy import SQLAlchemy
# from db import db
import json

database_name = "actingagency"
username = 'postgres'
password = '1234'
url = 'localhost:5432'
database_path = "postgresql://{}:{}@{}/{}".format(
    username, password, url, database_name)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie = Movie(
        title='Yes Day',
        release_date= datetime(2021, 3, 12)
    )

    movie.insert()
    
    actor = Actor(
        name='Jennifer Garner',
        age= 49,
        gender='Female'
    )

    actor.insert()
'''
Movie

'''
class Movie(db.Model):  
  __tablename__ = 'Movies'

  # Autoincrementing, unique primary key
  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  title = Column(String,  unique=True, nullable=False)
  release_date  = Column(DateTime, nullable=False)


  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date


  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date,
    }

'''
Actors

'''
class Actor(db.Model):  
  __tablename__ = 'Actors'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  age = Column(Integer)
  gender = Column(String)
  


  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender,
    }