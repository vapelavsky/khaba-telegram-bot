from db.core import db
from db.models.base import TimedBaseModel


class Photos(TimedBaseModel):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    # event = db.Column(db.String(50), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    photo_path = db.Column(db.String(255), nullable=False)
