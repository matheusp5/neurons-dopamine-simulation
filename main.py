from enum import Enum
from time import sleep
import threading  

# check dopamine present in dopamine receptor instead of neuron

DOPAMINE_RELEASE_AMOUNT = 1

class ActionType(Enum):
  play_with_friends = 'play_with_friends'

class Action:
  def __init__(self, action_type: ActionType, increased_dopamine_release: int, time_to_call_dat_transporters: int):
    self.increased_dopamine_release = increased_dopamine_release
    self.time_to_call_dat_transporters = time_to_call_dat_transporters
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
  dopamine_presence = False
  
  def __init__(self, neuron: Excitable):
    self.neuron = neuron
  
  def trigger_dopamine_release(self, time_to_call_dat_transporters: int = 5):
    self.dopamine_presence = True

    # trigger DAT transporter for dopamine reuptake
    sleep(time_to_call_dat_transporters)
    self.dopamine_presence = False
    
    
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

  def trigger_potential_dopamine_action(self, action: Action):
    for receptor in self.d1_dopamine_receptors:
      threading.Thread(target=receptor.trigger_dopamine_release, args=(action.time_to_call_dat_transporters,)).start()

    for receptor in self.d2_dopamine_receptors:
      threading.Thread(target=receptor.trigger_dopamine_release, args=(action.time_to_call_dat_transporters,)).start()

  def add_d1_dopamine_receptor(self, receptor: D1DopamineReceptor):
    self.d1_dopamine_receptors.append(receptor)

  def add_d2_dopamine_receptor(self, receptor: D2DopamineReceptor):
    self.d2_dopamine_receptors.append(receptor)

  def check_dopamine_presence(self, action: Action) -> bool:
    for receptor in self.d1_dopamine_receptors + self.d2_dopamine_receptors:
      if receptor.dopamine_presence:
        dopamine_to_increase = DOPAMINE_RELEASE_AMOUNT * action.increased_dopamine_release
        self.increase_excitement(dopamine_to_increase)
      else:
        self.decrease_excitement(DOPAMINE_RELEASE_AMOUNT)
    

class Brain:
  neurons = []

  def __init__(self, neurons: list[Neuron]):
    self.neurons = neurons

  def add_neuron(self, neuron: Neuron):
    self.neurons.append(neuron)

  def calculate_total_dopamine(self) -> int:
    return sum(neuron.excitement_level for neuron in self.neurons)
  
  def execute_action(self, action: Action):
    for neuron in self.neurons:
      neuron.trigger_potential_dopamine_action(action)

