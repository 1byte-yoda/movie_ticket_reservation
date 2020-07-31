from flask_restful.reqparse import RequestParser


class SeatReservationParser:
    """Input parser for seat reservation."""

    @classmethod
    def parse_reservation_input(cls, *, dict_: dict) -> RequestParser:
        """Parse those input that is needed to create a reservation."""
        parser = RequestParser()
        for name, type_ in dict_.items():
            parser.add_argument(name=name, type=type_, required=True)
        return parser.parse_args()
