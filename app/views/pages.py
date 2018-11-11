from flask import render_template, Blueprint, session, redirect, url_for, flash

mod = Blueprint('pages', __name__)

@mod.route('/', methods=['GET'])
def home_page():
    session.modified = True
    return render_template('home.html')


@mod.route('/about', methods=['GET'])
def about_page():
    session.modified = True
    return render_template('about.html')

@mod.route('/dashboard', methods=['GET'])
def dashboard_page():
    session.modified = True
    email = session.get('user', None)

    if email:
        flash("Successfully logged in!", "success")
        return render_template('dashboard.html', email=email)
    else:
        flash("Access unauthorized. Please login first.", "error")
        return redirect(url_for('pages.home_page'))

@mod.route('/testpage')
def test():
    return render_template('test.html')