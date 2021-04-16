from flask_admin.base import Admin
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import backref
from flask_login import UserMixin

db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db

class UserModel(db.Model, UserMixin):  
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)