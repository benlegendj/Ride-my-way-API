from flask import jsonify, Blueprint, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token
)

from cerberus import Validator
import datetime
from flask import jsonify


class RideMyWay(object):

    def __init__(self):
        '''creating a list containing dictionaries to act as a database'''
        self.users_counter = 0
        self.rides_list = []
        self.requests_list = []

    def add_rides(self, data):
        self.rides_list.append(data)
        return jsonify({'message': 'Ride Added'})

    def view_rides(self):
        return jsonify(self.rides_list)

    def request_rides(self, data):
        self.requests_list.append(data)
        response = jsonify({'message': "You have requested this ride"})
        return response

    def create_ride_validation(self, dict_data):
        '''ride details validation function'''
        schema = {
            'starting_point': {
                'type': 'string',
                'required': True,
                'empty': False,
                'maxlength': 25,
                'minlength': 4},
            'destination': {
                'type': 'string',
                'required': True,
                'empty': False,
                'maxlength': 25,
                'minlength': 4}}
        v = Validator(schema)
        v.allow_unknown = True
        return v.validate(dict_data)

    def date_validate(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
            return True
        except BaseException:
            return False

    def time_validate(self, time_text):
        timeformat = "%H:%M:%S"
        try:
            datetime.datetime.strptime(time_text, timeformat)
            return True
        except BaseException:
            return False

    def user_data_validation(self, dict_data):
        '''user data validation method'''
        schema = {
            'name': {
                'type': 'string',
                'required': True,
                'empty': False,
                'maxlength': 20,
                'minlength': 4},
            'email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            'password': {
                'type': 'string',
                'required': True,
                'maxlength': 16,
                'minlength': 6}}
        v = Validator(schema)
        v.allow_unknown = True
        return v.validate(dict_data)

    def check_email_exists(self, search_email):
        '''check for email existence'''
        for find_email in self.users_list:
            if find_email['email'] == search_email:
                return True
        return False

    def check_email_for_login(self, search_email):
        '''this checks the list and returns the email or false'''
        for find_email in self.users_list:
            if find_email['email'] == search_email:
                return find_email
        return False

    def user_registration(self, data):
        data['password'] = generate_password_hash(data['password'])
        self.users_list.append(data)
        return jsonify({'message': 'Registered Successfully'})

    def user_login(self, data):
        if not self.check_email_exists(data['email']):
            return jsonify({'message': 'Email does not exist'})
        get_email_for_login = self.check_email_for_login(data['email'])
        if check_password_hash(
                get_email_for_login['password'],
                data['password']):
            access_token = create_access_token(identity=data['email'])
            return jsonify(access_token=access_token)
        else:
            return jsonify({'message': 'Wrong Credentials'})

    def view_users(self):
        return jsonify(self.users_list)

