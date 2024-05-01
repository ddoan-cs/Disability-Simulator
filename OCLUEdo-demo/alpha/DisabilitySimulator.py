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

import random as r; 
#<COMMON_DATA>
ENERGY=r.randint(50, 100)
ACCOMMODATION=0
HAPPINESS=50
HOURS_LEFT=24

# Days left is still undecided. 
# Should cover mostly major events/tasks. 
DAYS_LEFT=3

# "task": (uniqueid, energy cost , deadline, prereq tasks)
# daily task uniqueid is just day the tasks will appear 
# major task uniqueid is just task + i where i is the task number
# Not using the deadline yet
TASKS = {
    # Daily Tasks 
    "Get out of bed": (10, 1, None),
    "Brush your teeth": (5, 1, None),
    "Eat breakfast": (15, 1, None),

    # Major Events 
    "Schedule a Doctor's Appointment": (10, 1, None),
    "Go to the doctor": (10, 1, ["Schedule a Doctor's Appointment"]),

    #"Request Accommodations": ("accommodation1", 10, 1, None) 
}

#</COMMON_DATA>

#<COMMON_CODE>
DEBUG=True

class State():
  def __init__(self, d=None):
    if d==None: 
      d = {'energy': ENERGY,
           'hours': HOURS_LEFT,
           'days': DAYS_LEFT,
           'tasks': [("Get out of bed", False), ("Brush your teeth", False), 
                     ("Eat breakfast", False), ("Schedule a Doctor's Appointment", False), ("Go to the doctor", False)], 
           'accommodations': ACCOMMODATION, 
           'happiness': HAPPINESS
          }
    self.d = d

  def __eq__(self,s2):
    for prop in self.d.keys():
      if self.d[prop] != s2.d[prop]: return False
    return True
  
  def get_task_info(self, task_name):
    if task_name in TASKS:
      task_info = TASKS[task_name]
    return task_info

  def task_to_string(self, task_name):
    txt = None
    task_info = self.get_task_info(task_name)
    txt = task_name + ", energy cost: "+ str(task_info[0]) + "\n"
    return txt
  
  def __str__(self):
    # Produces a textual description of a state.
    txt = "\n \n"
    for prop in self.d.keys():
      if prop == "tasks":
        continue
      txt += prop + " left: " + str(self.d[prop]) + "|"
    remaining =""
    finished = ""
    for task in self.d["tasks"]:
      if task[1]:
        finished += self.task_to_string(task[0])
      else:
        remaining += self.task_to_string(task[0])
    txt += "\n The remaining tasks are: \n" + remaining + "The finished tasks are: \n" + finished
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def __copy__(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    for prop in self.d.keys():
      if prop == "tasks":
        pass
      news.d[prop] = self.d[prop]
    news.d['tasks']=[(task[0], task[1]) for task in self.d["tasks"]]
    return news 

  def task_index(self, task):
    for (i, t) in enumerate(self.d["tasks"]):
      if t[0] == task:
        return i

  def can_complete(self, task):
    task_info = self.get_task_info(task)
    energy_cost = task_info[0]
    task_index = self.task_index(task)

    # Check if all prerequisites are completed
    if task_info[2]:
        for prereq_task_name in task_info[2]:
            prereq_task_index = self.task_index(prereq_task_name)
            if not self.d["tasks"][prereq_task_index][1]:
                return False

    return self.d["energy"] - energy_cost >= 0 and not self.d["tasks"][task_index][1]


  def complete(self, task):
    news = self.__copy__()      # start with a deep copy.
    task_info = self.get_task_info(task)
    news.d["energy"] = news.d["energy"] + task_info[0] + news.d["accommodations"]
    task_index = self.task_index(task)
    news.d["tasks"][task_index] = (self.d["tasks"][task_index][0], True)
    return news

  def sleep(self): 
    news = State()
    news.d["energy"] = self.d["energy"] + 20
    news.d["days"] = self.d["days"] - 1
    return news

  def is_goal(self):
    return self.d["days"] == 0

  def goal_message(self):
    return "Congratulations on successfully finishing the first three days of your simulation!"
  
SESSION = None
INACTIVE_PLAYERS = None 

def next_player(k, inactive_ok=False):
  if SESSION==None: return 0 # Roles not ready
  search_count = 0
  while True:
    k = (k + 1) % 6
    #if ROLE_BEING_PLAYED[k]:
    if len((SESSION['ROLES_MEMBERSHIP'])[k])>0:
      if k in INACTIVE_PLAYERS:
        if inactive_ok: return k
      else: return k
    search_count += 1
    if search_count < 1:
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
#</COMMON_CODE>

#<OPERATORS>  #---------------------
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
  "Completing task: " + task,
  lambda s, role=0, task1=task: s.can_complete(task1),
  lambda s, role=0, task1=task: s.complete(task1) ) 
  for task in TASKS.keys()]

OPERATORS += [Operator("Sleeping", 
  lambda s, role=0: True,
  lambda s, role=0: s.sleep())]
                      
if DEBUG:
  print("All operators:")
  for o in OPERATORS:
    print(o.name)
#</OPERATORS>

#<INITIAL_STATE>
INITIAL_STATE = None

def create_initial_state():
  global INITIAL_STATE
  INITIAL_STATE = State()
  print(INITIAL_STATE)
#</INITIAL_STATE>

#<ROLES>
ROLES = [ {'name': 'Student', 'min': 1, 'max': 1}]
#</ROLES>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
BRIFL_SVG = True # The program FoxAndGeese_SVG_VIS_FOR_BRIFL.py is available
render_state = None
def use_BRIFL_SVG():
  global render_state
  from  DisabilitySimulator_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>


