from flask import render_template, Blueprint, request, abort
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

cur = conn.cursor()


@mod.route('/classify', methods=['POST'])
def classify():
    url = request.json['url']

    emot = classify_emotion(url)

    return json.dumps(emot)

@mod.route('/register', methods=['POST'])
def register():

    data = request.json
    email = data['email']
    password = data['password']

    hashed_pw = generate_password_hash(password)

    query = "INSERT INTO users VALUES('%s', '%s');" % (email, hashed_pw)

    try :
        cur.execute(query)
        conn.commit()
    except pymysql.IntegrityError as err:
        code, msg = err.args

        print("register err code: %s" % code)

        # email address already exists
        if code == 1062:
            return "1"

    return "0"



@mod.route('/testpage')
def test():
    return render_template('test.html')


@mod.route('/testjson', methods=['GET'])
def testjson():
    return json.dumps('hihihi')