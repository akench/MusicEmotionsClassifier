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

def get_wav_info(audio_file):
    rate, data = wavfile.read(audio_file)

    if len(data.shape) > 1:
        data = data.sum(axis = 1) / 2
    return rate, data


def graph_spectrogram(audio_file, secs_per_spec = 10, save=True):
    """
    creates spectrograms using librosa library, given the audio file path and the number of seconds to have per spectrogram
    if also saving spectrogram, will save in `gen_specs` folder, otherwise will return the PIL image object

    Args:
        audio_file (str): file path to the audio file which should be converted to spectrograms
        secs_per_spec (int): the number of seconds from the audio file to be displayed in the spectrogram
        save (bool): whether or not to save the spectrogram

    Returns:
        if save is False, will return the list of spectrogram image objects, otherwise no return
    """

    if save:
        vid_id = audio_file.split('/')[-1].split('.')[0]
        emot = audio_file.split('/')[1]

        save_path = 'gen_specs/' + emot + '/' + vid_id

        #if the current .wav has already been converted, skip
        if path.exists(save_path + '_0.jpg') and save:
            print('exists')
            return


    data, rate = librosa.core.load(audio_file)

    split_data = split_list_by_num_samples(data, rate * secs_per_spec)


    name_index = 0
    specs = []

    for mini_data in split_data:

        S = librosa.feature.melspectrogram(mini_data, sr=rate, n_mels=128)
        log_S = librosa.amplitude_to_db(S)

        plt.figure(figsize=(secs_per_spec, 7))

        librosa.display.specshow(log_S, sr=rate, x_axis='time', y_axis='mel')


        plt.tight_layout()
        plt.axis('off')
        plt.gray()
        plt.draw()

        import io
        buf = io.BytesIO()
        plt.savefig(buf, bbox_inches='tight', pad_inches = 0, dpi=50, format='jpg')

        buf.seek(0)
        img = Image.open(buf)
        img = img.crop((120, 4, img.size[0] - 3, img.size[1] - 20))

        if save:
            img.save(save_path + '_' + str(name_index) + '.jpg')
        else:
            specs.append(img)
        buf.close()

        plt.clf()
        plt.cla()
        plt.close()

        name_index += 1

    if not save:
        return specs




def all_audio_to_spec(audio_dir):
    """
    Used to get the dataset to train TF model on
    converts all fils in audio directory to spectrograms

    Args:
        audio_dir (str): directory where all audio files are kept, split by emotion
    """
    import glob
    audio = glob.glob(audio_dir + '/*.mp3')

    for a in audio:
        graph_spectrogram(a)


