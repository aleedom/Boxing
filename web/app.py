from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_restful import Api, Resource
import json

from multibox import fit_to_boxes, Package


app = Flask(__name__, template_folder='./static')
app.config.from_object(BaseConfig)
api = Api(app)
db = SQLAlchemy(app)
db.track_modifications = True
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


class box_item(Resource):
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


class get_box(Resource):
    def get(self):
        boxes = Box.query.all()
        user_tags = request.args.get('tags').split(',')

        a = []
        for i in user_tags:
            a.append(i)
        user_tags = set(a)
        a = []
        for box in boxes:
            if box.tags.intersection(user_tags) == user_tags:
                a.append(box.serialize())
        return a

api.add_resource(box_item, '/api/box_order')
api.add_resource(get_all_boxes, '/api/boxes')
api.add_resource(get_box, '/api/box/tags')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
