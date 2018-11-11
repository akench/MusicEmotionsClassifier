from flask import render_template, Blueprint, session, redirect, url_for, flash

mod = Blueprint('pages', __name__)

@mod.route('/', methods=['GET'])
def home_page():
    # if user logged in, go to dashboard, otherwise go to login page
    if 'user' in session:
        return redirect(url_for('pages.dashboard_page'))
    else:
        return render_template('home.html')


@mod.route('/about', methods=['GET'])
def about_page():
    # render the about page
    return render_template('about.html')


@mod.route('/dashboard', methods=['GET'])
def dashboard_page():
    # if the user's session exists, render the dashboard
    if 'user' in session:
        flash("Successfully logged in!", "success")
        return render_template('dashboard.html')
    # otherwise redirect to the login page and flash an error
    else:
        flash("Access unauthorized. Please login first.", "error")
        return redirect(url_for('pages.home_page'))

