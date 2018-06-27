from api.app import app
import json
import unittest


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.user_input = {
            'name': 'testuser',
            'email': 'test@mail.com',
            'password': 'pass'
        }

        self.user_logins = {
            'email': 'test@mail.com',
            'password': 'pass'
        }

    def test_registration(self):
        '''sends HTTP GET request to the application'''
        response = self.app.post('/api/v1/auth/register', data=self.user_input)
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            response.data,
            b'{"message": "Registered Successfully"}')

    def test_user_login(self):
        '''test api allows user to login'''
        result = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_logins))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'access_token', result.data)

    def test_user_logout(self):
        '''test api allows user to logout'''
        result = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_logins))
        token = json.loads(result.data)
        access_token = token['access_token']
        response = self.app.post(
            'api/v1/auth/logout',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You are now logged out", response.data)
