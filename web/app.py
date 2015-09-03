,from flask import Flask
from flask import request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from config import BaseConfig
from package import Package
from binpack import binpack

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=['GET', 'POST'])
def Boxing():
    b1 = Package("5x5x5")
    b2 = Package("6x6x6")
    context = {'merch':[b1,b2]}
    if request.method == 'POST':
        #TODO validate size of box submited by user
        #should be no larger than the largest box in db
        m = Package(request.form['x'],request.form['y'],request.form['z'])
        context['merch'].append(m)

    return render_template('index.html',context=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)
