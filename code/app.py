from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.item import Item, Items
from resources.user import UserRegister
from resources.store import Store, Stores
from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "cole"   # This should be hidden / secure in production code
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

# Set Endpoints
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
