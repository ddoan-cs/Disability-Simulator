# Author:  Donavan, Lauren, Jack
# Purpose: test svgwrite with the new SOLUZION server and client
# Created: 2024
# Python version 3.x

import svgwrite
from alpha_v2 import * #State,
import alpha_v2

DEBUG = False
W = 850 # Width of Vis. region
SQW = W/8
HALF_SQW = SQW/2
H = 400
THREE_QUARTER_SQW = 3*(HALF_SQW/2)
IMAGE_WIDTH = 200 # Just a guess
IMAGE_HEIGHT = 350 # "   "   "
ROLE_COLOR = [
    "rgb(150, 150, 150)"] # no-role or observer: darker gray.

session = None
def render_state(s, roles=None):
    global session
    #if DEBUG: print("In HalfClue_SVG_VIS_FOR_BRIFL.py, s = "+str(s))
    session = get_session() # Need HOST and PORT info for accessing images.
    dwg = svgwrite.Drawing(filename = "test-svgwrite.svg",
                           id = "state_svg",  # Must match the id in the html template.
                           size = (str(W)+"px", str(H)+"px"),
                           debug=True)

    if roles==None or roles==[]:
      label = "This player doesn't have any role in the game."
      x = 100; y = 100
      dwg.add(dwg.text(label, insert = (x+HALF_SQW, y+THREE_QUARTER_SQW),
                     text_anchor="middle",
                     font_size="25",
                     fill = "red"))
    else:
      yc = 100
      role = roles[0]
      #for role in roles:
         # Background rectangle...
      dwg.add(dwg.rect(insert = (0,0),
                     size = (str(W)+"px", str(H)+"px"),
                     stroke_width = "1",
                     stroke = "black",
                     fill = ROLE_COLOR[role]))

         #y = 100
      print("Rendering for role "+ROLES[0]['name'])


      label = "This is for the role of "+ROLES[0]['name']
      x = 300; y = 100
      dwg.add(dwg.text(label, insert = (x+HALF_SQW, y-THREE_QUARTER_SQW),
                     text_anchor="middle",
                     font_size="25",
                     stroke = "black",
                     fill = "black"))

    render_meter(dwg, 100, 60, 200, 160, 5, 10, "Ballroom.jpg")
    render_task_list(dwg, s, 500, 60)
    svg_string = dwg.tostring()

    #print("svg_string is "); print(svg_string)    return svg_string
    return svg_string

def render_meter(dwg, x, y, width, height, value, max_value, image_filename=None):
    # Calculate the number of filled squares
    filled_squares = int(value / max_value * 8)

    # Define the size of each square and the image size
    square_size = min(width, height) / 8
    image_size = square_size * 1.2

    # Insert the image
    if image_filename:
        dwg.add(dwg.image(image_filename, insert=(x - 20, y + 5), size=(image_size, image_size)))

    # Draw the filled squares
    for i in range(filled_squares):
        dwg.add(dwg.rect(insert=(x + i * square_size, y),
                          size=(square_size, square_size),
                          fill="yellow",
                          stroke="black"))

    # Draw the empty squares
    for i in range(filled_squares, 8):
        dwg.add(dwg.rect(insert=(x + i * square_size, y),
                          size=(square_size, square_size),
                          fill="white",
                          stroke="black"))

def render_task_list(dwg, s, x, y):
    # Renders all tasks not yet completed
    # Need to update for subtasks
    completed_tasks = [task_name for (task_name, completed) in s.d["tasks"] if not completed]
    line_height = 20
    box_width = 200
    box_height = (len(completed_tasks) + 1) * line_height
    dwg.add(dwg.rect(insert=(x, y), size=(box_width, box_height), fill="white", stroke="black"))
    dwg.add(dwg.text("Tasks", insert=(x + 5, y + 15), font_size="20", fill="black"))
    for i, task_name in enumerate(completed_tasks):
        dwg.add(dwg.text(f"{task_name}", insert=(x + 5, y + 35 + i * line_height),
                         font_size="10", fill="black"))

if __name__ == '__main__':
    DEBUG = True
    session = {'HOST': 'localhost', 'PORT':5000}
    INITIAL_STATE = State()
    print(INITIAL_STATE)
    svg_string = render_state(INITIAL_STATE, roles=[0])
    print("svg_string is: ")
    print(svg_string)
