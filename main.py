from enum import Enum
from time import sleep

class ActionType(Enum):
  play_with_friends = 'play_with_friends'

class Action:
  def __init__(self, action_type: ActionType):
    self.action_type = action_type
    pass


class Excitable:  
  excitement_level = 0

  def increase_excitement(self, amount: int):
    self.excitement_level += amount

  def decrease_excitement(self, amount: int):
    if self.excitement_level - amount < 0:
      self.excitement_level = 0
    else:
      self.excitement_level -= amount

class DopamineReceptor:
  def __init__(self, neuron: Excitable):
    self.neuron = neuron
  
  def trigger_dopamine_release(self):
    self.neuron.increase_excitement(1)
    sleep(0.2)  
    self.neuron.decrease_excitement(1)
    
    
class D2DopamineReceptor(DopamineReceptor):
  def __init__(self):
    pass

class D1DopamineReceptor(DopamineReceptor):
  def __init__(self):
    pass

class Neuron(Excitable):
  d1_dopamine_receptors = []
  d2_dopamine_receptors = []

  def __init__(self, d1_dopamine_receptors: list[D1DopamineReceptor], 
               d2_dopamine_receptors: list[D2DopamineReceptor]):
      self.d1_dopamine_receptors = d1_dopamine_receptors
      self.d2_dopamine_receptors = d2_dopamine_receptors

  def trigger_action(self):
    pass

  def add_d1_dopamine_receptor(self, receptor: D1DopamineReceptor):
    self.d1_dopamine_receptors.append(receptor)

  def add_d2_dopamine_receptor(self, receptor: D2DopamineReceptor):
    self.d2_dopamine_receptors.append(receptor)

class Brain:
  neurons = []

  def __init__(self, neurons: list[Neuron]):
    self.neurons = neurons

  def add_neuron(self, neuron: Neuron):
    self.neurons.append(neuron)

  def calculate_total_dopamine(self) -> int:
    return sum(neuron.calculate_total_dopamine() for neuron in self.neurons)
  
  def execute_action(self, action):
    pass
    
  