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
        items = request.get_json(force=True)
        # items is a list of dictionaries need to convert to
        # a list of Pacakge() objects
        package_items = to_Package(items)

        # do the calculation
        result = fit_to_boxes(package_items)

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
        user_tags = set(request.args.get('tags').split(','))
        return [box.serialize()
                for box in boxes
                if box.tags.intersection(user_tags) == user_tags]


class get_box_by_size(Resource):
    def get(self):

        sizes = map(int, request.args.get('size').split(','))
        if len(sizes) == 1:
            boxes = Box.query.filter((Box.length == sizes[0]) | (Box.width == sizes[0]) | (Box.height == sizes[0]))
        elif len(sizes) == 2:
            # very ugly dont know if i can do better
            boxes = Box.query.filter(
                ((Box.length == sizes[0]) & (Box.width == sizes[1])) |
                ((Box.length == sizes[1]) & (Box.width == sizes[0])) |
                ((Box.length == sizes[0]) & (Box.height == sizes[1])) |
                ((Box.length == sizes[1]) & (Box.height == sizes[0])) |
                ((Box.width == sizes[0]) & (Box.height == sizes[1])) |
                ((Box.width == sizes[1]) & (Box.height == sizes[0])))
        elif len(sizes) == 3:
            boxes = Box.query.filter(
                ((Box.length == sizes[0]) & (Box.width == sizes[1]) & (Box.height == sizes[2])) |
                ((Box.length == sizes[0]) & (Box.width == sizes[2]) & (Box.height == sizes[1])) |
                ((Box.length == sizes[1]) & (Box.width == sizes[2]) & (Box.height == sizes[0])) |
                ((Box.length == sizes[1]) & (Box.width == sizes[0]) & (Box.height == sizes[2])) |
                ((Box.length == sizes[2]) & (Box.width == sizes[1]) & (Box.height == sizes[0])) |
                ((Box.length == sizes[2]) & (Box.width == sizes[0]) & (Box.height == sizes[1])))
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
