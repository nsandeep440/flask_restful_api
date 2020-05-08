from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
                            'username',
                            type=str,
                            required=True,
                            help='Username cannot be blank'
                         )
_user_parser.add_argument(
                            'password',
                            type=str,
                            required=True,
                            help='Password cannot be blank'
                         )
    
class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already exists'}, 400

        userModel = UserModel(**data) #(data['username'], data['password'])
        userModel.save_to_db()

        return {'message': 'User created successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        print(user.id)
        return {'user': user.json()}

    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return  {'message': 'User deleted'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user_model = UserModel.find_by_username(data['username'])
        if user_model and safe_str_cmp(data['password'], user_model
                                       .password):
            access_token = create_access_token(identity=user_model.id, fresh=True)
            refresh_token = create_refresh_token(user_model.id)
            return {                
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credential'}, 401
         

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # a unique identifier for JWT (JTI)
        BLACKLIST.add(jti)
        return {'message': 'User logged out successfully'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            'access_token': new_token
        }, 200