import unittest
from api.app import app
import json
from api.models import RideMyWay


class TestAuth(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.ride = {
            "starting_point": "nairobi",
            "destination": "kiambu",
            "date": "12/02/2018",
            "time": "10:00"
        }
        self.empty_ride = {
            "ride_id": "",
            "starting_point": "",
            "destination": "kiambu",
            "date": "12/02/2018",
            "time": "10:00"
        }

    def test_rides_can_register(self):
        response = self.app.post('/api/v1/rides', data=json.dumps(self.ride),
                                 content_type="application/json")
        self.assertIn("1", str(response.data))
        self.assertIn("kiambu", str(response.data))
        self.assertIn("nairobi", str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_rides_cannot_be_blank(self):
        """test api cannot register rides with blank fields"""
        response = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.empty_ride),
                                 content_type="application/json")

        self.assertEqual(response, {'message': 'Please enter correct ride details'})
        self.assertEqual(response.status_code, 400)

    def test_get_all_rides(self):
        '''test api can get all available rides (GET request)'''
        post_result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride))
        self.assertEqual(post_result.status_code, 201)
        result = self.app.get('/api/v1/rides')
        self.assertEqual(result.status_code, 200)

    def test_ride_get_by_id(self):
        '''test api can get a single ride by its id (GET request)'''
        post_result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride))
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        result = self.app.get(
            '/api/v1/rides/{}'.format(json_result['ride_id']),
            content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_rides_can_be_edited(self):
        """test api can edit a ride (PUT request)"""
        self.app.post('/api/v1/rides/', data=json.dumps(self.ride),
                      content_type='application/json')
        self.ride['destination'] = 'new_destination'
        response = self.app.put(
            '/api/v1/rides/ride1',
            data=json.dumps(
                self.ride),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_a_ride(self):
        """test api can delete a single ride by id"""
        post_result = self.app.post(
            '/api/v1/rides', data=json.dumps(self.ride))
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.app.delete('/api/v1/rides/1')
        self.assertEqual(delete_result.status_code, 200)
        response = self.app.get('/api/v1/rides/1')
        self.assertIn('Ride Doesnt Exist', str(response.data))

    def test_delete_non_existing_ride(self):
        """test api can delete a single ride by id"""
        delete_result = self.app.delete('/api/v1/rides/1')
        self.assertEqual(delete_result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
