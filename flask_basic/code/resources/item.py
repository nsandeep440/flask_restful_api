from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)
# from code.models.item import ItemModel
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every ITEM requires store if'
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item does not exists'}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': ' This item {} Already exists'.format(name)}, 400 # bad request
        data = Item.parser.parse_args()
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['isAdmin']:
            return {'message': 'Admin access is required'}, 401
        
        itemModel = ItemModel.find_by_name(name)
        if itemModel:
            itemModel.delete_from_db()
        return {'message': 'Item {} deleted'.format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        print(data)
        itemModel = ItemModel.find_by_name(name)

        if itemModel:
            itemModel.price = data['price']
        else:
            itemModel = ItemModel(name, data['price'], data['store_id'])

        print(itemModel.price)

        itemModel.save_to_db()

        return itemModel.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200      
        return {
                'items': [item['name'] for item in items],
                'message': 'Mode info is available, if you log-in'
            }, 200
