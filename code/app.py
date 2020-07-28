from datetime import datetime as dt

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from account import AccountRegister
from reservation import Reservation, ReservationList

app = Flask(__name__)
app.secret_key = "change_this_later_bro"
api = Api(app=app)

jwt = JWT(app=app, authentication_handler=authenticate,
          identity_handler=identity)

cinema = {
    "cinemas": [
        {"name": "SM City Calamba Cinema"},
        {"name": "SM City San Pablo Cinema"}
    ]
}

reservations = [
    {
        "id": 99,
        "size": 5,
        "reserve_time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cancel_time": None,
        "account_id": 0,  # <= Modify Later
        "movie_screen_id": 3,  # <= Modify Later
    }
]

reservation_routes = [
    "/reservation/create",
    "/reservation/update",
    "/reservation/<int:id_>",
    "/reservation/cancel"
]

reservation_list_routes = ["/reservations"]

api.add_resource(Reservation, *reservation_routes)
api.add_resource(ReservationList, *reservation_list_routes)
api.add_resource(AccountRegister, "/register")

app.run(port=5000, debug=True)
