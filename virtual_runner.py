from ucb import Tree
import os
import random
import numpy as np
import operator
import math

th = None
fn = [f for f in os.listdir('./audio/') if f.endswith(".wav")]
s = None
gamma = 0.9
radius = 8

start_time = None
maximum_reward = 1
maxmimum_time = 30

class VirtualSubject(object):
	"""docstring for VirtualSubject"""
	def __init__(self):
		super(VirtualSubject, self).__init__()
		self.msg_val = [[1,1,1],[1,1,2],[1,2,1],[1,2,2],[2,1,1],[2,1,2],[2,2,1],[2,2,2]]
		self.reward = {}
		self.max_elapsed_time = 50 # max 60 secs
		self.allactions = self.getAllActions()
		self.goal = self.getGoal()
		

	def getAllActions(self):
		allactions = []

		for i in range(5):
			ra = random.random()
			for msg in self.msg_val:
				a = [i] + msg
				allactions.append(a)
				'''
				randrew = np.random.normal(ra, 0.05)
				if randrew > 1:
					randrew = 1
				if randrew < 0:
					randrew = 0
				self.reward[tuple(a)] = randrew
				'''
		#print(self.reward)
		
		return allactions

	def getGoal(self):
		goal = []
		ra = random.randint(0,4)
		#print(ra)
		for i in range(15):
			if int(i/3) == ra:
				goal.append(random.randint(1,2))
			else:
				goal.append(0)
		#goal = max(self.reward.items(), key=operator.itemgetter(1))[0]
		'''
		goal = []
		for i in range(15):
			goal.append(random())
		'''

		g = goal[3*ra:3*(ra+1)]

		for i in range(5):
			for msg in self.msg_val:
				dis = 0
				if i == ra:
					for x in range(3):
						dis += (msg[x]-g[x])**2
				else:
					for x in range(3):
						dis += (msg[x])**2
						dis += (g[x])**2
				dis = math.sqrt(dis)

				a = [i]+msg
				
				#distance based reward model
				#self.reward[tuple(a)] = (-1.0/radius) * (dis - radius)

				
				# one-button reward model
				
				if dis == 0:
					dis = 0.0001
				rew = (1.0/dis)*self.max_elapsed_time + np.random.normal(0, 2)
				self.reward[tuple(a)] = 1.0/(1+np.exp(-0.2*rew+5));
				
	
		#print(goal)
		#print(self.reward)
		return list([ra]+g)



class Runner(object):

	def __init__(self, f):
		self.path = './audio/'
		self.filenames = fn
		#self.filenames = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
		self.mp3_list = []
		self.audio_dict = {}
		self.new_reward = False
		self.num = 3
		self.selected = [0,[1,1,1]] #initial
		self.playtime = maxmimum_time # 30 secs
		self.UCB = Tree()
		self.subject = VirtualSubject()
		self.goal = None
		self.f = f

		#print(self.UCB)
		i = 0



	def play(self, numsteps):
		# TODO: play self.ids
		self.goal = self.subject.goal
		
		arew = 0
		dis = 0
		numstep = 0
		while numstep < numsteps:
			#print(self.selected)
			rew = self.reward(numstep)
			arew = arew*gamma + (1-gamma)*rew
			numstep += 1
		res = self.UCB.result()
		#print(res)
		cur = res[0]*3*[0]
		cur += res[1]
		cur += (15-len(cur))*[0]

			
		goal = self.goal[0]*3*[0]+self.goal[1:]
		goal += (15-len(goal))*[0]
		for i in range(15):
			dis += (cur[i]-goal[i])*(cur[i]-goal[i])
		dis = math.sqrt(dis)
		#print(cur, goal)
		ret = [str(dis), str(arew)]
		ret = " ".join(ret)
		ret += "\n"
		#print(ret)
		self.f.write(ret)
		return [dis, arew]

	def reward(self, numsteps):
		rew = self.subject.reward[tuple([self.selected[0]]+self.selected[1])]
		self.selected = self.UCB.UCB_step(rew, numsteps)
		#print("here", self.selected)
		#self.selected = selection(rew)
		return rew



def main():
	global runner
	trials = 1000
	num_steps = range(10,1001)
	num_steps = num_steps[::10]
	for numsteps in num_steps:
		fi = "../finalexp/distance_based/uct/1000steps/uct_"+str(numsteps)+"steps_1000trials.txt"
		with open(fi, "w") as f:

			print(numsteps)
			trials = 1000
			while trials > 0:
				runner = Runner(f)
				runner.play(numsteps)
				trials -= 1

main()
