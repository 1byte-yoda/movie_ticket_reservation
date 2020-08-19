from datetime import datetime
import os

from sqlalchemy.types import CHAR, FLOAT
import stripe

from db import db
from .account import AccountModel
from .customized_queries.reservation import SELECT_TICKET_QUERY


CURRENCY = "usd"


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
    head_count = db.Column(db.Integer, nullable=False)
    reserve_datetime = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account = db.relationship(AccountModel, backref="account", lazy=True)
    status = db.Column(CHAR(16), nullable=False, default="failed")
    token = db.Column(db.String(128), nullable=False)
    total_price = db.Column(FLOAT(7, 2), nullable=False)

    def __init__(self, head_count, account, total_price, token):
        self.head_count = head_count
        self.account = account
        self.total_price = total_price
        self.token = token

    def save_to_db(self):
        """Docstring here."""
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "head_count": self.head_count,
            "reserve_datetime": self.reserve_datetime,
            "account": self.account.json()
        }

    def set_status(self, status: str):
        self.status = status

    def charge_with_stripe(self, item_details: dict, token: str) -> stripe.Charge:
        stripe.api_key = os.environ.get("STRIPE_API_KEY")
        line_times = [{
            "price_data": {
                "currency": CURRENCY,
                "product_data": item_details,
                "unit_amount": price,
            },
            "quantity": head_count
        }]
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_times=line_times,
            source=token,
            success_url="",
            cancel_url=""
        )

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
