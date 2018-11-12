from flask import render_template, Blueprint, request, abort, redirect, url_for, session, flash
import json
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

from app.classification import classify_emotion


mod = Blueprint('routes', __name__)

conn = pymysql.connect(
    host="localhost",
    user="testuser",
    password="password",
    db="musicemotions"
)

cur = conn.cursor(pymysql.cursors.DictCursor)

# classify url route
@mod.route('/classify', methods=['POST'])
def classify():
    url = request.json['url']
    emot = classify_emotion(url)

    return json.dumps(emot)


# register route
@mod.route('/register', methods=['POST'])
def register():

    email = request.form['email']
    password = request.form['password']

    hashed_pw = generate_password_hash(password)

    query = "INSERT INTO users VALUES('%s', '%s');" % (email, hashed_pw)

    try:
        cur.execute(query)
        conn.commit()
    except pymysql.IntegrityError as err:
        # pylint: disable=unbalanced-tuple-unpacking
        code, msg = err.args

        print("register err code: %s: %s" % (code, msg))

        # email address already exists
        if code == 1062:
            flash('Invalid email address; A user with that email address already exists', 'error')
            return redirect(url_for('pages.home_page'))

    flash('You have successfully registered. Please login.', 'success')
    return redirect(url_for('pages.home_page'))



# login route
@mod.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    query = "SELECT * FROM users where email='%s';" % email

    try:
        cur.execute(query)
        row = cur.fetchone()

        # user not found
        if row is None or len(row) == 0:
            flash('User not found.', 'error')
            return redirect(url_for('pages.home_page'))

        elif check_password_hash(row['password'], password):
            # login successful
            session['user'] = email
            return redirect(url_for('pages.dashboard_page'))
        else:
            # wrong password
            flash('Invalid password...', 'error')
            return redirect(url_for('pages.home_page'))
    
    except pymysql.IntegrityError as err:
        # pylint: disable=unbalanced-tuple-unpacking
        code, msg = err.args

        print("login err code %s: %s" % (code, msg))
        flash('Unknown error. Please try again later', 'error')
        return redirect(url_for('pages.home_page'))


        
@mod.route('/logout', methods=['GET'])
def logout():

    session.pop('user')

    flash('You have been logged out', 'success')
    return redirect(url_for('pages.home_page'))