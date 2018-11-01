from pymongo import MongoClient
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

client = MongoClient('mongodb://localhost:27017/musicemotions')
collection = client.musicemotions.users


@app.route('/register', methods=['POST'])
def register():

    json_data = request.json
    username = json_data['username']
    password = json_data['password']

    if request.method == 'POST':   

        collection.insert({'username' : username, 
            'password': password, 
            'songs': {
                'happy': [],
                'sad': [],
                'angry': [],
                'relaxing': [],
                'motivational': [],
                'tense': []
            }})

        return json.dumps('success')


@cross_origin
@app.route('/login', methods=['POST'])
def login():

    json_data = request.json

    username = json_data['username']
    password = json_data['password']

    for obj in collection.find():
        if obj['username'] == username and obj['password'] == password:
            print('success!!')
            return json.dumps('true')

    print('could not login!')
    return json.dumps('false') 


@cross_origin
@app.route('/classify', methods=['POST'])
def classify_audio():

    #sends username and youtube url
    json_data = request.json
    url = json_data['url']
    username = json_data['username']

    label = predict_class(url)

    if label == None:
        return json.dumps('error')

    emot = label_to_emot[label]

    addUrlToDb(username, emot, url)
    return json.dumps(emot)


@app.route('/getSavedSongs/<username>', methods=['GET'])
def getSavedSongs(username):

    for obj in collection.find():
        if obj['username'] == username:
            return json.dumps(obj['songs'])

    return json.dumps('error')



def addUrlToDb(username, emot, url):

    url = url.replace('watch?v=', 'embed/')

    thing_to_change = 'songs.{}'.format(emot)
    collection.find_one_and_update({'username': username}, {'$push': {thing_to_change: url}})



if __name__ == '__main__':
    app.run(debug = True)
        