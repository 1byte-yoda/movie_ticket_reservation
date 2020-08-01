from app.api.models.seat_reservation import SeatReservationModel
from ...base_test import BaseTest


class SeatReservationTest(BaseTest):
    def test_seat_reservation(self):
        with self.app_context():
            seat_reservation = SeatReservationModel(10, 1, 1, 1)
            seat_reservation.save_to_db()
            query_parameters = {"seat_id": 1, "movie_screen_id": 1, "reservation_id": 1}
            self.assertIsNotNone(SeatReservationModel.find(data=query_parameters))
