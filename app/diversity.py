#
# Copyright 2021 Athina Georgara <ageorg@iiia.csic.es>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import copy
import operator

import numpy as np

QN = 0
QL = 1


class Agent(object):
	"""docstring for ClassName"""

	def __init__(self, id, attributes):
		self.id = id
		self.attributes = attributes
		self.equivalent = {attr: [] for attr in attributes}

	def getValue(self, attr):
		for i in self.attributes:
			if i == attr:return i.value
		return None

	def __str__(self):
		return str(self.id)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return (isinstance(other, Agent) and  self.id == other.id)

	def __le__(self, other):
		return (isinstance(other, Agent) and  self.id <= other.id)

	def __ge__(self, other):
		return (isinstance(other, Agent) and  self.id >= other.id)

	def __lt__(self, other):
		return (isinstance(other, Agent) and  self.id < other.id)
		
	def __gt__(self, other):
		return (isinstance(other, Agent) and  self.id > other.id)

	def __hash__(self):
		return hash(self.id)


class Attribute(object):
	"""docstring for ClassName"""

	def __init__(self, attribute_id, attribute_type, attribute_range, value=None):
		self.id = attribute_id
		self.type = attribute_type
		self.range = attribute_range
		self.value = value

	def __str__(self):
		return str(self.id)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return (isinstance(other, Attribute) and  self.id == other.id)

	def __le__(self, other):
		return (isinstance(other, Attribute) and  self.id <= other.id)

	def __ge__(self, other):
		return (isinstance(other, Attribute) and  self.id >= other.id)

	def __lt__(self, other):
		return (isinstance(other, Attribute) and  self.id < other.id)
		
	def __gt__(self, other):
		return (isinstance(other, Attribute) and  self.id > other.id)

	def __hash__(self):
		return hash(self.id)


def diversity(team, attribute_ids):
	sd = 0
	for attr in attribute_ids:
		if attr.type == QL:
			freq = { option:0 for option in attr.range }
			for a in team:
				val = a.getValue(attr)
				freq[val] += 1
			prop = {option:freq[option] / len(team) for option in freq}
			diversity = sum([ -(prop[option] * np.log(prop[option])) / np.log(len(attr.range)) for option in prop if prop[option] > 0])
		else:
			diversity = np.std([a.getValue(attr) for a in team])
		sd += diversity
	return sd


def findEquivalentAgents(agent, attribute, agents, reqattr=None, epsilon=1e-2):
	eq = []
	if reqattr == None:
		reqattr = agent.attributes
	for a in agents:
		if a != agent:
			flag = True
			for attr in reqattr:
				if attr != attribute:
					cond = a.getValue(attr) != agent.getValue(attr) if attr.type == QL else abs(a.getValue(attr) - agent.getValue(attr)) > epsilon
					if cond:
						flag = False
						break
			if flag:
				eq.append(a)
	return eq


def changeDiversity (team, attribute, epsilon=0.1, positive=True):

	current_diversity = diversity(team, [attribute])
	alternative_teams = []
	for agent in team:
		for a in agent.equivalent[attribute]:
			if a not in team:
				new_team = sorted([i for i in team if i != agent] + [a])
				new_diversity = diversity(new_team, [attribute])
				diff = current_diversity - new_diversity

				# print(tuple(new_team),diff)
				if ((diff >= epsilon and positive) or (diff <= epsilon and ~positive)) and (new_team not in alternative_teams):
					alternative_teams += [new_team]
	return alternative_teams


if __name__ == '__main__':

	agents = []
	attribute_ids = {1000:QN, 1001:QN, 1002:QL, 1003:QL, 1004:QN}
	options = ['poor', 'bad', 'mediocre', 'good', 'excellent']

	attribute_types = {QN:[0, 1], QL:options}
	print('Generating data...')
	for i in range(2000):
		attributes = []
		for attr in attribute_ids:
			val = list(np.random.choice(options, 1))[0] if attribute_ids[attr] == QL else np.random.uniform(0, 1),
			attributes.append(
				Attribute(
					attr, attribute_ids[attr], attribute_types[attribute_ids[attr] ], val[0]
					)
				)
		agents.append(Agent(i, attributes))

	print('Diversity')
	reqattr = [Attribute(1000, QN, [0, 1]), Attribute(1002, QL, options)]
	print(diversity(agents, reqattr))
	team = list(np.random.choice(agents, 30, replace=False))
	print(team)
	print('-' * 50)

	print('Finding Equivalences...')
	for agent in agents:
		for attr in reqattr:
			agent.equivalent[attr] = findEquivalentAgents(agents[0], attr, agents, reqattr=reqattr)

	attr = reqattr[0]
	alternative_teams = changeDiversity(team, attr, epsilon=0.1, positive=False)
	for team_ in alternative_teams:
		print(team_, diversity(team_, reqattr))
