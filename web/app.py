from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_restful import Api, Resource


app = Flask(__name__, template_folder='./static')
app.config.from_object(BaseConfig)
api = Api(app)
db = SQLAlchemy(app)


def volume(item):
    return item['length']*item['width']*item['height']*item['amount']


class Box(Resource):
    def post(self):
        box = request.get_json(force=True)
        total_volume = 0
        for item in box:
            total_volume += volume(item)
        return total_volume

api.add_resource(Box, '/api/box_order')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
