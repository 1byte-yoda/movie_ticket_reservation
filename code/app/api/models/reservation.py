from datetime import datetime

from db import db
from .account import AccountModel
from .payment import PaymentModel
from .movie_screen import MovieScreenModel


class ReservationModel(db.Model):
    """Docstring Here."""

    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    head_count = db.Column(db.Integer)
    reserve_datetime = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship(AccountModel, backref="account", lazy=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    payment = db.relationship(PaymentModel, backref="payment", lazy=True,
                              uselist=False)

    def __init__(self, head_count, account, payment,
                 reserve_datetime=None, id=None):
        self.id = id
        self.head_count = head_count
        self.reserve_datetime = reserve_datetime
        self.account = account
        self.payment = payment

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()

    def generate_json_ticket(self) -> dict:
        """Generate a JSON ticket summary of a reservation."""
        columns = ["ticket_id", "cinema_name", "screen_id", "movie_name",
                   "play_datetime", "end_datetime", "price_breakdown", "total_price"]
        select_ticket = ("SELECT res.id AS 'ticket_id', "
                         "c.name AS 'cinema_name', "
                         "s.id AS 'screen_id', "
                         "m.name AS 'movie_name', "
                         "DATE_FORMAT(sch.play_datetime, '%Y-%m-%d %T') AS 'play_datetime', "
                         "DATE_FORMAT(sch.end_datetime, '%Y-%m-%d %T') AS 'end_datetime', "
                         "CONCAT(COUNT(sr.id), ' x ', sr.price) AS 'price_breakdown', "
                         "p.total_price "
                         "FROM reservation AS res "
                         "JOIN payment p ON p.id = res.payment_id "
                         "JOIN seat_reservation AS sr ON sr.reservation_id = res.id "
                         "JOIN movie_screen AS ms ON ms.id = sr.movie_screen_id "
                         "JOIN movie AS m ON m.id = ms.movie_id "
                         "JOIN screen AS s ON s.id = ms.screen_id "
                         "JOIN schedule AS sch ON sch.id = ms.schedule_id "
                         "JOIN cinema AS c ON c.id = s.cinema_id "
                         "WHERE res.id=:res_id "
                         "GROUP BY sr.`reservation_id`")
        ticket = (self.query.from_statement(db.text(select_ticket).params(res_id=self.id))
                            .with_entities(*columns).first())
        ticket_dict = dict(zip(columns, ticket))
        ticket_dict["price_breakdown"] = ticket_dict["price_breakdown"].decode()
        return ticket_dict
