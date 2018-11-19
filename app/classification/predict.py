import tensorflow as tf
import os
from app.classification.get_audio import dl_audio
from app.classification.make_spectrogram import graph_spectrogram
from PIL import Image
import numpy as np
from app.classification.parse_img import *
import glob
import numpy as np
import time
import random
import pymysql


label_to_emot = {0:'angry', 1:'happy', 2:'motivational', 3:'relaxing', 4:'sad'}


def load_graph(graph_file_path):

    with tf.gfile.GFile(graph_file_path, 'rb') as f:
        #load the pbfile and get the unserialized graph_Def
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    #import this graph_def into a new graph
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name="inceptionv3")

    return graph


def inference(data, graph):

    # list_of_tuples = [op.values()[0] for op in graph.get_operations()]
    # print(list_of_tuples)

    x = graph.get_tensor_by_name('inceptionv3/Placeholder:0')
    y = graph.get_tensor_by_name('inceptionv3/final_result:0')

    with tf.Session(graph = graph) as sess:
        out = sess.run(y, feed_dict={x: data})
        label_list = sess.run(tf.argmax(tf.squeeze(out)))
        return label_list


def percentify(x):

    perc = (x / np.sum(x))
    return perc

def get_conf_per_class(spec_list):

    # sad 0, happy 1, angry 4
    label_list = [0, 0, 0, 0, 0, 0]
    graph = load_graph('/home/akench/Desktop/output_graph.pb')

    for img in spec_list:

        img = resize_crop(img, size=299, grey = False)
        arr = np.asarray(img)

        lbl = inference([arr], graph)
        label_list[lbl] += 1

    return label_list


def predict_class(youtube_link):

    t0 = time.time()

    start1 = time.clock()
    try:
        dl_audio_path = dl_audio(youtube_link, None)
    except:
        return None

    print("time to download audio: ", time.clock() - start1)


    start2 = time.clock()
    specs_imgs = graph_spectrogram(dl_audio_path, save = False)
    print("time to create imgs: ", time.clock() - start2)


    os.remove(dl_audio_path)

    random.shuffle(specs_imgs)

    specs_imgs = specs_imgs[: int(len(specs_imgs) / 2)]

    start3 = time.clock()
    conf = get_conf_per_class(specs_imgs)
    print("time to feed through model: ", time.clock() - start3)

    print(conf)
    print('took %f seconds to predict.' % (time.time() - t0))

    return np.argmax(perc)


def classify_emotion(url, email, conn):

    class_index = predict_class(url)

    # store embedded url in db
    url = url.replace('watch?v=', 'embed/')

    # TODO work on persist errors using redis and show to user next time
    # if there was some error in the classification, return 
    if not class_index:
        return 

    emot = label_to_emot[class_index]

    print('song is emot:', emot)

    try:
        # get cursor object to execute queries
        cur = conn.cursor(pymysql.cursors.DictCursor)

        # add song and emotion to songemotions table
        query = "INSERT INTO songemotions VALUES('%s', '%s');" % (url, emot)
        cur.execute(query)

        conn.commit()

        # add the song to the usersongs table
        query = "INSERT INTO usersongs VALUES('%s', '%s');" % (email, url)
        cur.execute(query)

        conn.commit()

    except pymysql.IntegrityError as err:
        print("error: ", err.args)

