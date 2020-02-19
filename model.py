import sys
sys.path.insert(0, ".//Agents")

import time
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation,SimultaneousActivation,StagedActivation
import torch
import pyro
import torch.distributions as tod
import pyro.distributions as pyd
import matplotlib.pyplot as plt
from scipy.stats import poisson
import plotly.graph_objects as go
from scipy import ndimage
from Agents.labs import Labs
from Agents.funding import Funding
from Agents.researchers import Student,Junior
from Agents.landscape import Episthemic_Landscape

class WorldModel(Model):
    """A model with some number of agents."""
    def __init__(self, N_students,N_juniors,num_labs,elsize = 100,funding_nos = 12,num_topics = 5,m_j = 25_000 , m_u = 12_000,lamb = 0.1,remove_thres = 5):
        self.timestep = 0                             # Start of time in the model
        self.num_agents_s = N_students
        self.num_agents_j = N_juniors
        self.num_labs = num_labs
        self.funding_nos = funding_nos
        self.elsize = elsize
        model_stages = ["step_stage_1", "step_stage_2","step_stage_3","step_stage_4", "step_stage_5","step_stage_6","step_stage_7","step_stage_final"]
        self.topics = num_topics     # We start with having 5 topics
        self.m_j = 25_000
        self.m_u = 12_000
        self.lamb = lamb
        self.remove_thres = remove_thres
        self.schedule = StagedActivation(self,model_stages)
        lab_arr = []
        # Create agents
        for _ in range(self.topics):
            self.schedule.add(Episthemic_Landscape(0,self,self.elsize))
        for _ in range(self.funding_nos):
            self.schedule.add(Funding(0,self))
        for _ in range(self.num_agents_s):
            self.schedule.add(Student(0,self))
        for _ in range(self.num_agents_j):
            self.schedule.add(Junior(0,self))
        for j in range(self.num_labs):
            c = Labs(j,self)
            lab_arr.append(c)
        #self.sorted_labs = sorted(lab_arr, key=lambda x: x.lab_repute, reverse=True)
        #print("The lenght of",len(sorted_labs))
        #for lab in self.sorted_labs:
            self.schedule.add(c)
            #print("Lab",lab,"is added")
        
        

    def step(self,to_print = True):
        '''Advance the model by one step.'''
        self.timestep+= 1
        print("Timestep:",self.timestep)
        self.schedule.step()
        senior_agent =  [agent for agent in self.schedule.agents if (agent.category == 'S' and agent.is_funded )]
        sorted_senior_agent = sorted(senior_agent, key=lambda x: x.current_bid, reverse=True)

        junior_agent =  [agent for agent in self.schedule.agents if (agent.category == 'J')]
        sorted_senior_agent = sorted(senior_agent, key=lambda x: x.current_bid, reverse=True)

        student_agent =  [agent for agent in self.schedule.agents if (agent.category == 'U')]
        sorted_student_agent = sorted(student_agent, key=lambda x: x.reputation, reverse=True)

        lab_agent =  [agent for agent in self.schedule.agents if (agent.category == 'lab')]
        sorted_lab_agent = sorted(lab_agent, key=lambda x: x.lab_repute, reverse=True)

        print("--------")
        #print("Highest funded senior researcher is",sorted_senior_agent[-1].unique_id)
        print("--------")
        
        if to_print:
          
          for agent in sorted_senior_agent:
              agent.printing_step()

          print("=============")

        
          for agent in sorted_junior_agent:
              agent.printing_step()


          print("=============")

          
          for agent in sorted_student_agent:
              agent.printing_step()

          print("=============")

    
          for agent in sorted_lab_agent:
              agent.printing_step()



empty_model = WorldModel(30,30,10)
for _ in range(10):
  empty_model.step(to_print = False)
  print("-------------")