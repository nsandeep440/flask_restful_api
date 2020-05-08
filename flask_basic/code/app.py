from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

### import authenticate and identity function from security file
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' ### Root folder of our project
## it can be mysql, oracle sql, postgres any thing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXECPTIONS'] = True

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = 'sandeep' # app.config['JWT_SECRET_KEY']
api = Api(app)

### flask decorator to create tables
@app.before_first_request
def create_tables():
    db.create_all()

# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)
# pass app and security functions to JWT class

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # should read this form DB or config file
        return {'isAdmin': True}
    return {'isAdmin': False}

@jwt.token_in_blacklist_loader
def check_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'Token expired',
        'error': 'token_expired'
    }), 401
    
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Invalid token',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Unauthorized Loader',
        'error': 'unauthorized_loader'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_refreshed_callback():
    return jsonify({
        'description': 'Needs Fresh Token Loader',
        'error': 'needs_fresh_token_loader'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'Your token is Revoked',
        'error': 'revoked_token_loader'
    }), 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    print("MAIN CALLED")
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
