import sqlite3
from db import db

class ItemModel(db.Model):
    # we have to
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # now every ItemModel has a store, that is the store wich matches the store_id
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

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
