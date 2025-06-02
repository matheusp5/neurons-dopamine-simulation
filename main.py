from enum import Enum
from time import sleep
import threading  

# maybe there will have a thread just for checking if
# there are dopamine in receptors

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
  dopamine_presence = False
  
  def __init__(self, neuron: Excitable):
    self.neuron = neuron
  
  def trigger_dopamine_release(self, time = 1):
    print('Dopamine released')
    self.dopamine_presence = True
    sleep(time)
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

  def trigger_potential_dopamine_action(self):

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
    
def check_dopamine_for_receptor(receptor: DopamineReceptor):
  print('Checking dopamine presence for receptor...')

  while(True):
    if receptor.dopamine_presence:
      print('Has dopamine')
    else:
      print('No dopamine')
    sleep(1)


# tests

dopamine_receptor = D1DopamineReceptor()

thread = threading.Thread(target=check_dopamine_for_receptor,args=(dopamine_receptor,))

thread.start()


sleep(2)

dopamine_receptor.trigger_dopamine_release()
