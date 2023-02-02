from datetime import datetime

from marshmallow import Schema, fields
from app.database import db


class Place(db.Model):
    __tablename__ = 'place'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    picture_url = db.Column(db.String(250))
    price = db.Column(db.Integer)
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    features_on = db.Column(db.String(100))  # что есть
    features_off = db.Column(db.String(100))  # чего нет
    # date_create = db.Column(db.DateTime, default=datetime.utcnow)


class PlaceSchema(Schema):
    pk = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    picture_url = fields.URL()
    price = fields.Str()
    country = fields.Str()
    city = fields.Str()
    features_on = fields.Str()
    features_off = fields.Str()
    # date_create = fields.Str()
