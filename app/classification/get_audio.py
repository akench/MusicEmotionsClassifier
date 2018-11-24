from __future__ import unicode_literals
import youtube_dl
from random import *
import os.path

def dl_audio(url):

	# format is 'https://www.youtube.com/embed/{vid_id}'
	vid_id = url.split('/')[-1]

	outfile = 'temp'

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
		info_dict = ydl.extract_info(url)
		title = info_dict.get('title', None)

	return (outfile + '.mp3', title)