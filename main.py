from enum import Enum
from time import sleep
import threading  
from datetime import datetime
import sys
import tty
import termios

# check dopamine present in dopamine receptor instead of neuron
# Show de Bola 👍

DOPAMINE_RELEASE_AMOUNT = 1

class ActionType(Enum):
  play_with_friends = 'play_with_friends'
  eat_food = 'eat_food'
  watch_movie = 'watch_movie'
  read_book = 'read_book'
  exercise = 'exercise'
  listen_music = 'listen_music'
  meditate = 'meditate'
  use_cocaine = 'use_cocaine'
  use_cannabis = 'use_cannabis'

class Action:
  def __init__(self, key: str, text: str, action_type: ActionType, increased_dopamine_release: int, time_to_call_dat_transporters: int, affects_cb1_receptors: bool = False):
    self.increased_dopamine_release = increased_dopamine_release
    self.time_to_call_dat_transporters = time_to_call_dat_transporters
    self.action_type = action_type
    self.text = text
    self.key = key[0]
    self.affects_cb1_receptors = affects_cb1_receptors

def make_actions():
  actions = (
    Action('p', 'Play with friends', ActionType.play_with_friends, increased_dopamine_release=2, time_to_call_dat_transporters=5),
    Action('e', 'Eat food', ActionType.eat_food, increased_dopamine_release=1, time_to_call_dat_transporters=3),
    Action('w', 'Watch movie', ActionType.watch_movie, increased_dopamine_release=1, time_to_call_dat_transporters=4),
    Action('r', 'Read book', ActionType.read_book, increased_dopamine_release=1, time_to_call_dat_transporters=2),
    Action('x', 'Exercise', ActionType.exercise, increased_dopamine_release=3, time_to_call_dat_transporters=6),
    Action('l', 'Listen music', ActionType.listen_music, increased_dopamine_release=2, time_to_call_dat_transporters=5),
    Action('m', 'Meditate', ActionType.meditate, increased_dopamine_release=1, time_to_call_dat_transporters=3),
    Action('c', 'Use cocaine', ActionType.use_cocaine, increased_dopamine_release=5, time_to_call_dat_transporters=30),
    Action('n', 'Use cannabis', ActionType.use_cannabis, increased_dopamine_release=4, time_to_call_dat_transporters=45, affects_cb1_receptors=True)
  )

  dictionary_actions = {action.key: action for action in actions}

  return actions.count, dictionary_actions, actions

class Excitable:  
  excitement_level = 0

  def increase_excitement(self, amount: int):
    self.excitement_level += amount

  def decrease_excitement(self, amount: int):
    if self.excitement_level - amount < 0:
      self.excitement_level = 0
    else:
      self.excitement_level -= amount

class CB1Receptor:
  activated = False
  
  def activate(self, duration: int):
    self.activated = True
    sleep(duration)
    self.activated = False

class DopamineReceptor:
  dopamine_presence = False
  
  def trigger_dopamine_release(self, action: Action, neuron: Excitable, cb1_activated: bool = False):
    self.dopamine_presence = True

    t1 = threading.Thread(target=self.increase_excitement_level, args=(action, neuron, cb1_activated))
    t1.daemon = True
    t1.start()

    # trigger DAT transporter for dopamine reuptake
    sleep(action.time_to_call_dat_transporters)

    self.dopamine_presence = False

  def increase_excitement_level(self, action: Action, neuron: Excitable, cb1_activated: bool) -> bool:
    while self.dopamine_presence:
        dopamine_to_increase = DOPAMINE_RELEASE_AMOUNT * action.increased_dopamine_release
        
        # If CB1 receptors are activated (by cannabis), increase dopamine effect
        if cb1_activated:
          dopamine_to_increase = int(dopamine_to_increase * 1.5)
        
        neuron.increase_excitement(dopamine_to_increase)  
        sleep(1)  # simulate time taken for dopamine release

class D2DopamineReceptor(DopamineReceptor):
  def __init__(self):
    pass

class D1DopamineReceptor(DopamineReceptor):
  def __init__(self):
    pass

class Neuron(Excitable):
  def __init__(self, d1_dopamine_receptors: list[D1DopamineReceptor], 
               d2_dopamine_receptors: list[D2DopamineReceptor],
               cb1_receptors: list[CB1Receptor] = None):
      self.d1_dopamine_receptors = d1_dopamine_receptors
      self.d2_dopamine_receptors = d2_dopamine_receptors
      self.cb1_receptors = cb1_receptors if cb1_receptors else []

  def trigger_potential_dopamine_action(self, action: Action):
    cb1_activated = False
    
    # If action affects CB1 receptors (like cannabis), activate them
    if action.affects_cb1_receptors and self.cb1_receptors:
      for receptor in self.cb1_receptors:
        threading.Thread(target=receptor.activate, args=(action.time_to_call_dat_transporters,)).start()
      cb1_activated = True

    for receptor in self.d1_dopamine_receptors:
      threading.Thread(target=receptor.trigger_dopamine_release, args=(action, self, cb1_activated)).start()

  def some_receptor_with_dopamine(self) -> bool:
    return any(receptor.dopamine_presence for receptor in self.d1_dopamine_receptors + self.d2_dopamine_receptors)

  def add_d1_dopamine_receptor(self, receptor: D1DopamineReceptor):
    self.d1_dopamine_receptors.append(receptor)

  def add_d2_dopamine_receptor(self, receptor: D2DopamineReceptor):
    self.d2_dopamine_receptors.append(receptor)

  def add_cb1_receptor(self, receptor: CB1Receptor):
    self.cb1_receptors.append(receptor)

class Brain:
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
          neuron.decrease_excitement(DOPAMINE_RELEASE_AMOUNT * 2)

        sleep(1)

  def print_excitement_level(self):
    while True:
      total_excitement_level = self.get_total_excitement_level()
      current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

      msg = f'{current_time} | Brain excitement level: {total_excitement_level}'
      print('\r' + msg.ljust(80), end='', flush=True)

      sleep(1)

def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def main(): 
  d1_receptor1 = D1DopamineReceptor()
  d1_receptor2 = D1DopamineReceptor()
  cb1_receptor1 = CB1Receptor()
  cb1_receptor2 = CB1Receptor()

  neuron1 = Neuron([d1_receptor1], [d1_receptor2], [cb1_receptor1, cb1_receptor2])

  brain = Brain([neuron1])

  _, actions_dict, actions = make_actions()

  print(f'Available actions:')

  for i, action in enumerate(actions):
    print(f'Type "{action.key}" to "{action.text}"')

  print('\nPress "q" to quit the program.\n')

  print('-' * 15 + '\n')

  sleep(3)

  # automatic decrease dopamine level if there arent't 
  t1 = threading.Thread(target=brain.decrease_dopamine_level)
  t1.daemon = True
  t1.start()

  # automatic print excitement level
  t2 = threading.Thread(target=brain.print_excitement_level)
  t2.daemon = True
  t2.start()

  while True:
    char = read_key()
      
    if char.lower() == 'q':
      # by default, as a multi-threading program its 
      # necessary to kill all child threads
      # and then we can exit the program.
      # but all threads are daemon threads
      # and deamon threads are killed when the main thread exits
      sys.exit(0)
      break;
    else:
      action = actions_dict.get(char.lower())

      if action is None:
        print(f'Invalid action key: {char}')
        continue

      brain.execute_action(action)

    sleep(1)  # avoid busy waiting

if __name__ == '__main__':
  main()