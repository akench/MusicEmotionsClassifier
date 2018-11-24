import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from scipy.io import wavfile
import os.path as path
import io
from PIL import Image
import librosa
import librosa.display
import numpy as np
import io
from multiprocessing import Pool
import random

almost_zero = 0.001

def split_list_by_num_samples(data, num_samples):
    """
    converts a flat list of audio data to many groups of audio data, so each can be turned into a spectrogram

    Args:
        data (list): audio samples
        num_samples (int): number of samples to have per list

    Returns:
        list of lists: containing the split data
    """

    new = []
    index = 0
    while index + num_samples < len(data):
        new.append(data[index : index + num_samples])
        index += num_samples

    return new


def audio_sample_to_img(sample, rate, secs_per_spec):
    '''
    Converts the audio sample to a spectrogram image

    Args:
        sample (list) : samples taken from audio
        rate (int): sample rate of audio

    Returns:
        PIL Image of spectrogram
    '''

    S = librosa.feature.melspectrogram(sample, sr=rate, n_mels=128)
    log_S = librosa.amplitude_to_db(S)

    plt.figure(figsize=(secs_per_spec, 7))

    librosa.display.specshow(log_S, sr=rate, x_axis='time', y_axis='mel')

    plt.tight_layout()
    plt.axis('off')
    plt.gray()
    plt.draw()

    # save plot into buffer
    buf = io.BytesIO()
    plt.savefig(buf, bbox_inches='tight', pad_inches = 0, dpi=50, format='jpg')

    # open the image from the buffer and crop it to get the important parts
    buf.seek(0)
    img = Image.open(buf)
    img = img.crop((120, 4, img.size[0] - 3, img.size[1] - 20))

    # close everything
    buf.close()
    plt.clf()
    plt.cla()
    plt.close()

    return img


def graph_spectrogram(audio_file):
    """
    creates spectrograms using librosa library, given the audio file path and the number of seconds to have per spectrogram

    Args:
        audio_file (str): file path to the audio file which should be converted to spectrograms

    Returns:
        will return the list of spectrogram image objects, otherwise no return
    """
    secs_per_spec = 10
    data, rate = librosa.core.load(audio_file)
    split_data = split_list_by_num_samples(data, rate * secs_per_spec)

    random.shuffle(split_data)

    # if songs longer than 100 seconds, take the first 10 images, since its shuffled
    if len(split_data) > 10:
        split_data = split_data[:10]

    pool = Pool()
    results = [pool.apply_async(audio_sample_to_img, args=(sample, rate, secs_per_spec)) for sample in split_data]
    specs = [p.get() for p in results]

    return specs




