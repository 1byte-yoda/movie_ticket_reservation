from datetime import datetime

from db import db
from .account import AccountModel
from .payment import PaymentModel
from .customized_queries.reservation import SELECT_TICKET_QUERY


TICKET_COLUMNS = [
    "ticket_id",
    "cinema_name",
    "screen_id",
    "movie_name",
    "play_datetime",
    "end_datetime",
    "price_breakdown",
    "total_price",
]


class ReservationModel(db.Model):
    """Docstring Here."""

    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
    head_count = db.Column(db.Integer)
    reserve_datetime = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship(AccountModel, backref="account", lazy=True)
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    payment = db.relationship(PaymentModel, backref="payment", lazy=True, uselist=False)

    def __init__(self, head_count, account, payment, reserve_datetime=None, id=None):
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
        ticket = (
            self.query.from_statement(
                db.text(SELECT_TICKET_QUERY).params(res_id=self.id)
            )
            .with_entities(*TICKET_COLUMNS)
            .first()
        )
        ticket_dict = dict(zip(TICKET_COLUMNS, ticket))
        ticket_dict["price_breakdown"] = ticket_dict["price_breakdown"].decode()
        return ticket_dict
