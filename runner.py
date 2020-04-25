#from pydub import AudioSegment
#from pydub.playback import play
#import wave, pyaudio
import time, os, sys
from pynput.keyboard import Key, Listener
from ucb import selection
import threading
#from playsound import playsound
#import pygame
from ucb import Tree
#import mido
#from pythonosc import udp_client
import OSC
import requests

#pygame.init()

#client = udp_client.SimpleUDPClient("127.0.0.1", 57120)
OSC_client = OSC.OSCClient()
OSC_client.connect(('127.0.0.1', 57120))   
URL = 'https://webdocs.cs.ualberta.ca/~yourui/index.py'

th = None
fn = [f for f in os.listdir('./audio/') if f.endswith(".wav")]
s = None
send = None
req_data = {}

start_time = None
maximum_reward = 100
maxmimum_time = 50
numstep = 0
numsteps = 100

def on_press(key):
	global runner, th, start_time

	rew = 0
	if key == Key.esc:
		th.cancel()
		return False
	if key == Key.enter:
		th.cancel()
		elpased_time = time.time()-start_time
		rew = 1.0*elpased_time*maximum_reward/maxmimum_time # linear function
		print("key pressed")
		runner.reward(rew)


class Runner(object):

	def __init__(self):
		self.path = './audio/'
		self.filenames = fn
		#self.filenames = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
		self.mp3_list = []
		self.audio_dict = {}
		self.new_reward = False
		self.reward = 0
		self.num = 3
		self.selected = range(self.num) #initial
		self.playtime = maxmimum_time # 30 secs
		self.UCB = Tree()

		print(self.UCB)
		i = 0
		'''
		for aud in self.filenames:
			print(aud)
			self.audio_dict[i] = aud
			i += 1
			#self.mp3_list.append(sa.wavread(self.path+aud))
			self.mp3_list.append(AudioSegment.from_file(self.path+aud))
		'''

	def get_next(self):
		rew = maximum_reward
		self.reward = rew
		#print(self.filenames)
		if not self.new_reward:
			self.selected = self.UCB.UCB_step(rew, numstep)
			#self.selected = selection(rew)
			print("from get_next")

	def play(self):
		global th, s, start_time, numstep, numsteps, send
		numstep += 1
		self.get_next()
		th = threading.Timer(self.playtime, self.play)
		th.start()
		start_time = time.time()
		self.new_reward = False
		# TODO: play self.ids
		#print(self.selected)
		send_list_first = [0]*self.selected[0]*len(self.selected[1])
		send_list_last = [0]*(self.UCB.num_ind-(self.selected[0]+1)*len(self.selected[1]))
		send_list_middle = []

		for s in self.selected[1]:
			if s == 0:
				send_list_middle.append(0.2)
			else:
				send_list_middle.append(0.8)
		send = send_list_first + send_list_middle + send_list_last
		req_data['songs'] = send
		req_data['timestamp'] = start_time
		req_data['reward'] = self.reward
		#send = ' '.join(str(e) for e in send_list_first)+ ' '+' '.join(str(e) for e in self.selected[1])+' '+' '.join(str(e) for e in send_list_last)
		#send = ' '.join(str(e) for e in send)
		#print(send)
		oscmsg = OSC.OSCMessage()
		oscmsg.setAddress("/print")
		for s in send:
			oscmsg.append(s)
		OSC_client.send(oscmsg)
		
		# send http get request
		print(req_data)
		r = requests.get(url = URL, params = req_data) 	
		#print(r)
		#client.send_message("/print", send)
		'''
		if len(self.selected) == 1:
			mixed = self.mp3_list[self.selected[0]]
		else:
			mixed = self.mp3_list[self.selected[0]].overlay(self.mp3_list[self.selected[1]])
		for i in range(len(self.selected)):
			if i <= 1:
				continue
			else:
				mixed1 = mixed.overlay(self.mp3_list[self.selected[i]])
		mixed.export("mixed.wav", format='wav')
		s = pygame.mixer.Sound("mixed.wav")
		s.play()
		'''
		#msg = mido.Message('note_on', note=0)


	def reward(self, rew):
		global th, send
		self.reward = rew
		self.new_reward = True
		self.selected = self.UCB.UCB_step(rew,numstep)
		#self.selected = selection(rew)
		self.play()
		print("from new_reward")


def main():
	global runner

	numsteps = 100
	runner = Runner()
	runner.play()
	with Listener(on_press=on_press) as listener:
		listener.join()

main()



# ask abram: how long for human to listening and break
# human machine interaction testing setting (look for literature)
# write a script for cutting the first one minute audio

'''
/ lopen 0 0 0 0\
127.0.0.1:57125
ADSR envelope, trigger
'''

'''
envolpes of sounds
balance the total volume (maximum volume)
'''
