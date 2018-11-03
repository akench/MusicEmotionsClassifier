from flask import render_template, Blueprint, request
import json

from app.classification import classify_emotion


mod = Blueprint('routes', __name__)


@mod.route('/classify', methods=['POST'])
def classify():
    url = request.json['url']

    emot = classify_emotion(url)

    return json.dumps(emot)



@mod.route('/testpage')
def test():
    return render_template('test.html')


@mod.route('/testjson', methods=['GET'])
def testjson():
    return json.dumps('hihihi')