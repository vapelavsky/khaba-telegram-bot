from db.core import db
from db.models.base import TimedBaseModel
from .photos import Photos
from .user import User


class Event(TimedBaseModel):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    event_name = db.Column(db.String(50))

    user = db.Column(db.Integer, nullable=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._photo = set()

    @property
    async def photo(self):
        image = await Photos.select('photo_path').where(Photos.parent_id == self.id).gino.all()
        return [image[i].photo_path for i in range(len(image))]
