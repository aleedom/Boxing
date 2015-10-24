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


class Box_item(Resource):
    def post(self):
        items = request.get_json(force=True)
        # items is a list of dictionaries need to convert to
        # a list of Pacakge() objects
        package_items = to_Package(items)

        # do the calculation
        result = fit_to_boxes(package_items)

        return result


class GET_Boxes(Resource):
    def get(self):
        items = Box.query.all()
        a = []
        for item in items:
            a.append(item.serialize())
        return len(a), a

api.add_resource(Box_item, '/api/box_order')
api.add_resource(GET_Boxes, '/api/boxes')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
