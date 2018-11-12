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

    perc = percentify(label_list)
    return perc


def predict_class(youtube_link):

    t0 = time.time()

    print("SASASASASAS", youtube_link)

    try:
        dl_audio_path = dl_audio(youtube_link, None)
    except:
        return None


    specs_imgs = graph_spectrogram(dl_audio_path, save = False)
    os.remove(dl_audio_path)

    random.shuffle(specs_imgs)

    specs_imgs = specs_imgs[: int(len(specs_imgs) / 2)]

    perc = get_conf_per_class(specs_imgs)
    print(perc)
    print('took %f seconds to predict.' % (time.time() - t0))

    return np.argmax(perc)


def classify_emotion(url):
    emot = label_to_emot[predict_class(url)]

    print('song is emot:', emot)
    # todo add to db


if __name__=='__main__':
    print(classify_emotion('https://www.youtube.com/watch?v=mF3DCa4TbD0'))