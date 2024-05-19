'''alpha_v2.py
("The redesigning and debugging of the alpha version of
Disability Simulator")
A SOLUZION problem formulation, for ZZ003.py.
'''
#<METADATA>
SOLUZION_VERSION = "3.0"
PROBLEM_NAME = "Disability Simulator"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Jack', 'Lauren', 'Donavan']
PROBLEM_CREATION_DATE = "28-APR-2024"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''This is the second alpha version of our disability simulator game.
 It will showcase the same elements as our original alpha version with a different
 design for the state of the game that will allow a smooth transfer over to the flask
 client.

'''
#</METADATA>

#<COMMON_DATA>
"""Game Metrics"""
import random as r;
HAPPINESS = 50
MAX_HAPPINESS = 100


"""Board"""
# Board Length should be length.
BOARD_LENGTH = 100

from enum import Enum

class SlotType(Enum):
    EVENT = "event"

    #TODO What is the purpose of empty slots if we do not have energy?
    EMPTY = "empty"

    #TODO Need to figure out how to show starting and ending messages if they are unique.
    # Should consider this when moving to the FLASK client.
    START = "start"
    END = "end"

"""Slot Values"""
SLOTS = {
    # TODO Need to come up with the exact details of events: scope, type, etc.
    # Slot = {
    #        0: {“message in slot”,  “(metric, cost)”, }
    #        }
    # cost: ("Happiness, Position")

    # Start
    0: {"type": "start", "message": "Welcome to your journey! Your choices will affect your happiness and position. Choose wisely and enjoy the ride.", "cost": None},

    # Positive Events
    1: {"type": "positive", "message": "You went to an amusement park with your family and gained 5 happiness and 5 position.", "cost": ((5, 5), (5, 4))},
    2: {"type": "positive", "message": "You went to the movies with your friends and gained 5 happiness and 2 position.", "cost": ((5, 2), (5, 1))},
    3: {"type": "positive", "message": "You went to your favorite concert and gained 5 happiness and 2 position.", "cost": ((5, 2), (5, 1))},
    4: {"type": "positive", "message": "You went to a baseball game and gained 5 happiness and 2 position.", "cost": ((5, 2), (5, 1))},
    5: {"type": "positive", "message": "You had enough energy to clean the house and gained 5 happiness and 2 position.", "cost": ((5, 2), (5, 1))},
    6: {"type": "positive", "message": "You received a compliment on your report and gained 3 happiness and 3 position.", "cost": ((3, 3), (3, 2))},
    7: {"type": "positive", "message": "You helped a friend move and gained 4 happiness and 1 position.", "cost": ((4, 1), (4, 0))},
    8: {"type": "positive", "message": "You volunteered at a local charity and gained 4 happiness and 3 position.", "cost": ((4, 3), (4, 2))},
    9: {"type": "positive", "message": "You had a relaxing day at the spa and gained 5 happiness and 1 position.", "cost": ((5, 1), (5, 0))},
    10: {"type": "positive", "message": "You completed a challenging project and gained 6 happiness and 4 position.", "cost": ((6, 4), (6, 3))},
    11: {"type": "positive", "message": "You hung out with friends on a Saturday evening and gained 2 happiness and 1 position.", "cost": ((2, 1), (2, 0))},
    12: {"type": "positive", "message": "You attended a friend's wedding and gained 4 happiness and 3 position.", "cost": ((4, 3), (4, 2))},
    13: {"type": "positive", "message": "You hosted a game night and gained 3 happiness and 2 position.", "cost": ((3, 2), (3, 1))},
    14: {"type": "positive", "message": "You joined a new club and gained 3 happiness and 2 position.", "cost": ((3, 2), (3, 1))},
    15: {"type": "positive", "message": "You attended a networking event and gained 2 happiness and 4 position.", "cost": ((2, 4), (2, 3))},
    16: {"type": "positive", "message": "You had a refreshing shower and gained 2 happiness and 1 position.", "cost": ((2, 1), (2, 0))},
    17: {"type": "positive", "message": "You finished all your laundry for the week and gained 4 happiness and 2 position.", "cost": ((4, 2), (4, 1))},
    18: {"type": "positive", "message": "You played guitar and learned a new song, so you gained 5 happiness and 3 position.", "cost": ((5, 3), (5, 2))},
    19: {"type": "positive", "message": "You took a day for self-care and gained 4 happiness and 2 position.", "cost": ((4, 2), (4, 1))},
    20: {"type": "positive", "message": "You went to the gym yesterday and gained 1 happiness and 1 position.", "cost": ((1, 1), (1, 0))},
    21: {"type": "positive", "message": "You got admitted as a teaching assistant for next quarter and gained 6 happiness and 5 position.", "cost": ((6, 5), (6, 4))},

    # Negative Events
    22: {"type": "negative", "message": "You weren't able to sleep last night, so you woke up tired and lost 5 happiness and 2 position.", "cost": ((-5, -2), (-5, -3))},
    23: {"type": "negative", "message": "You weren't able to do anything because your back pain increased and lost 5 happiness and 4 position.", "cost": ((-5, -4), (-5, -5))},
    24: {"type": "negative", "message": "You went grocery shopping and lost 0 happiness and 1 position.", "cost": ((0, -1), (0, -2))},
    25: {"type": "negative", "message": "You suddenly had a migraine and lost 5 happiness and 5 position.", "cost": ((-5, -5), (-5, -6))},
    26: {"type": "negative", "message": "You were too tired to cook, so you didn't eat and lost 5 happiness and 5 position.", "cost": ((-5, -5), (-5, -6))},
    27: {"type": "negative", "message": "You got stuck in traffic for hours and lost 3 happiness and 2 position.", "cost": ((-3, -2), (-3, -3))},
    28: {"type": "negative", "message": "You had a disagreement with a classmate and lost 4 happiness and 3 position.", "cost": ((-4, -3), (-4, -4))},
    29: {"type": "negative", "message": "You missed an important deadline and lost 5 happiness and 4 position.", "cost": ((-5, -4), (-5, -5))},
    30: {"type": "negative", "message": "You had a flat tire on the way to an event and lost 3 happiness and 1 position.", "cost": ((-3, -1), (-3, -2))},
    31: {"type": "negative", "message": "You had a family argument and lost 4 happiness and 3 position.", "cost": ((-4, -3), (-4, -4))},
    32: {"type": "negative", "message": "You skipped brushing your teeth and lost 1 happiness and 1 position.", "cost": ((-1, -1), (-1, -2))},
    33: {"type": "negative", "message": "You were too tired to wash the dishes yesterday and lost 3 happiness and 2 position.", "cost": ((-3, -2), (-3, -3))},
    34: {"type": "negative", "message": "You didn't have time to go to a concert due to headaches and lost 3 happiness and 1 position.", "cost": ((-3, -1), (-3, -2))},
    35: {"type": "negative", "message": "You neglected self-care and lost 4 happiness and 3 position.", "cost": ((-4, -3), (-4, -4))},
    36: {"type": "negative", "message": "You ate street food and got food poisoning and lost 3 happiness and 2 position.", "cost": ((-3, -2), (-3, -3))},
    37: {"type": "negative", "message": "You failed an important exam and lost 4 happiness and 4 position.", "cost": ((-4, -4), (-4, -5))},
    38: {"type": "negative", "message": "You had an argument with a friend and lost 3 happiness and 2 position.", "cost": ((-3, -2), (-3, -3))},
    39: {"type": "negative", "message": "You felt left out at a social gathering and lost 4 happiness and 2 position.", "cost": ((-4, -2), (-4, -3))},
    40: {"type": "negative", "message": "You canceled plans with friends at the last minute and lost 2 happiness and 2 position.", "cost": ((-2, -2), (-2, -3))},
    41: {"type": "negative", "message": "You were embarrassed in front of a group and lost 4 happiness and 3 position.", "cost": ((-4, -3), (-4, -4))},
    42: {"type": "negative", "message": "You missed a friend's important event and lost 3 happiness and 3 position.", "cost": ((-3, -3), (-3, -4))},

    # End
    43: {"type": "end", "message": "Congratulations! You've reached the end of your journey. Reflect on your experiences and the balance between happiness and position.", "cost": None}
}

"""Visualizations"""
NAMES = ['Player1','Player2']
#</COMMON_DATA>

#<COMMON_CODE>
class PlayerState():
  """Represents the state of a player in the game.

    Each PlayerState instance includes properties such as happiness, player name,
    disability status, and position. Only one player is assigned a disability,
    which is tracked using the disability_assigned class variable.

    Methods:
    - __eq__(self, s2): Compares two PlayerState instances for equality based on their property values.
    - __str__(self): Returns a textual description of a PlayerState instance.
    - __hash__(self): Generates a hash value for a PlayerState instance.
    - __copy__(self): Creates a deep copy of a PlayerState instance.
  """
  disability_assigned = False

  def __init__(self, player_name, d=None):
    if d==None:
      d = {'happiness': HAPPINESS,
           'playerName' : player_name,
           'disability' : False,
           'position' : 0
          }

      if not PlayerState.disability_assigned:
         d['disability'] = True
         PlayerState.disability_assigned = True

    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    txt = ""
    for prop in self.d.keys():
      if prop == 'playerName' or prop == 'disability':
        continue
      elif prop == 'grades':
        txt += f"{prop} {self.d[prop]:.2f}\n"
        continue
      txt += prop + " " + str(self.d[prop]) + "\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for prop in self.d.keys():
        news.d[prop] = self.d[prop]
    return news

class State():
  """Represents the state of the game.

    Each State instance includes properties such as the current player, the game board layout,
    player states (including their happiness, position, and disability status),
    the current message for the player, and the result of the last dice roll.
  """
  def __init__(self, d=None):
    if d==None:
        players_states = {i: PlayerState(i) for i in range(2)}

        d = {'currentPlayer' : 0,
           'board' : {},
           'players' : players_states,
           'message' : "",
           'currentRoll' : None
        }

        for i in range(BOARD_LENGTH):
          if i == 0:
              d['board'][i] = SlotType.START
          elif i == BOARD_LENGTH - 1:
              d['board'][i] = SlotType.END
          elif r.random() < 0.4:
              d['board'][i] = SlotType.EVENT
          else:
              d['board'][i] = SlotType.EMPTY

    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.

    txt = "\n"

    # Case 1: When it is the next player's turn.
    if self.d['message'] != "":
        txt += "You rolled a " + str(self.d['currentRoll']) + ".\n"
        txt += str(self.d['message']) + "\n"
        for player_name, player_state in self.d["players"].items():
            if self.d['currentPlayer'] != player_name:
                txt += "You now have " + str(player_state.d['happiness']) + " happiness "
                txt += "and are at position " + str(player_state.d['position'] + 1) + " on the board. \n \n"
        txt += "It is now " + str(self.d['currentPlayer']) + "'s turn. \n"
    else:
       # Case 2: When there is no previous player
       # Start State
       message = self.grab_slot_values("start")
       txt += str(message['message']) + "\n"

       txt += "It is " + str(self.d['currentPlayer']) + "'s turn. \n"
       for player_name, player_state in self.d["players"].items():
            if self.d['currentPlayer'] == player_name:
                txt += "You have " + str(player_state.d['happiness']) + " happiness "
                txt += "and are at position " + str(player_state.d['position'] + 1) + " on the board. \n \n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def __copy__(self):
    # Copies the state and returns the newly created copy.
    news = State({})
    for prop in self.d.keys():
        news.d[prop] = self.d[prop]
    return news

  def is_goal(self):
    return any(player_state.d["position"] == BOARD_LENGTH - 1 for player_state in self.d["players"].values())

  def current_player_slot_type(self):
    # Finds the slot type the current player is on.
    player_position = self.current_position(self.d['currentPlayer'])
    slot_type = self.d['board'][player_position]
    return slot_type

  # Should probably move these methods into PlayerState.
  def current_position(self, player):
    return self.d['players'][player].d['position']

  def has_disability(self):
    # Finds the current position of the current player.
    current_player = self.d['currentPlayer']
    return self.d['players'][current_player].d['disability']

  def grab_slot_values(self, slot_type):
    # Grabs the values of the slots: message
    event = SLOTS.get(0)
    while event and event["type"] != slot_type:
       event_id = int(r.random() * len(SLOTS))
       event = SLOTS.get(event_id)
    return event

  def handle_event(self):
    message_type = None
    # Grabs the corresponding message type based on the presence of a disability
    # and a hardcoded value.
    if self.has_disability:
        message_type = "negative" if r.random() < 0.7 else "positive"
    else:
        message_type = "negative" if r.random() < 0.5 else "positive"

    message = self.grab_slot_values(message_type)
    current_player = self.d['currentPlayer']
    self.d['message'] = message['message']

    cost_value = None
    if self.has_disability:
       cost_value = message['cost'][1]
    else:
       cost_value = message['cost'][0]

    # Updates happiness of the player.
    new_happiness = self.d["players"][current_player].d["happiness"] + cost_value[0]
    if new_happiness < 0:
        self.d["players"][current_player].d["happiness"] = 0
    elif new_happiness > MAX_HAPPINESS:
       self.d["players"][current_player].d["happiness"] = MAX_HAPPINESS
    else:
       self.d["players"][current_player].d["happiness"] = new_happiness

    # Updates position of the player.
    new_position = self.d["players"][current_player].d["position"] + cost_value[1]
    if new_position < 0:
       self.d["players"][current_player].d["position"] = 0
    elif new_position > BOARD_LENGTH:
       self.d["players"][current_player].d["position"] = BOARD_LENGTH
    else:
       self.d["players"][current_player].d["position"] = new_position

  def handle_empty_slot(self):
    self.d['message'] = "You landed on an empty slot."

  def handle_start(self):
    message = self.grab_slot_values("start")
    self.d['message'] = message['message']

  def handle_end(self):
    message = self.grab_slot_values("end")
    self.d['message'] = message['message']

  def handle_current_slot(self):
    slot_type = self.current_player_slot_type()
    if slot_type == SlotType.EVENT:
        self.handle_event()
    elif slot_type == SlotType.EMPTY:
        self.handle_empty_slot()
    elif slot_type == SlotType.START:
        self.handle_start()
    elif slot_type == SlotType.END:
        self.handle_end()
    else:
        raise ValueError(f"Unknown slot type: {slot_type}")

  """Visualization Methods"""
  def get_happiness(self, player):
    return self.d["players"][player].d["happiness"]


def can_move(s, role):
  # Precondition function for the operator: Roll a Dice
  if not s.d['currentPlayer'] == role:
      return False

  s.d['currentRoll'] = r.randint(1, 6)
  for player, state in s.d['players'].items():
      if s.current_position(player) == BOARD_LENGTH - 1:
          return False
  return True

def move(s, role):
  # Transformation function for the operator: Roll a Dice
  news = s.__copy__()
  current_player = news.d['currentPlayer']
  for player, state in news.d['players'].items():
      if player == current_player:
          if (state.d['position'] + s.d['currentRoll']) >= BOARD_LENGTH - 1:
            state.d['position'] = BOARD_LENGTH - 1
          else:
            state.d['position'] += s.d['currentRoll']

  news.handle_current_slot()
  news.d['currentPlayer'] = next_player(news.d['currentPlayer'], )
  return news

SESSION = None

def next_player(k):
  if SESSION==None: return 0 # Roles not ready
  search_count = 0
  while True:
    k = (k + 1) % 2
    #if ROLE_BEING_PLAYED[k]:
    if len((SESSION['ROLES_MEMBERSHIP'])[k])>0:
      return k
    search_count += 1
    if search_count > 2:
      print("Nobody is playing today.\n")
      raise Exception("No players available in function: next_player.")

def is_user_in_role(role_no):
  username = SESSION['USERNAME']
  rm = SESSION['ROLES_MEMBERSHIP']
  if rm==None: return False
  users_in_role = rm[role_no]
  return username in users_in_role

def get_session():
  return SESSION

def goal_message(self):
  self.next_player()
  return f"Congratulations to {self.d['currentPlayer']} for finishing the game!"
#<COMMON_CODE>

#<INITIAL_STATE>
INITIAL_STATE = None
def create_initial_state():
  global INITIAL_STATE
  INITIAL_STATE = State()
  print(INITIAL_STATE)
#</INITIAL_STATE>

#<ROLES>
ROLES = [{'name': 'Player1', 'min': 1, 'max': 1},
         {'name': 'Player2', 'min': 1, 'max': 1},
         {'name': 'Observer', 'min': 0, 'max': 25}
         ]
#</ROLES>

#<OPERATORS>
class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s, role_number=0):
    return self.precond(s, role=role_number)

  def apply(self, s):
    return self.state_transf(s)

OPERATORS = [Operator(
    "Roll a dice: ",
    lambda s, role=0: can_move(s, role),
    lambda s, role=0: move(s, role))]

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
BRIFL_SVG = True
render_state = None
def use_BRIFL_SVG():
  global render_state
  from DisabilitySimulator_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>
