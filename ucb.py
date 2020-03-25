import numpy as np
import math
#import matplotlib.pyplot as plt
#from scipy.stats import bernoulli
import random
from itertools import combinations 

num_arm = 5
arms = range(5)
num_select = 2

timesteps = 0
num = 100
k = 10
delta = 1.0/(num*num)

class Node(object):
	"""docstring for Node"""
	def __init__(self, value, depth, parent):
		self.ucb = np.inf
		self.num = 0
		self.mean = np.inf
		self.depth = depth
		#self.next_layer = next_layer
		self.children = None
		self.parent = parent
		self.value = value
		self.msg = None

	def parent():
		return self.parent



class Tree(object):
	"""docstring for UCT"""
	def __init__(self):
		
		self.value = 'a'
		self.act_val = 0
		self.num_ind = 15
		self.msg_val = [[1,1,1],[1,1,2],[1,2,1],[1,2,2],[2,1,1],[2,1,2],[2,2,1],[2,2,2]]		
		self.all_actions = []
		self.a_t = 0
		self.max_ucb = 0
		self.initialization()
		self.init_true = False

	def initialization(self):
		#root
		self.root = Node(self.value, 0, None)

		self.value = chr(ord(self.value) + 1)
		#first layer: 5 nodes
		first_layer = []
		for i in range(5):
			new_node = Node(self.value, 1, self.root)
			self.value = chr(ord(self.value) + 1)
			first_layer.append(new_node)
		
		self.root.children = first_layer


		#second layer: each node has 2^3 children
		for second in self.root.children:
			second_layer = []
			for i in self.msg_val:
				new_node = Node(self.act_val, 2, second)
				self.act_val += 1
				new_node.msg = i
				second_layer.append(new_node)
			second.children = second_layer
			self.all_actions += second_layer

		#print(self.all_actions)

	def traverse(self, children):
		if children == None:
			return
		for c in children:
			print(c.value, c.ucb)
			self.traverse(c.children)

	def result(self):
		# finding the maximum ucb in first layer
		max_ucb = 0
		first_node = 0
		for c in self.root.children:
			if max_ucb < c.mean:
				max_ucb = c.mean
				first_node = c.value
				#print(max_ucb, first_node)


		# finding the maximum ucb in second layer
		max_ucb = 0
		second_node = 0
		for c in self.root.children[ord(first_node)-ord('b')].children:
			if max_ucb < c.mean:
				max_ucb = c.mean
				second_node = c.value

		act = [ord(first_node)-ord('b'), self.msg_val[int(second_node%len(self.msg_val))]]
		#self.a_t = act[0]*len(self.msg_val) + int(second_node%len(self.msg_val))

		return act


	def UCB_step(self, reward, numsteps):
		if not self.init_true:
			self.init_true = True
			return [0,[1,1,1]]
		#print("reward from UCB_step ", reward)
		# get node in first layer
		fir_node = self.root.children[int(self.a_t/len(self.msg_val))]

		if fir_node.mean == np.inf:
			fir_node.mean = reward
		else:
			fir_node.mean = (fir_node.mean*fir_node.num + reward)/(fir_node.num+1)
		fir_node.num += 1
		fir_node.ucb  = fir_node.mean + math.sqrt(2*math.log(1.0/delta)/fir_node.num)

		# get node in second layer
		sec_node = fir_node.children[int(self.a_t%len(self.msg_val))]

		if sec_node.mean == np.inf:
			sec_node.mean = reward
		else:
			sec_node.mean = (sec_node.mean*sec_node.num + reward)/(sec_node.num+1)

		sec_node.num += 1
		bias = 1#2*1.0/math.sqrt(3)
		sec_node.ucb = sec_node.mean + bias*math.sqrt(2*math.log(numsteps)/sec_node.num)

		'''
		# updating the value of fir_node
		max_ucb = 0
		for c in fir_node.children:
			if max_ucb < c.ucb and c.ucb != np.inf:
				max_ucb = c.ucb

		fir_node.ucb = max_ucb
		'''

		#self.traverse(self.root.children)

		# finding the maximum ucb in first layer
		max_ucb = 0
		first_node = 0
		for c in self.root.children:
			if max_ucb < c.ucb:
				max_ucb = c.ucb
				first_node = c.value
				#print(max_ucb, first_node)


		# finding the maximum ucb in second layer
		max_ucb = 0
		second_node = 0
		for c in self.root.children[ord(first_node)-ord('b')].children:
			if max_ucb < c.ucb:
				max_ucb = c.ucb
				second_node = c.value

		act = [ord(first_node)-ord('b'), self.msg_val[int(second_node%len(self.msg_val))]]
		self.a_t = act[0]*len(self.msg_val) + int(second_node%len(self.msg_val))

		return act

'''
class UCB(object):
	"""docstring for UCB"""
	def __init__(self, step):
		# actions: all combinations of 5 choose 2
		self.actions = self.choose(step)
		self.means = [np.inf]*len(self.actions)
		self.ucb = [np.inf]*len(self.actions)
		self.num_ucb = [0]*len(self.actions)
		self.a_t = 0

	def choose(self, step):
		comb = []
		if step == 0:
			acts = list(combinations(arms, 1))
		if step == 1:
			acts = list(combinations(arms, num_select))
		
		for a in acts:
			newact = [0]*num_arm
			for i in a:
				newact[i] = 1
			comb.append(newact)
		return comb



	def UCB_step(self, reward):

		if self.means[self.a_t] == np.inf:
			self.means[self.a_t] = reward
		else:
			self.means[self.a_t] = (self.means[self.a_t]*self.num_ucb[self.a_t] + reward)/(self.num_ucb[self.a_t]+1)
		
		self.num_ucb[self.a_t] += 1
		#if self.num_ucb[self.a_t] != 0:
		self.ucb[self.a_t] = self.means[self.a_t] + math.sqrt(2*math.log(1.0/delta)/self.num_ucb[self.a_t])
		

		self.a_t = np.argmax(self.ucb)
		act = self.actions[self.a_t]
		ret = []
		for i in range(len(act)):
			if act[i] == 1:
				ret.append(i)
		print(self.a_t, self.ucb)
		return ret
'''
# random selection
def selection(reward):
	allselect = [0,1,2,3,4,5,6,7,8,9]
	random.shuffle(allselect)
	return allselect[:3]
