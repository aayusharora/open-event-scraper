import os
import requests


def save_audio(audio_url, filename, dirname='audio'):
	try:
		audio_content = requests.get(audio_url).content
		filename = os.path.join(dirname, filename)
		f = open((filename), 'wb')
		f.write(audio_content)
		f.close()

		return filename
	except:
		return ""
