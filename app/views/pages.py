from flask import render_template, Blueprint

mod = Blueprint('pages', __name__)

@mod.route('/', methods=['GET'])
def home_page():

    return render_template('home.html')


@mod.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')

@mod.route('/dashboard', methods=['GET'])
def dashboard_page():
    return render_template('dashboard.html')