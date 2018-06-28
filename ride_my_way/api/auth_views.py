'''ímport dependancies'''
import datetime
from flask import jsonify, Blueprint, request, Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from ride_my_way import app, jwt
from ride_my_way.api.models import RideMyWay

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''check if token is blacklisted'''
    jti = decrypted_token['jti']
    return jti in blacklist

auth = Blueprint('auth', __name__)
ride_my_way = RideMyWay()


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    '''Function to reset user password'''
    email = request.json.get('email')
    for user in ride_my_way.users_list:
        if email == user['email']:
            user['password'] = generate_password_hash("Pass123")
            return jsonify({
                'message': "Password has been changed to Pass123. Please login and change it."
            }), 201
    return jsonify({'message': 'Email not found.'})

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    '''Fuction to register a new user'''
    try:
        sent_data = request.get_json(force=True)
        data = {
            'user_id': len(ride_my_way.users_list) + 1,
            'name': sent_data['name'],
            'email': sent_data['email'],
            'password': sent_data['password'],
            'is_admin': False
        }
        if ride_my_way.check_email_for_login(data['email']):
            return jsonify({'message': 'Email Exists'})
        else:
            if ride_my_way.user_data_validation(data):
                return ride_my_way.user_registration(data), 201
            else:
                return jsonify(
                    {'message': 'Please enter all the data in the correct format.'})
    except BaseException:
        return jsonify({'message': 'Please enter all the data required'})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    '''Function for logging in'''
    try:
        sent_data = request.get_json(force=True)
        data = {
            'email': sent_data['email'],
            'password': sent_data['password']
        }
        return ride_my_way.user_login(data), 200
    except BaseException:
        return jsonify(
            {'message': 'Please enter your email and password correctly'})

@app.route('/api/v1/auth/logout', methods=['GET', 'POST'])
@jwt_required
def logout():
    '''Function for logout'''
    token_identifier = get_raw_jwt()['jti']
    blacklist.add(token_identifier)
    return jsonify({'message': 'You are now logged out'}), 200

@app.route('/api/v1/auth/change-password', methods=['PUT'])
@jwt_required
def change_password():
    '''Function for changing user password'''
    email = get_jwt_identity()
    new_password = request.json.get('new_password')
    old_password = request.json.get('old_password')
    for user in ride_my_way.users_list:
        if email == user['email']:
            if ride_my_way.password_validation({"password": new_password}):
                if check_password_hash(user['password'], old_password):
                    user['password'] = generate_password_hash(new_password)
                    return jsonify(
                        {'message': "Password has been changed"}), 201
                else:
                    return jsonify({"message": "Old password does not match"})
            else:
                return jsonify(
                    {'message': "Password needs to be 6 characters or more"})
    return jsonify({'message': 'Unable to change password.'})


@app.route('/api/v1/auth/users')
@jwt_required
def view_users():
    '''Function for viewing all users'''
    return ride_my_way.view_users(), 200

