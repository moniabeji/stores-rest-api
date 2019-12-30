
import sqlite3
from db import db

# the use and the Item model gona to extend db.model
class UserModel(db.Model):
    # 2 - tell sqlalchemy where thiese models are going to be stored
    __tablename__ = 'users'  # this the table that will be created  in the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  # limit the size of username
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.something = "hi" # this property will exist in the object: but won't be related to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id)