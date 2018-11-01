from flask import render_template, Blueprint


mod = Blueprint('routes', __name__)


@mod.route('/test')
def test():
    return render_template('test.html')