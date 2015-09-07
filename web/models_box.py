from app import db
from sqlalchemy.dialects.postgresql import JSON

class Box(db.Model):
    __tablename__ = 'boxes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tag = db.Column(db.String)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    z = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,name,tag,available=False,x=1,y=1,z=1):
        self.name = name
        self.tag = tag
        self.x = x
        self.y = y
        self.z = z
        self.volumne = x*y*z
        self.available = available

    #def __repr__(self):
    #    return '<id {0} : {1}-{2}-{6} {3}x{4}x{5}>'.format(self.id,self.name, self.tag, self.x, self.y, self.z, self.available)
