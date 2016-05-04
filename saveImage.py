import os
import PIL
from PIL import Image
import requests


def save_img(img_url, filename, filter_image=True, dirname='speakers'):
	try:
		img_content = requests.get(img_url).content
		filename = os.path.join(dirname, filename)
		f = open((filename), 'wb')
		f.write(img_content)
		f.close()

		if filter_image:
			basewidth = 100
			img = Image.open(filename)
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img.save(filename)

		return filename
	except:
		return ""
