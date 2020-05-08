from flask_restful import Resource
from models.store_model import StoreModel

class Store(Resource):
    def get(self, name):
        storeModel = StoreModel.find_by_name(name)
        if storeModel:
            return storeModel.json()
        return {'message': 'Store: {} not found'.format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name: "{}" already exists'.format(name)}, 400

        storeModel = StoreModel(name)
        try:
            storeModel.save_to_db()
        except:
            return {'message': 'An error occured while saving data'}, 500
        return storeModel.json(), 201

    def delete(self, name):
        storeModel = StoreModel.find_by_name(name)
        if storeModel:
            storeModel.delete_from_db()

        return {'message': 'Store: "{}" deleted'.format(name)}


class StoreList(Resource):
    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {'stores': [store.json() for store in StoreModel.find_all()]}
