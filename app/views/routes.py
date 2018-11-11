from flask import render_template, Blueprint, request, abort, redirect, url_for, session
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

    data = request.json
    email = data['email']
    password = data['password']

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
            return "1"

    return "0"



# login route
@mod.route('/login', methods=['POST'])
def login():

    data = request.json
    email = data['email']
    password = data['password']

    query = "SELECT * FROM users where email='%s';" % email

    try:
        cur.execute(query)
        row = cur.fetchone()

        # user not found
        if row is None or len(row) == 0:
            return "4"

        elif check_password_hash(row['password'], password):
            # login successful
            session['user'] = email
            return "0"
        else:
            # wrong password
            return "3"
    
    except pymysql.IntegrityError as err:
        # pylint: disable=unbalanced-tuple-unpacking
        code, msg = err.args

        print("login err code %s: %s" % (code, msg))

        return "5"

        


