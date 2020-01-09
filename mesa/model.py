# model.py

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class SchellingAgent(Agent):
	'''
	Schelling segregation agent
	'''

	def __init__(self, position, model, agent_type):
		super().__init__(position, model)
		self.position = position
		self.type = agent_type

	# step function
	def step(self):
		similar = 0
		# find similar neighbours
		for neighbour in self.model.grid.neighbor_iter(self.position):
			if neighbour.type == self.type:
				similar += 1

		# move to random empty location
		if similar < self.model.homophily:
			self.model.grid.move_to_empty(self)

		else:
			self.model.happy += 1

class Schelling(Model):
	'''
	Model for Schelling segregation agent
	'''

	def __init__(self, height, width, density, minority_pc, homophily):
		self.height = height
		self.width = width
		self.density = density
		self.minority_pc = minority_pc
		self.homophily = homophily

		# grid
		self.grid = SingleGrid(height, width, torus=True)

		# schedule
		self.schedule = RandomActivation(self)

		# datacollector
		self.happy = 0
		self.datacollector = DataCollector(
			{ "happy": "happy" }, 
			{"x": lambda a: a.position[0], "y": lambda a: a.position[1]}
		)

		# agent setup
		for cell in self.grid.coord_iter():
			x = cell[1]
			y = cell[2]

			if self.random.random() < self.density:
				if self.random.random() < self.minority_pc:
					agent_type = 1
				else:
					agent_type = 0

				agent = SchellingAgent((x, y), self, agent_type)
				self.grid.position_agent(agent, (x, y))
				self.schedule.add(agent)

		self.running = True
		self.datacollector.collect(self)

	def step(self):
		# reset at each step
		self.happy = 0
		self.schedule.step()

		# collect data
		self.datacollector.collect(self)

		# stop if all agents are happy
		if self.happy == self.schedule.get_agent_count():
			self.running = False




