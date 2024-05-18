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
H = 600
THREE_QUARTER_SQW = 3*(HALF_SQW/2)
IMAGE_WIDTH = 200 # Just a guess
IMAGE_HEIGHT = 350 # "   "   "

ROLE_COLOR = [
    "rgb(100, 100, 150)", 
    "rgb(150, 100, 100)", 
    "rgb(150, 150, 150)"] # no-role or observer: darker gray.

# Gradient colors for different slot types
SLOT_GRADIENT_COLORS = {
    SlotType.EMPTY: ["#fce3ae", "#ddb7ab"], # Light Yellow to Light Peach
    SlotType.START: ["#ffb482", "#e5989b"], # Light Orange to Light Pink
    SlotType.END: ["#b0d07e", "#89c4f4"],   # Light Green to Light Blue
    SlotType.EVENT: ["#ffbae1", "#e687c5"], # Light Pink to Pink
}

session = None
def render_state(s, roles=None):
    global session
    session = get_session() # Need HOST and PORT info for accessing images.
    dwg = svgwrite.Drawing(filename = "test-svgwrite.svg",
                           id = "state_svg",  # Must match the id in the html template.
                           size = (str(W)+"px", str(H)+"px"),
                           debug=True)

    if roles==None or roles==[]:
        label = "This player doesn't have any role in the game."
        x = 200; y = 100
        dwg.add(dwg.text(label, insert = (x+HALF_SQW, y+THREE_QUARTER_SQW),
                     text_anchor="middle",
                     font_size="25",
                     fill = "red"))
    else:
        index = 0
        if s.d['currentPlayer'] == "Player1": 
            index = 0
        else: 
            index = 1
        #for role in roles:
        dwg.add(dwg.rect(insert = (0,0),
                     size = (str(W)+"px", str(H)+"px"),
                     stroke_width = "1",
                     stroke = "black",
                     fill = ROLE_COLOR[roles[index]]))

        position = s.current_position(NAMES[roles[(index + 1) % 2]])


        # Define gradients for each SlotType
        for slot_type, colors in SLOT_GRADIENT_COLORS.items():
            gradient_id = "grad_" + slot_type.name
            gradient = dwg.linearGradient((0, 0), (0, 1), id=gradient_id)
            gradient.add_stop_color(0, colors[0])
            gradient.add_stop_color(1, colors[1])
            dwg.defs.add(gradient)

        # Generate the board
        ROWS = 20
        space_width = int(W / ROWS)
        for i in range(BOARD_LENGTH):
            x = i % ROWS * space_width
            y = i // ROWS * space_width
            slot_type = s.d['board'].get(i, SlotType.EMPTY)
            gradient_id = "grad_" + slot_type.name
        
            # Draw the main block with gradient fill
            dwg.add(dwg.rect(insert=(x + 5, y + 75),
                        size=(str(space_width) + "px", str(space_width) + "px"),
                        stroke_width="1",
                        stroke="black",
                        fill="url(#" + gradient_id + ")"))

            # Add board position text
            dwg.add(dwg.text(str(i + 1), insert=(x + 8, y + 75 + 10), fill="black", font_size="8px"))

            # Add a marker at the player's position
            if i == position:
                dwg.add(dwg.circle(center=(x + 5 + space_width/2, y + 75 + space_width/2),
                           r=space_width/4,
                           fill=ROLE_COLOR[index]))  
      
        label = "It is now " + NAMES[roles[index]] + "'s turn."
        x = 350; y = 100
        dwg.add(dwg.text(label, insert = (x+HALF_SQW, y-THREE_QUARTER_SQW),
                     text_anchor="middle",
                     font_size="25",
                     stroke = "black",
                     fill = "black"))  

        # Add legend
        legend_x = 20
        legend_y = 430
        legend_width = 20
        legend_height = 20

        for slot_type, colors in SLOT_GRADIENT_COLORS.items():
            gradient_id = "grad_" + slot_type.name
            legend_rect = dwg.rect(insert=(legend_x, legend_y),
                                size=(str(legend_width) + "px", str(legend_height) + "px"),
                                stroke_width="1",
                                stroke="black",
                                fill="url(#" + gradient_id + ")")
            dwg.add(legend_rect)

            legend_text = dwg.text(slot_type.name,
                                insert=(legend_x + legend_width + 5, legend_y + legend_height / 2),
                                fill="black",
                                font_size="12px")
            dwg.add(legend_text)

            legend_y += legend_height + 5

    svg_string = dwg.tostring()

    #print("svg_string is "); print(svg_string)    return svg_string
    return svg_string

if __name__ == '__main__':
    DEBUG = True
    session = {'HOST': 'tempura.cs.washington.edu', 'PORT':5000}
    INITIAL_STATE = State()
    print(INITIAL_STATE)
    svg_string = render_state(INITIAL_STATE, roles=[0])
    print("svg_string is: ")
    print(svg_string)
