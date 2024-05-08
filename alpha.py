'''alpha.py
("The Cards Half of the game of 'Clue'")
A SOLUZION problem formulation, for ZZ003.py.

Incorporating "accusations" as of April 8.
a. Add an "accusation_phase" variable to states.
b. Add a "current_accusation" variable to states.
c. Add operators analogous to the suggestion operators,
 but for accusations.
d. Update the vis to show 
    i. accusation in progress (but not what it is).
    ii. results of the accusation, followed by
          acknowledge end of turn, if wrong;
          or END OF GAME, if correct.
    iii. if any passive players, a list of them.
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
 '''This is the alpha version of our disability simulator game.
 It will showcase the general direction of the game focusing on a couple of the first 
 major events in the storyline. The game will include the most concrete states 
 that do not involve other aspects of the game outside of our main operator: Starting
 and completing a task.

'''
#</METADATA>

#<COMMON_DATA>
"""Disabilities""" 
DISABILITIES = [
    ("mobility", ["Chronic Pain", "Amputation"]),
    ("visual", ["Blindness", "Color Blindness"]),
    ("hearing", ["Deafness", "Tinnitus"])
]

"""Game Metrics"""
import random as r; 

ENERGY=r.randint(50, 100)
GRADES=r.uniform(2.0, 4.0) 
ACCOMMODATION=0
HAPPINESS=50


"""Board""" 
BOARD_LENGTH = 20
from enum import Enum

class SlotType(Enum):
    POSITIVE_EVENT = "positive"
    NEGATIVE_EVENT = "negative"
    EMPTY = "empty"
    BRANCH = "branch" 
    START = "start"
    END = "end"
    SPECIAL = "special"
    VARIABLE = "variable"

POSITIONS = {
    0: SlotType.START,
    1: SlotType.EMPTY,
    2: SlotType.EMPTY,
    3: SlotType.POSITIVE_EVENT,
    4: SlotType.NEGATIVE_EVENT,
    5: SlotType.EMPTY,
    6: SlotType.EMPTY,
    7: SlotType.NEGATIVE_EVENT,
    8: SlotType.POSITIVE_EVENT,
    9: SlotType.BRANCH,

    # First Branch 
    10: SlotType.POSITIVE_EVENT,
    11: SlotType.EMPTY,
    12: SlotType.POSITIVE_EVENT,
    13: SlotType.EMPTY,
    14: SlotType.POSITIVE_EVENT,

    # Second Branch
    15: SlotType.NEGATIVE_EVENT,
    16: SlotType.EMPTY,
    17: SlotType.NEGATIVE_EVENT,
    18: SlotType.EMPTY,
    19: SlotType.NEGATIVE_EVENT,

    20: SlotType.NEGATIVE_EVENT,
    21: SlotType.POSITIVE_EVENT,
    22: SlotType.EMPTY,
    23: SlotType.EMPTY,
    24: SlotType.END 
}

"""Slot Values"""
SLOTS = {
    # position_req is the range of where any specific slot can appear

    # Positive Events
    0: {"type": "positive", "message": "You were able to schedule a doctor's appointment.", "position_req": (0, 8)},
    1: {"type": "positive", "message": "You received support from a friend or family member.", "position_req": (0, 8)},
    2: {"type": "positive", "message": "You accomplished a personal goal.", "position_req": (1, 23)},

    3: {"type": "positive", "message": "You made progress in your studies/work despite challenges.", "position_req": (10, 14)},
    4: {"type": "positive", "message": "You had a pleasant social interaction.", "position_req": (10, 14)},
    5: {"type": "positive", "message": "You participated in a fun and fulfilling activity.", "position_req": (10, 14)},

    # Negative Events
    6: {"type": "negative", "message": "You experienced a flare-up of symptoms.", "position_req": (0, 8)},
    7: {"type": "negative", "message": "You had trouble sleeping last night.", "position_req": (1, 23)},
    8: {"type": "negative", "message": "You encountered accessibility barriers in public.", "position_req": (0, 8)},

    9: {"type": "negative", "message": "You faced discrimination due to your disability.", "position_req": (15, 19)},
    10: {"type": "negative", "message": "You missed an important appointment.", "position_req": (15, 19)},
    11: {"type": "negative", "message": "You struggled with daily tasks.", "position_req": (15, 19)},

    # Special Events
    12: {"type": "special", "message": "You had a pair study session. ", "position_req": (1, 23)},

    # Empty
    #14: {"type": "empty", "message": "You decided to take a shower.", "position_req": (1, 1)},
    #15: {"type": "empty", "message": "You were able to eat breakfast.", "position_req": (2, 2)},
    #16: {"type": "empty", "message": "You cooked a meal today.", "position_req": (5, 5)},
    #17: {"type": "empty", "message": "You did laundry today.", "position_req": (6, 6)},
    #18: {"type": "empty", "message": "You cleaned your room.", "position_req": (11, 11)},
    #19: {"type": "empty", "message": "You went grocery shopping.", "position_req": (13, 13)},
    #20: {"type": "empty", "message": "You exercised today.", "position_req": (16, 16)},
    #21: {"type": "empty", "message": "You attended a social event.", "position_req": (18, 18)},
    #22: {"type": "empty", "message": "You completed an assignment.", "position_req": (22, 22)},
    #23: {"type": "empty", "message": "You cooked a meal today.", "position_req": (23, 23)},

    # Branch
    13: {"type": "branch", "message": "You just had your first test. \n", "position_req": (9, 9)},

    # Start
    14: {"type": "start", "message": "You have just started your last month of university when you have suddenly developed symptoms of some unknown cause.", "position_req": (0, 0)},

    # End
    15: {"type": "end", "message": "You were able to finish your last month and graduate!",  "position_req": (24, 24)}
}
#</COMMON_DATA>

#<COMMON_CODE>
class PlayerState(): 
  def __init__(self, player_name, d=None):
    if d==None: 
      d = {'energy': ENERGY, 
           'accommodations': ACCOMMODATION, 
           'happiness': HAPPINESS, 
           'grades' : GRADES,
           'playerName' : player_name,
           'disability' : DISABILITIES[r.randint(0, 2)], 
           'position' : 0
          }
      
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
  def __init__(self, d=None):
    if d==None: 
        players_states = {f"Player{i+1}": PlayerState(f"Player{i+1}") for i in range(4)}

        d = {'currentPlayer' : "Player1", 
           'board' : POSITIONS, 
           'players' : players_states, 
           'message' : "", 
           'currentRoll' : 0
        }
      
    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True
  
  def __str__(self):
    # Produces a textual description of a state.
    txt = "\n" 
    for prop in self.d.keys():
      if prop == 'board' or prop == 'players': 
        continue
      txt += prop + " is " + str(self.d[prop]) + "\n"
    for player_name, player_state in self.d["players"].items():
      if self.d['currentPlayer'] == player_name: 
        txt += str(player_state)
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
  
  def can_move(self):
    self.d['currentRoll'] = r.randint(1, 6)
    current_player = self.d['currentPlayer']
    for player, state in self.d['players'].items():
        if player == current_player:
            return (state.d['position'] + self.d['currentRoll']) < BOARD_LENGTH
        
    return False

  def move(self):
    news = self.__copy__()
    current_player = news.d['currentPlayer']
    for player, state in news.d['players'].items():
        if player == current_player:
            state.d['position'] += self.d['currentRoll']

    share, player_name = news.on_same_position()
    if share: 
        news.handle_special(player_name)
    else: 
        news.handle_current_slot()

    news.next_player()
    return news

  def next_player(self):
    current_player_idx = 0
    for player, state in self.d['players'].items():
        if player == self.d['currentPlayer']:
            break
        current_player_idx += 1

    next_player_idx = (current_player_idx + 1) % 4
    self.d['currentPlayer'] =  list(self.d['players'].keys())[next_player_idx]

  def current_player_slot_type(self):
    player_position = self.current_position()
    slot_type = self.d['board'][player_position]
    return slot_type
  
  def on_same_position(self): 
    share = False 
    shared_player = None
    current_player = self.d['currentPlayer']
    current_position = self.current_position()
    for player, state in self.d['players'].items():
        if player != current_player and current_position != 0 and state.d['position'] == current_position:
            share = True
            shared_player = player
            break

    return share, shared_player

  
  def current_position(self): 
    current_player = self.d['currentPlayer']
    return self.d['players'][current_player].d['position']
    
  def grab_slot_values(self, slot_type): 
    for event_id in range(len(SLOTS)):
        event = SLOTS.get(event_id)
        if event and event["type"] == slot_type and self.current_position() in range(*event["position_req"]):
            return event['message']
    return ""
  
  def handle_positive_event(self):
    self.d['message'] = self.grab_slot_values("positive")
        
  def handle_negative_event(self): 
    self.d['message'] = self.grab_slot_values("negative")

  def handle_empty_slot(self):
    # Empty slots return a variable amount of energy to the player
    current_player = self.d['currentPlayer']
    energy_gain = r.randint(5, 20) 
    self.d["players"][current_player].d["energy"] += energy_gain

    return ""

  def handle_branch(self):
    self.d['message'] = self.grab_slot_values("branch")

    if self.d["energy"] < 30 and self.d["happiness"] < 50: 
        self.d["grades"] -= 0.5
        self.d['message'] += "You crammed soo much that you got anxious and failed your test."
    else:
        self.d["grades"] += 0.5
        self.d['message'] += "You aced your test."

  def handle_start(self):
    self.d['message'] = self.grab_slot_values("start")
  
  def handle_end(self):
    self.d['message'] = self.grab_slot_values("end")
  
  def handle_special(self, other): 
    self.d['message'] = self.grab_slot_values("special")

    current_player = self.d["currentPlayer"]
    self.d["players"][current_player].d["happiness"] += 5 
    self.d["players"][current_player].d["grades"] += 0.5 
    self.d["players"][other].d["happiness"] += 5 
    self.d["players"][other].d["grades"] += 0.5    

  def handle_current_slot(self):
    slot_type = self.current_player_slot_type()
    if slot_type == SlotType.POSITIVE_EVENT:
        self.handle_positive_event()
    elif slot_type == SlotType.NEGATIVE_EVENT:
        self.handle_negative_event()
    elif slot_type == SlotType.EMPTY:
        self.handle_empty_slot()
    elif slot_type == SlotType.BRANCH:
        self.handle_branch()
    elif slot_type == SlotType.START:
        self.handle_start()
    elif slot_type == SlotType.END:
        self.handle_end()
    else:
        raise ValueError(f"Unknown slot type: {slot_type}")

  def is_goal(self):
    return any(player_state.d["position"] >= BOARD_LENGTH for player_state in self.d["players"].values())


  def goal_message(self):
    return f"Congratulations to {self.d['currentPlayer']} for finishing the game!"

#<COMMON_CODE>
  
#<OPERATORS>
from soluzion import Basic_Operator as Operator

OPERATORS = [Operator(
    "Roll a dice: ",
    lambda s: s.can_move(),
    lambda s: s.move())]

#</OPERATORS>
                      