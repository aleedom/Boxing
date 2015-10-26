from app import db
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY

modmethods = ['add', 'clear', 'difference_update', 'discard',
              'intersection_update', 'pop', 'remove',
              'symmetric_difference_update', 'update',
              '__ior__', '__iand__', '__isub__', '__ixor__']


class MutableSet(Mutable, set):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, cls):
            return cls(value)
        else:
            return value

    def to_JSON(self):
        return list[self]


def _make_mm(mmname):
    def mm(self, *args, **kwargs):
        try:
            retval = getattr(set, mmname)(self, *args, **kwargs)
        finally:
            self.changed()
        return retval
    return mm

for m in modmethods:
    setattr(MutableSet, m, _make_mm(m))

del modmethods, _make_mm


def ArraySet(_type, dimensions=1):
    return MutableSet.as_mutable(ARRAY(_type, dimensions=dimensions))


class Box(db.Model):
    __tablename__ = 'Boxes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    tags = db.Column(ArraySet(db.String))
    length = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tags, length=1, width=1, height=1):
        self.name = name
        self.tags = tags
        self.length = length
        self.width = width
        self.height = height

    def serialize(self):
        return {
            'id':       self.id,
            'name':     self.name,
            'tags':     list(self.tags),
            'length':   self.length,
            'width':    self.width,
            'height':   self.height
        }
