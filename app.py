from datetime import timedelta

from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT
from security import authenticate, identify
from ressources.user import UserRegister
#web Its very important to imoort all models that Sqlachemy can create the tables
from ressources.item import Item, ItemList
from ressources.store import Store, StoreList
app = Flask(__name__)
# sqlalchemy has its own modification tracker
# the line bellow turn off the flask SQLAlchemy modification tracker
# thos only changing the extension behaviours and not the underling SQLAlchemy behaviors
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# this is will create all tables unless they exist already,
@app.before_first_request
def create_tables():
    db.create_all()







#authentification
app.secret_key ='jose'
# Authentication URL
#If we want to change the url to the authentication endpoint, for instance, we want to use/login instead of /auth , we can do something like this:
app.config['JWT_AUTH_URL_RULE'] = '/login'
# Token Expiration Time
# config JWT to expire within half an hour(60*30)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'



jwt = JWT(app, authenticate, identify)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ =="__main__":
    # we import this here because of a  circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)