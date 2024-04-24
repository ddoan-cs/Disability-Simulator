'''pre-alpha.py'''

#<METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "Pre-alpha"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Donavan, Jack, Lauren']
PROBLEM_CREATION_DATE = "23-APR-2024"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''This is the pre-alpha version of our disability simulator game.
 It will showcase the general direction of the game without involving 
 the complex storyline. The game will include the most concrete states 
 that do not involve other aspects of the game outside of our main operator: Starting
 and completing a task."
'''
#</METADATA>

#<COMMON_DATA>
import random as rand 
#</COMMON_DATA>

#<COMMON_CODE>
ENERGY=rand.randint(50, 100)
DAYS_LEFT=3
HOURS_LEFT=24
#   "task": (energy, deadline)
DAILY_TASKS = {
    "Get out of bed": (10, 1),
    "Brush your teeth": (5, 1),
    "Eat breakfast": (15, 1)
}

class State():
  def __init__(self, d=None):
    if d==None: 
      d = {'energy': ENERGY,
           'hours': HOURS_LEFT,
           'days': DAYS_LEFT,
           'tasks': [("Get out of bed", False), ("Brush your teeth", False), ("Eat breakfast", False)]
           }
    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True

  def task_to_string(task_name):
    if task_name in DAILY_TASKS:
        return task + ", energy cost: "+ str(task[1]) + "\n"
    
  def __str__(self):
    # Produces a textual description of a state.
    txt = ""
    for prop in self.d.keys():
      if prop == "tasks":
        pass
      txt += prop + " left: " + str(self.d[prop]) + "\n"
    txt += "The remaining tasks are: \n"
    for task in self.d["tasks"]:
      self.task_to_string(task)
      txt += task[0] + ", energy cost: "+ str(task[1]) + "\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for prop in self.d.keys():
      if prop == "tasks":
        pass
      news.d[prop] = self.d[prop]
    news.d['tasks']=[(task[0], task[1]) for task in self.d.tasks]
    return news 

  def can_complete(self, d, task):
    '''Tests whether it's legal to complete the specific task.'''
    side = self.d['ferry'] # Where the ferry is.
    p = self.d['agents']
    if h<1: return False # Need an H to steer boat.
    h_available = p[H][side]
    if h_available < h: return False # Can't take more h's than available
    r_available = p[R][side]
    if r_available < r: return False # Can't take more r's than available
    h_remaining = h_available - h
    r_remaining = r_available - r
    # Humans must not be outnumbered on either side:
    if h_remaining > 0 and h_remaining < r_remaining: return False
    h_at_arrival = p[H][1-side]+h
    r_at_arrival = p[R][1-side]+r
    if h_at_arrival > 0 and h_at_arrival < r_at_arrival: return False
    return True


  def move(self,h,r):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the ferry carrying
     h humans and r robots.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['ferry']        # where is the ferry?
    p = news.d['agents']          # get the array of arrays of agents.
    p[H][side] = p[H][side]-h     # Remove agents from the current side.
    p[R][side] = p[R][side]-r
    p[H][1-side] = p[H][1-side]+h # Add them at the other side.
    p[R][1-side] = p[R][1-side]+r
    news.d['ferry'] = 1-side      # Move the ferry itself.
    return news

  def is_goal(self):
    '''If all Ms and Cs are on the right, then s is a goal state.'''
    p = self.d['agents']
    return (p[H][RIGHT]==3 and p[R][RIGHT]==3)

  def goal_message(self):
    return "Congratulations on successfully guiding the humans and robots across the creek!"

#</COMMON_CODE>

#<OPERATORS>
from soluzion import Basic_Operator as Operator

HR_combinations = [(1,0),(2,0),(3,0),(1,1),(2,1)]

OPERATORS = [Operator(
  "Cross the creek with "+str(h)+" humans and "+str(r)+" robots",
  lambda s, h1=h, r1=r: s.can_move(h1,r1),
  lambda s, h1=h, r1=r: s.move(h1,r1) ) 
  for (h,r) in HR_combinations]
#</OPERATORS>