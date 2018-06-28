'''import dependancies'''
from flask_api import FlaskAPI
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from cerberus import Validator

app = FlaskAPI(__name__)

'''setup jwt for token encryption'''
app.config['JWT_SECRET_KEY'] = 'this is secret'
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

'''import routes'''
from ride_my_way.api.auth_views import auth
from ride_my_way.api.rides_views import rides

'''registering the routes to blueprints'''
app.register_blueprint(auth)
app.register_blueprint(rides)