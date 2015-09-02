from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=['GET', 'POST'])
def hello():
    b = Box.query.all()
    return render_template('index.html',boxes=b)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
