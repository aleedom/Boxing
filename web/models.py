# models.py


import datetime
from app import db


class Box(db.Model):

    __tablename__ = 'Boxes'

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    z = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    def __init__(self, x=1,y=1,z=1):
        self.x = x
        self.y = y
        self.z = z
        self.volume = x*y*z
