class Rides:
    def __init__(self,ride_id,starting_point,destination,date,time):
        self.ride_id=ride_id
        self.starting_point=starting_point
        self.destination=destination
        self.date = date
        self.time=time






class User:
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password

class Requests(Rides):
    def __init__(self,requester):
        self.requester=requester




