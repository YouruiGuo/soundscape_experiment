import requests

volumes = [[1,1,1],[1,1,2],[1,2,1],[1,2,2],[2,1,1],[2,1,2],[2,2,1],[2,2,2]]
url = 'https://webdocs.cs.ualberta.ca/~yourui/djcontrol_server.py'
current_url = 'https://webdocs.cs.ualberta.ca/~yourui/currentplaying.py'

res = requests.post(url=current_url)
uuid = res.content

while True:
	song = input('enter the song number (0-4):')
	volume = input('enter the volume number (0-7):')
	data = {}
	data['song'] = song
	data['volume'] = volumes[volume]
	data['uuid'] = uuid
	r = requests.get(url = URL, params = data)
