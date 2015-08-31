# app.py


from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x = request.form['dim-x']
        y = request.form['dim-y']
        z = request.form['dim-z']
        box = Box(x,y,z)
        db.session.add(post)
        db.session.commit()
    boxes = Post.query.order_by(Box.volume.desc()).all()
    return render_template('index.html', boxes=boxes)


if __name__ == '__main__':
    app.run()
