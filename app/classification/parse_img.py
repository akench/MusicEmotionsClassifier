import PIL.ImageOps
from PIL import Image
import numpy as np
from random import *

def resize_crop(img, save_path = None, crop_type = 'center', size = None, grey = True):
	'''
	Args:
		img : image to crop and resize
	 	save_path : where to save image, if not None
		crop_type : 'center' or 'random'
	 	size : width of resized img
	Returns:
		cropped and resized image
	'''

	if not isinstance(img, Image.Image):
		try:
			img = Image.open(img)
		except IOError:
			raise ValueError('file %s not found' % (img))

	if grey:
		img = img.convert('L')


	w = img.size[0]
	h  = img.size[1]

	center_w = w // 2
	center_h = h // 2

	#if pix is horizontal
	if w > h:

		if crop_type == 'center':

			img = img.crop(
				(
					center_w - h // 2,
					0,
					center_w + h // 2,
					h
				)
			)
		elif crop_type == 'random':

			if w//8 > w-h:
				start_width = randint(0, w - h)
			else:
				start_width  = randint(w//8, w - h)

			img = img.crop(
				(
					start_width,
					0,
					start_width + h,
					h
				)
			)
		elif crop_type is None:
			pass
		else:
			raise ValueError("Invalid crop type")


	#img is vertical
	elif w < h:
		if crop_type == 'center':

			img = img.crop(
				(
					0,
					center_h - w // 2,
					w,
					center_h + w // 2
				)
			)
		elif crop_type == 'random':

			if h // 8 > h - w:
				start_height = randint(0, h-w)
			else:
				start_height  = randint(h // 8, h - w)

			img = img.crop(
				(
					0,
					start_height,
					w,
					start_height + w
				)
			)
		elif crop_type is None:
			pass
		else:
			raise ValueError("Invalid crop type")


	if size is not None:
		img = img.resize((size, size), PIL.Image.ANTIALIAS)

	if save_path is not None:
		img.save(save_path)

	return img