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
from app.views.db_manager import insert_song, insert_user_song, is_song_in_db


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
    """
    Performs inference on a graph and returns logits for each class

    Args:
        data (nparray): spectrogram image in np array format
        graph: tensorflow loaded graph
    """

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


def get_confidences(spec_list):
    """
    Passes the spectrogram images to model and gets the prediction
    combines the prediction of all spectrogram images to get a list of confidence values

    Args:
        spec_list (list): list of PIL image objects of the spectrograms

    Returns:
        list: label list of the emotion of each spectrogram image, predicted from model
    """

    # sad 0, happy 1, ... angry 4
    label_list = [0, 0, 0, 0, 0, 0]
    graph = load_graph('/home/akench/Desktop/output_graph.pb')

    for img in spec_list:

        img = resize_crop(img, size=299, grey = False)
        arr = np.asarray(img)

        lbl = inference([arr], graph)
        label_list[lbl] += 1

    return label_list


def predict_class(youtube_url):
    """
    Predicts the class of a youtube url by downloading the audio,
    generating spectrogram images of the audio, then feeding it through the model

    Args:
        youtube_url (str): url to predict class of
    
    Returns:
        str: emotion of song
        str: title of youtube video 

    """

    t0 = time.time()

    start1 = time.clock()
    try:
        dl_audio_path, title = dl_audio(youtube_url, None)
    except Exception as err:
        # if there was some error downloading, just return None
        print('download error: {}'.format(err))
        return None

    print("time to download audio: ", time.clock() - start1)


    start2 = time.clock()
    specs_imgs = graph_spectrogram(dl_audio_path, save = False)
    print("time to create imgs: ", time.clock() - start2)

    # remove temporary audio file
    os.remove(dl_audio_path)

    random.shuffle(specs_imgs)

    start3 = time.clock()
    conf = get_confidences(specs_imgs)
    print("time to feed through model: ", time.clock() - start3)

    print(conf)
    print('took %f seconds to predict.' % (time.time() - t0))

    # index of the emotion according to the model
    class_index = np.argmax(conf)
    
    # return the emotion and title
    return label_to_emot[class_index], title


def classify_emotion(url, email):
    """
    Higher level method which classifies the emotion of a song
    then adds the song to the songemotions table
    and then adds the song to the usersongs table

    Args:
        url (str): youtube url of song
        email (str): email address of the user to classify song for
    """

    # use the embedded version of url
    url = url.replace('watch?v=', 'embed/')
    vid_id = extract_vid_id(url)

    # check if song has already been classified
    if is_song_in_db(vid_id):
        print('song already classified')
        # add song to user library
        insert_user_song(email, vid_id)
    else:
        # download and predict the class of the song
        args = predict_class(url)

        # if some error return none
        if args is None or args[0] is None:
            return

        emot, title = args

        # TODO work on persist errors using redis and show to user next time

        # save the songs emotion
        insert_song(vid_id, title, emot)

        # mark this song as part of this user's library
        insert_user_song(email, vid_id)


def extract_vid_id(url):
    ''' 
    Extracts a youtube video id from the url

    Args:
        url (str): youtube url

    Returns:
        str : video id
    '''

    # remove an ending slash, if there is one
    if url[-1] == '/':
        url = url[:-1]

    if 'watch?v=' in url:
        # get the stuff after the watch?v=
        return url.split('watch?v=')[-1]
    elif 'embed/' in url:
        return url.split('embed/')[-1]

    else:
        # if dont know, just take the last 11 characters as the ID
        return url[-11:]
