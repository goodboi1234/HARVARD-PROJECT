from pomegranate import  bayesian_network
from pomegranate import Node

from pomegranate import DiscreteDistribution
from pomegranate import ConditionalProbabilityDistribution
from pomegranate import ConditionalProbabilityTable
import json
import os
import pandas as pd 
import numpy as np 
import re
import torch

# Making the Rain probabilities. Using DiscreteDistribution because it's the parent class.
rain1 = DiscreteDistribution({
    "none": 0.7,
    "light": 0.2,
    "heavy": 0.1
})

#MAKING THE NODE OUT OF IT
rain = Node(rain1 , name = "rain")

# Node for Track Maintenance. Typed conditional probability to represent that the probability
# of maintenance will depend on the probability of rain. Using ConditionalProbabilityDistribution.
maintainance = Node(ConditionalProbabilityDistribution(
    ["none", "yes", 0.4],
    ["none", "no", 0.6],
    ["light", "no", 0.8],
    ["light", "yes", 0.2],
    ["heavy", "yes", 0.9],
    ["heavy", "no", 0.1]
), name="maintainance")

# The conditional probability of Train.
train = Node(ConditionalProbabilityTable(
    [["none", "yes", "on time", 0.8],
     ["none", "yes", "delayed", 0.2],
     ["none", "no", "on time", 0.9],
     ["none", "no", "delayed", 0.1],
     ["light", "no", "delayed", 0.3],
     ["light", "no", "on time", 0.7],
     ["light", "yes", "delayed", 0.4],
     ["light", "yes", "on time", 0.6],
     ["heavy", "yes", "on time", 0.4],
     ["heavy", "yes", "delayed", 0.6],
     ["heavy", "no", "on time", 0.5],
     ["heavy", "no", "delayed", 0.5]
 ], [rain.distribution, maintainance.distribution]), name="train")

# Clearing with the Appointment module.
appointment = Node(ConditionalProbabilityTable([
    ["on time", "attend", 0.9],
    ["on time", "missed", 0.1],
    ["delayed", "attend", 0.6],
    ["delayed", "missed", 0.4]
], [train.distribution]), name="appointment")

# Now clearing with the Bayesian network.
model = p.BayesianNetwork()
model.add_states(rain, maintainance, train, appointment)

# Connecting nodes to define dependencies.
model.add_edge(rain, maintainance)
model.add_edge(rain, train)
model.add_edge(maintainance, train)
model.add_edge(train, appointment)

# Finalize the model.
model.bake()

