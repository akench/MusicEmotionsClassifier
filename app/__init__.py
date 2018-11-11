from flask import Flask, render_template, url_for, session
from app.views import routes, pages
from flask_cors import CORS, cross_origin

# initialize the flask application
app = Flask(__name__)
app.secret_key = 'ifh0i2pk3[wg[e;fwoqjigw3uqbfaw'

cors = CORS(app)

# register blueprints with app
app.register_blueprint(pages.mod)
app.register_blueprint(routes.mod)