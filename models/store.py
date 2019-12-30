import sqlite3
from db import db

class StoreModel(db.Model):
    # we have to
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # we can do a back referenece, it allow the store to see which items are in the items database
    items = db.relationship('ItemModel', lazy='dynamic') # this variable is a list of items many to one relationship
    # could be many items with the same store id
    #lazy='dynamaic' : to tell sqlachemy do not retrieve items in less we need that
    # when we use lazy dynamic self.items become a query builder that has the ability to look inti the items table , we us e.all() to look into the items
    #table

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1 #this is will return an ItemModel project
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     # return cls(row[0], row[1])
        #     return cls(*row)

    def save_to_db(self):
        # will save the model in the database
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
