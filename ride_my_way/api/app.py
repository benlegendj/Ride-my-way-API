from flask import Flask, request, jsonify
from api.models import RideMyWay

app = Flask(__name__)
ride_my_way = RideMyWay()


@app.route('/')
def hello_world():
    return jsonify({'it worked': ' use 127.0.0.1:5000/rides to get,post,edit or delete rides'})


@app.route('/api/v1/rides', methods=['POST'])
def register():
    user_input = request.get_json(force=True)
    data = {
        'ride_id': len(ride_my_way.rides_list) + 1,
        'starting_point': user_input.get('starting_point'),
        'destination': user_input.get('destination'),
        'date': user_input.get('date'),
        'time': user_input.get('time'),

    }
    if ride_my_way.create_ride_validation(data):
        ride_my_way.add_rides(data)
        response = jsonify({
            'ride_id': data['ride_id'],
            'destination': data['destination'],
            'starting_point': data['starting_point'],
            'date': data['date'],
            'time': data['time']
        })
        response.status_code = 201
        return response
    else:
        response= jsonify({"message": "Please enter correct ride details"})
        return response,400


@app.route('/api/v1/rides', methods=['GET'])
def get_all_rides():
    return jsonify(ride_my_way.rides_list), 200


@app.route('/api/v1/rides/<int:id>', methods=['GET'])
def get_ride_by_id(id):
    '''function to get a single ride'''
    offer = [ride for ride in ride_my_way.rides_list if ride['ride_id'] == id]
    if len(offer) == 0:
        return jsonify({'message': "Ride Doesnt Exist"})
    return jsonify({"ride": offer[0]})


@app.route('/api/v1/rides/<int:ride_id>', methods=['DELETE'])
def delete_book(ride_id):
    '''function to delete rides'''
    offer = [ride for ride in ride_my_way.rides_list if ride['ride_id'] == ride_id]
    if len(offer) == 0:
        return jsonify({'message': "Ride Doesnt Exist"})
    ride_my_way.rides_list.remove(offer[0])
    return jsonify({'message': "Ride Was Deleted Successfully"})


@app.route('/api/v1/request')
def request_a_ride():
    ...


@app.route('/api/v1/rides', methods=['PUT'])
def edit_a_ride():
    ...


if __name__ == '__main__':
    app.run()
