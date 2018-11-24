from __future__ import unicode_literals
import youtube_dl
from random import *
import os.path
from app.classification.make_spectrogram import all_audio_to_spec

def dl_audio(url, emot, save = True):

	# format is 'https://www.youtube.com/embed/{vid_id}'
	vid_id = url.split('/')[-1]

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
		# ydl.download([url])
		info_dict = ydl.extract_info(url)
		title = info_dict.get('title', None)

	return (outfile + '.mp3', title)