from flask import render_template, Blueprint, request, abort, redirect, url_for, session, flash
import json
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Thread
import os
from app.views.db_manager import insert_user, get_password_for_user

from app.classification import classify_emotion


mod = Blueprint('routes', __name__)

# cur = conn.cursor(pymysql.cursors.DictCursor)

# classify url route
@mod.route('/songs', methods=['GET', 'POST'])
def classify():

    if request.method == 'POST':
        url = request.json['url']
        email = session.get('user', None)

        thread = Thread(target=classify_emotion, args=(url, email))
        thread.start()

        return "success"


# register route
@mod.route('/register', methods=['POST'])
def register():

    email = request.form['email']
    password = request.form['password']
    hashed_pw = generate_password_hash(password)

    # attempt to insert this new user into the database
    err_code = insert_user(email, hashed_pw)

    if err_code == 0:
        flash('You have successfully registered. Please login.', 'success')
    elif err_code == 1062:
        flash('Invalid email address; A user with that email address already exists', 'error')
    else:
        flash('Unknown Error, please try again later')

    return redirect(url_for('pages.home_page'))


# login route
@mod.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # get password for this user, if user exists
    saved_password, errno = get_password_for_user(email)

    if errno != 0:
        # if there was an error
        flash('Unknown error. Error code %d' % errno, 'error')
        return redirect(url_for('pages.home_page'))

    if saved_password is None:
        flash('User not found', 'error')
        return redirect(url_for('pages.home_page'))

    elif check_password_hash(saved_password, password):
        # login successful
        session['user'] = email
        return redirect(url_for('pages.dashboard_page'))

    else:
        # wrong password
        flash('Password is incorrect', 'error')
        return redirect(url_for('pages.home_page'))

        
@mod.route('/logout', methods=['GET'])
def logout():

    if 'user' in session:
        session.pop('user')

    flash('You have been logged out', 'success')
    return redirect(url_for('pages.home_page'))