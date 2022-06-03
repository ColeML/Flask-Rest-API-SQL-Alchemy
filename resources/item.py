from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="store_id field cannot be left blank!")

    def get(self, name: str):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
        except:
            return {'message': "An error occurred retrieving the item."}, 500
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name: str):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price, item.store_id = data['price'], data['store_id']

        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
