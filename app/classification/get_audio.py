from __future__ import unicode_literals
import youtube_dl
from random import *
import os.path
from make_spectrogram import all_audio_to_spec

def dl_audio(url, emot, save = True):

	vid_id = url.split('=')[1]

	if emot is None:
		outfile = 'temp'
	else:	
		outfile = 'audio/' + emot + '/' + vid_id



	if os.path.exists(outfile + '.mp3'):
		print('.', end='', flush=True)
		return outfile + '.mp3'

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	    'outtmpl': outfile + '.%(ext)s'
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	return outfile + '.mp3'