import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        print(item)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}
        #data = request.get_json(force = True, silent= True)
        data = Item.parser.parse_args()
        print(data)
        #item = {'name': data['name'], data['price']: 12.00}
        item = ItemModel(name, **data)
        # print(item)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 #Internal server error
        return item.json(), 201



    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}
    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, **data)
        print(type(updated_item))
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
        # return {'items' : [item.json() for item in ItemModel.query.all()]}