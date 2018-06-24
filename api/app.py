from flask import Flask, request, jsonify

app = Flask(__name__)

rides = []


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/v1/rides', methods=['POST'])
def register():
    user_data = request.get_json(force=True)
    ride = {
        "ride_id": user_data.get("ride_id"),
        "starting_point": user_data.get("starting_point"),
        "destination": user_data.get("destination"),
        "date": user_data.get("date"),
        "time": user_data.get("time"),
    }
    rides.append(ride)
    return jsonify({"message": ride}), 201


@app.route('/api/v1/rides/', methods=['GET'])
def get_all_rides():
    for items in rides:
        return jsonify({"message": items})


@app.route('/api/v1/rides/', methods=['DELETE'])
def delete():
    ...


@app.route('/api/v1/request')
def request_a_ride():
    ...


@app.route('/api/v1/rides', methods=['PUT'])
def edit_a_ride():
    ...


if __name__ == '__main__':
    app.run()
