from enum import Enum
from time import sleep
import threading  
from datetime import datetime

# check dopamine present in dopamine receptor instead of neuron
# Show de Bola 👍

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
  
  def trigger_dopamine_release(self, action: Action):
    self.dopamine_presence = True

    threading.Thread(target=self.increase_excitement_level, args=(action,)).start()

    # trigger DAT transporter for dopamine reuptake
    sleep(action.time_to_call_dat_transporters)

    self.dopamine_presence = False

  def increase_excitement_level(self, action: Action) -> bool:
    while self.dopamine_presence:
        dopamine_to_increase = DOPAMINE_RELEASE_AMOUNT * action.increased_dopamine_release
        self.neuron.increase_excitement(dopamine_to_increase)  

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

    # for receptor in self.d2_dopamine_receptors:
    #   threading.Thread(target=receptor.trigger_dopamine_release, args=(action.time_to_call_dat_transporters,)).start()

  def some_receptor_with_dopamine(self) -> bool:
    return any(receptor.dopamine_presence for receptor in self.d1_dopamine_receptors + self.d2_dopamine_receptors)

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
  
  def execute_action(self, action: Action):
    for neuron in self.neurons:
      neuron.trigger_potential_dopamine_action(action)

  def some_receptor_with_dopamine(self) -> bool:
    return any(neuron.some_receptor_with_dopamine() for neuron in self.neurons)
  
  def get_total_excitement_level(self) -> int:
    return sum(neuron.excitement_level for neuron in self.neurons)
  
  def decrease_dopamine_level(self):
    while True:
      for neuron in self.neurons:
        if not neuron.some_receptor_with_dopamine():
          neuron.decrease_excitement(DOPAMINE_RELEASE_AMOUNT)

        sleep(1)

  def print_excitement_level(self):
    total_excitement_level = self.get_total_excitement_level()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(f'{current_time} Neuron excitement level: {total_excitement_level}')
    print('---')

    


def main(): 
  brain = Brain()

  # automatic decrease dopamine level if there arent't 
  threading.Thread(target=brain.decrease_dopamine_level, args=(brain,)).start()

  # automatic print excitement level
  threading.Thread(target=brain.print_excitement_level).start()

if __name__ == '__main__':
  main()