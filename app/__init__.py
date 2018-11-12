from flask import Flask, render_template, url_for, session
from app.views import routes, pages
from flask_cors import CORS, cross_origin
from datetime import timedelta
import multiprocessing as mp

# initialize the flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfghjkl;lkjhgfdsasrtyuiknbvcxdtyuiop[wrgKJUYjK'

cors = CORS(app)

# register blueprints with app
app.register_blueprint(pages.mod)
app.register_blueprint(routes.mod)


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    session.modified = True
