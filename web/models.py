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
    box_id = db.Column(db.Integer, primary_key=True)
    box_name = db.Column(db.String, nullable=False, unique=True)
    box_tags = db.Column(ArraySet(db.String))
    box_length = db.Column(db.Integer, nullable=False)
    box_width = db.Column(db.Integer, nullable=False)
    box_height = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tags, length=1, width=1, height=1):
        self.box_name = name
        self.box_tags = tags
        self.box_length = length
        self.box_width = width
        self.box_height = height

    def serialize(self):
        return {
            'id':       self.box_id,
            'name':     self.box_name,
            'tags':     list(self.box_tags),
            'length':   self.box_length,
            'width':    self.box_width,
            'height':   self.box_height
        }


class Customer(db.Model):
    customer_id = db.Column(db.String, primary_key=True)
    customer_firstname = db.Column(db.String, nullable=False, unique=False)
    customer_lastname = db.Column(db.String, nullable=False, unique=False)
    customer_email = db.Column(db.String, nullable=False, unique=True)
    customer_orders = db.relationship('Order', backref='Customer', lazy='dynamic')

    def __init__(self, id, firstname, lastname, email):
        self.customer_id = id
        self.customer_firstname = firstname
        self.customer_lastname = lastname
        self.customer_email = email

    def serialize(self):
        return {
            'id':       self.customer_id,
            'first_name':     self.customer_firstname,
            'last_name':    self.customer_lastname,
            'email':   self.customer_email,
            'orders':   [o.order_id for o in self.customer_orders]
        }


class Merchandise(db.Model):
    merchandise_id = db.Column(db.String, primary_key=True)
    merchandise_name = db.Column(db.String, nullable=False)
    merchandise_price = db.Column(db.Float)
    merchandise_length = db.Column(db.Integer, nullable=True)
    merchandise_width = db.Column(db.Integer, nullable=True)
    merchandise_height = db.Column(db.Integer, nullable=True)

    def __init__(self, id, name, price, x, y, z):
        self.merchandise_id = id
        self.merchandise_name = name
        self.merchandise_price = price
        self.merchandise_length = x
        self.merchandise_width = y
        self.merchandise_height = z

    def serialize(self):
        return {
            'id':       self.merchandise_id,
            'name':     self.merchandise_name,
            'price':    self.merchandise_price,
            'length':   self.merchandise_length,
            'width':    self.merchandise_width,
            'height':   self.merchandise_height
        }

boxes = db.Table('boxes',
                 db.Column('box_id', db.Integer, db.ForeignKey('box.box_id')),
                 db.Column('order_id', db.Integer, db.ForeignKey('order.order_id'))
                 )
merch = db.Table('merch',
                 db.Column('merchandise_id', db.String, db.ForeignKey('merchandise.merchandise_id')),
                 db.Column('order_id', db.Integer, db.ForeignKey('order.order_id'))
                 )


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_customerid = db.Column(db.String, db.ForeignKey('customer.customer_id'))
    order_boxes = db.relationship('Box', secondary=boxes, backref=db.backref('boxes', lazy='dynamic'))
    order_merchandise = db.relationship('Merchandise', secondary=merch, backref=db.backref('merch', lazy='dynamic'))
    order_date = db.Column(db.DateTime)

    def serialize(self):
        return {
            'id':           self.order_id,
            'customer_id':  self.order_customerid,
            'boxes':        [b.box_name for b in self.order_boxes],
            'merchandise':  [m.merchandise_name for m in self.order_merchandise],
            'date':         self.order_date.isoformat(),
        }
