from flask import Flask, render_template, url_for, session
from app.views import routes
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.secret_key = 'secret123'

cors = CORS(app)


@app.route('/', methods=['GET'])
def home_page():
    return render_template('home-page.html')


app.register_blueprint(routes.mod)