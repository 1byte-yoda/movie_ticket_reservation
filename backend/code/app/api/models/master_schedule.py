# from datetime import datetime

# from db import db


# class MasterScheduleModel(db.Model):
#     """Docstring here."""

#     __tablename__ = "master_schedule"

#     id = db.Column(db.Integer, primary_key=True)
#     launch_date = db.Column(db.Date, nullable=False)
#     phase_out_date = db.Column(db.Date, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now)
#     updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

#     def __init__(self, launch_date, phase_out_date):
#         self.launch_date = launch_date
#         self.phase_out_date = phase_out_date

#     def json(self):
#         return {
#             "launch_date": self.launch_date,
#             "phase_out_date": self.phase_out_date
#         }

#     @classmethod
#     def find_by_id(cls, id: int) -> "MasterScheduleModel":
#         """Find a master schedule in the database by id."""
#         return cls.query.filter_by(id=id).first()

#     @classmethod
#     def find_by_dates(cls, dates: dict) -> "MasterScheduleModel":
#         return cls.query.filter_by(**dates).first()

#     def save_to_db(self):
#         """Save a new master schedule in the database."""
#         db.session.add(self)
#         db.session.commit()

#     def update(self, update_data: dict):
#         """Update a master schedule in the database."""
#         (db.session.query(MasterScheduleModel)
#                    .filter_by(id=self.id)
#                    .update(update_data))

#     def remove_from_db(self):
#         """Remove a master schedule from the database."""
#         db.session.delete(self)
#         db.session.commit()
