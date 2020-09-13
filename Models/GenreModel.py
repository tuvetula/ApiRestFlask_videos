import datetime
from config import db , ma

class Genre(db.Model):

    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), index=True)

class GenreSchema(ma.SQLAlchemySchema):

    class Meta:

        model = Genre

        sqla_session = db.session
