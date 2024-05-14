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
BOARD_LENGTH = 24
from enum import Enum

class SlotType(Enum):
    EVENT = "event"

    #TODO What is the purpose of empty slots if we do not have energy?
    EMPTY = "empty"

    #TODO Need to figure out how to show starting and ending messages if they are unique.
    # Should consider this when moving to the FLASK client.
    START = "start"
    END = "end"

# This represents a 24-space game board.
POSITIONS = {
    0: SlotType.START,
    1: SlotType.EMPTY,
    2: SlotType.EMPTY,
    3: SlotType.EVENT,
    4: SlotType.EVENT,
    5: SlotType.EMPTY,
    6: SlotType.EMPTY,
    7: SlotType.EVENT,
    8: SlotType.EVENT,
    9: SlotType.EVENT,
    10: SlotType.EVENT,
    11: SlotType.EMPTY,
    12: SlotType.EVENT,
    13: SlotType.EMPTY,
    14: SlotType.EVENT,
    15: SlotType.EVENT,
    16: SlotType.EMPTY,
    17: SlotType.EVENT,
    18: SlotType.EMPTY,
    19: SlotType.EVENT,
    20: SlotType.EVENT,
    21: SlotType.EVENT,
    22: SlotType.EMPTY,
    23: SlotType.EMPTY,
    24: SlotType.END
}

"""Slot Values"""
SLOTS = {
    # TODO Need to come up with the exact details of events: scope, type, etc.
    # Slot = {
    #        0: {“message in slot”,  “(metric, cost)”, }
    #        }


    # Positive Events
    0: {"type": "positive", "message": "You were able to schedule a doctor's appointment.", "cost": ("Happiness", 10)},
    1: {"type": "positive", "message": "You were able to cook breakfast.", "cost": ("Position", 2)},

    # Negative Events
    2: {"type": "negative", "message": "You were not able to rest", "cost": ("Happiness", -10)},
    3: {"type": "negative", "message": "Your symptoms got worse.", "cost": ("Position", -2)},

    # Start
    4: {"type": "start", "message": "You have just started your last month of university when you have suddenly developed symptoms of some unknown cause.", "cost": None},

    # End
    55: {"type": "end", "message": "You were able to finish your last month and graduate!", "cost": None}
}
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

#<INITIAL_STATE>
INITIAL_STATE = None
import random


def create_initial_state():
  global INITIAL_STATE
  # setup()
  INITIAL_STATE = State()
  print(INITIAL_STATE)
#</INITIAL_STATE>

class State():
  """Represents the state of the game.

    Each State instance includes properties such as the current player, the game board layout,
    player states (including their happiness, position, and disability status),
    the current message for the player, and the result of the last dice roll.

    Methods:
    - __init__(self, d=None): Initializes a State instance with default values if no dictionary is provided.
    - __eq__(self, s2): Compares two State instances for equality based on their property values.
    - __str__(self): Returns a textual description of a State instance.
    - __hash__(self): Generates a hash value for a State instance.
    - __copy__(self): Creates a deep copy of a State instance.
    - can_move(self): Precondition function for the operator: Roll a Dice.
    - move(self): Transformation function for the operator: Roll a Dice.
    - next_player(self): Updates the state to the next player.
    - current_player_slot_type(self): Finds the slot type the current player is on.
    - current_position(self): Finds the current position of the current player.
    - has_disability(self): Checks if the current player has a disability.
    - grab_slot_values(self, slot_type): Grabs the values of the slots.
    - handle_event(self): Handles the event based on the current player's disability status.
    - handle_empty_slot(self): Handles an empty slot.
    - handle_start(self): Handles the start slot.
    - handle_end(self): Handles the end slot.
    - handle_current_slot(self): Handles the current slot the player is on.
    - is_goal(self): Checks if any player has reached the goal position.
    - goal_message(self): Generates a message for the winning player.
  """
  def __init__(self, d=None):
    if d==None:
        players_states = {f"Player{i+1}": PlayerState(f"Player{i+1}") for i in range(2)}

        d = {'currentPlayer' : "Player1",
           'board' : POSITIONS,
           'players' : players_states,
           'message' : "",
           'currentRoll' : None
        }

    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.

    txt = "\n"
    # Case 1: When it is the next player's turn.
    if self.d['currentRoll'] is not None:
        txt += "You rolled a " + str(self.d['currentRoll']) + ".\n"
        txt += str(self.d['message']) + "\n"
        for player_name, player_state in self.d["players"].items():
            if self.d['currentPlayer'] != player_name:
                txt += "You now have " + str(player_state.d['happiness']) + " happiness "
                txt += "and are at position " + str(player_state.d['position']) + " on the board \n \n"
        txt += "It is now " + str(self.d['currentPlayer']) + "'s turn. \n"
    else:
       # Case 2: When there is no previous player
       txt += "It is " + str(self.d['currentPlayer']) + "'s turn. \n"
       for player_name, player_state in self.d["players"].items():
            if self.d['currentPlayer'] == player_name:
                txt += "You have " + str(player_state.d['happiness']) + " happiness "
                txt += "and are at position " + str(player_state.d['position']) + " on the board \n \n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def __copy__(self):
    # Copies the state and returns the newly created copy.
    news = State({})
    for prop in self.d.keys():
        news.d[prop] = self.d[prop]
    return news

  def can_move(self):
    # Precondition function for the operator: Roll a Dice
    self.d['currentRoll'] = r.randint(1, 6)
    return True

  def move(self):
    # Transformation function for the operator: Roll a Dice
    news = self.__copy__()
    current_player = news.d['currentPlayer']
    for player, state in news.d['players'].items():
        if player == current_player:
            if (state.d['position'] + self.d['currentRoll']) >= BOARD_LENGTH:
               state.d['position'] = BOARD_LENGTH
            else:
               state.d['position'] += self.d['currentRoll']

    news.handle_current_slot()
    news.next_player()
    return news

  def next_player(self):
    # Updates the state to the next player.
    current_player_idx = 0
    for player, state in self.d['players'].items():
        if player == self.d['currentPlayer']:
            break
        current_player_idx += 1

    next_player_idx = (current_player_idx + 1) % 2
    self.d['currentPlayer'] =  list(self.d['players'].keys())[next_player_idx]

  def current_player_slot_type(self):
    # Finds the slot type the current player is on.
    player_position = self.current_position()
    slot_type = self.d['board'][player_position]
    return slot_type

  # Should probably move these methods into PlayerState.
  def current_position(self):
    # Finds the current position of the current player.
    current_player = self.d['currentPlayer']
    return self.d['players'][current_player].d['position']

  def has_disability(self):
    # Finds the current position of the current player.
    current_player = self.d['currentPlayer']
    return self.d['players'][current_player].d['disability']

  def grab_slot_values(self, slot_type):
    # Grabs the values of the slots: message
    for event_id in range(len(SLOTS)):
        event = SLOTS.get(event_id)
        if event and event["type"] == slot_type:
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

    # Updates the current state using the grabbed message.
    if message['cost'][0] == 'happiness':
        self.d["players"][current_player].d["happiness"] += message['cost'][1]
    else:
        new_position = self.d["players"][current_player].d["position"] + message['cost'][1]
        if new_position < 0:
           self.d["players"][current_player].d["position"] = 0
        elif new_position > BOARD_LENGTH:
           self.d["players"][current_player].d["position"] = BOARD_LENGTH
        else:
           self.d["players"][current_player].d["position"] = new_position

  def handle_empty_slot(self):
    # TODO
    self.d['message'] = "You landed on an empty slot."

  def handle_start(self):
    self.d['message'] = self.grab_slot_values("start")

  def handle_end(self):
    self.d['message'] = self.grab_slot_values("end")

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

  def is_goal(self):
    return any(player_state.d["position"] == BOARD_LENGTH for player_state in self.d["players"].values())

  # Since the current player is advanced on the operator, the winner should be the previous player.
  def goal_message(self):
    self.next_player()
    return f"Congratulations to {self.d['currentPlayer']} for finishing the game!"

#<COMMON_CODE>

#<ROLES>
ROLES = [{'name': 'Disabled', 'min': 1, 'max': 1},
         {'name': 'Able-Bodied', 'min': 1, 'max': 1},
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
    lambda s: s.can_move(),
    lambda s: s.move())]

#</OPERATORS>

#<STATE_VIS>
BRIFL_SVG = True # The program FoxAndGeese_SVG_VIS_FOR_BRIFL.py is available
render_state = None
def use_BRIFL_SVG():
  global render_state
  from  DisabilitySimulator_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>
