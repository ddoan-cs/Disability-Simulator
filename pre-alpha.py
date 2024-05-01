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
# "task": (energy, deadline)
# Not using the deadline yet
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
  
  def get_task_info(self, task_name):
    if task_name in DAILY_TASKS:
      task_info = DAILY_TASKS[task_name]
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
      txt += prop + " left: " + str(self.d[prop]) + "\n"
    remaining =""
    finished = ""
    for task in self.d["tasks"]:
      if task[1]:
        finished += self.task_to_string(task[0])
      else:
        remaining += self.task_to_string(task[0])
    txt += "\nThe remaining tasks are: \n" + remaining + "The finished tasks are: \n" + finished
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
    news.d['tasks']=[(task[0], task[1]) for task in self.d["tasks"]]
    return news 

  def task_index(self, task):
    for (i, t) in enumerate(self.d["tasks"]):
      if t[0] == task:
        return i

  def can_complete(self, task):
    task_info = self.get_task_info(task)
    engery_cost = task_info[0]
    task_index = self.task_index(task)
    return self.d["energy"] - engery_cost >= 0 and not self.d["tasks"][task_index][1]

  def complete(self, task):
    news = self.copy()      # start with a deep copy.
    task_info = self.get_task_info(task)
    news.d["energy"] -= task_info[0]
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

#</COMMON_CODE>

#<OPERATORS>
from soluzion import Basic_Operator as Operator

OPERATORS = [Operator(
  "Completing task: " + task,
  lambda s, task1=task: s.can_complete(task1),
  lambda s, task1=task: s.complete(task1) ) 
  for task in DAILY_TASKS.keys()]

OPERATORS += [Operator("Sleeping", lambda s: True,lambda s: s.sleep())]
#</OPERATORS>