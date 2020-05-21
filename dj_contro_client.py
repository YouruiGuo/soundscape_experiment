import requests
import re

volumes = [[1,1,1],[1,1,2],[1,2,1],[1,2,2],[2,1,1],[2,1,2],[2,2,1],[2,2,2]]
URL = 'https://webdocs.cs.ualberta.ca/~yourui/djcontrol_server.py'
current_url = 'https://webdocs.cs.ualberta.ca/~yourui/currentplaying.py'

res = requests.post(url=current_url)
uuid = re.findall(r'\n([^|\n]*)\n', res.content)

while True:
	song = input('enter the song number (0-4):')
	volume = input('enter the volume number (0-7):')
	data = {}
	data['song'] = song
	data['volume'] = volumes[volume]
	data['uuid'] = uuid
	print(data)
	r = requests.get(url = URL, params = data)
	print(r.content)
