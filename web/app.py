from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_restful import Api, Resource
import json
from multibox import fit_to_boxes, Package

app = Flask(__name__, template_folder='./static')
api = Api(app)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
from models import Box


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)


def to_Package(items):
    """
    This functoin is meant to turn a list of dictionaries into a list of package objects
    input
        items : [{'length': <val>, 'width': <val>, 'height': <val>, 'amount': <val>}, ...]
    output
        [pkg, pkg, ...]
    """
    result = []
    for item in items:
        s_item = "{}x{}x{}".format(item['length'], item['width'], item['height'], item['amount'])
        p_item = Package(s_item)
        result.extend([p_item] * item['amount'])
    return result


class fit_boxes(Resource):
    def post(self):
        # items is a list of 2 things, [0] is the list of things to be boxed [1] is the boxes to be used
        items = request.get_json(force=True)

        # a list of Pacakge() objects
        package_items = to_Package(items[0])
        db_boxes = Box.query.all()
        boxes = {}
        owned = items[1]['owned']
        not_owned = items[1]['not_owned']
        # one or both conditions must be true which makes this decision tree easier
        if owned and not_owned:
            # use all boxes
            for box in db_boxes:
                boxes[box.box_name] = Package((box.box_length, box.box_width, box.box_height))

        elif owned:
            # if owned is true then not_owned is false
            # therefor only use owned boxes
            for box in db_boxes:
                if box.box_tags.intersection({'owned'}) == {'owned'}:
                    boxes[box.box_name] = Package((box.box_length, box.box_width, box.box_height))

        else:
            # not_owned must be true and owned must be false
            # therefor only use not owned boxes
            for box in db_boxes:
                if box.box_tags.intersection({'owned'}) != {'owned'}:
                    boxes[box.box_name] = Package((box.box_length, box.box_width, box.box_height))

        # do the calculation
        # input is a list of packages to be boxed, and a dictionary {name: package_object} of possible boxes to be used
        result = fit_to_boxes(package_items, boxes)

        return result


class get_all_boxes(Resource):
    def get(self):
        items = Box.query.all()
        a = []
        for item in items:
            a.append(item.serialize())
        return {'length': len(a), 'items': a}


class get_box_by_tags(Resource):
    def get(self):
        boxes = Box.query.all()
        user_tags = set(request.args.get('box_tags').split(','))
        return [box.serialize()
                for box in boxes
                if box.box_tags.intersection(user_tags) == user_tags]


class get_box_by_size(Resource):
    def get(self):

        sizes = map(int, request.args.get('size').split(','))
        if len(sizes) == 1:
            boxes = Box.query.filter((Box.box_length == sizes[0]) |
                                     (Box.box_width == sizes[0]) |
                                     (Box.box_height == sizes[0]))
        elif len(sizes) == 2:
            # very ugly dont know if i can do better
            boxes = Box.query.filter(
                ((Box.box_length == sizes[0]) & (Box.box_width == sizes[1])) |
                ((Box.box_length == sizes[1]) & (Box.box_width == sizes[0])) |
                ((Box.box_length == sizes[0]) & (Box.box_height == sizes[1])) |
                ((Box.box_length == sizes[1]) & (Box.box_height == sizes[0])) |
                ((Box.box_width == sizes[0]) & (Box.box_height == sizes[1])) |
                ((Box.box_width == sizes[1]) & (Box.box_height == sizes[0])))
        elif len(sizes) == 3:
            boxes = Box.query.filter(
                ((Box.box_length == sizes[0]) & (Box.box_width == sizes[1]) & (Box.box_height == sizes[2])) |
                ((Box.box_length == sizes[0]) & (Box.box_width == sizes[2]) & (Box.box_height == sizes[1])) |
                ((Box.box_length == sizes[1]) & (Box.box_width == sizes[2]) & (Box.box_height == sizes[0])) |
                ((Box.box_length == sizes[1]) & (Box.box_width == sizes[0]) & (Box.box_height == sizes[2])) |
                ((Box.box_length == sizes[2]) & (Box.box_width == sizes[1]) & (Box.box_height == sizes[0])) |
                ((Box.box_length == sizes[2]) & (Box.box_width == sizes[0]) & (Box.box_height == sizes[1])))
        else:
            return "invalid input"
        return [box.serialize() for box in boxes]

api.add_resource(fit_boxes, '/api/fit_boxes')
api.add_resource(get_all_boxes, '/api/boxes')
api.add_resource(get_box_by_tags, '/api/boxes/tags')
api.add_resource(get_box_by_size, '/api/boxes/size')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
