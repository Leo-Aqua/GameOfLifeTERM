import os
import random
from time import sleep
import curses
import json
import sys


#dict

#options_dict = {
#    "fps" : 30,
#    "random_threshold" : 0.7
#}

#jsonified = json.dumps(options_dict, indent=4)

with open("options.txt", "r") as f:
    
    
    
    json_options = json.load(f)
    print(json_options)
    f.close

# Options
random_start = True  # Start with a random dot layout
threshold = json_options["random_threshold"]  # Only allows values between 0 and 1. Higher values give less starting dots
fps = json_options["fps"]


# Variables
refresh_time = 1/fps
term_size_x, term_size_y = os.get_terminal_size()
term_size_x = int(round(term_size_x / 2))
blocks = []



# init 
curses.initscr()
curses.mousemask(1)  # Enable mouse event tracking for button click events
curses.curs_set(0)





# Function to generate a new blocks layout
def generate_blocks(random_blocks:bool = True):
    new_blocks = []
    for row in range(term_size_y):
        rowlist = []
        for char in range(term_size_x):
            if random_blocks == True:
                num = round(random.random(), 3)
            else:
                num = 0
            if num > threshold:
                num = 1
            else:
                num = 0
            rowlist.append(num)
        new_blocks.append(rowlist)
    return new_blocks

# Start with an initial layout

blocks = generate_blocks(random_blocks=False)




def life(i1: int, i2: int, blocks: list):
    blocks[i1][i2] = 1

def death(i1: int, i2: int, blocks: list):
    blocks[i1][i2] = 0

def get_alive_counts(blocks):
    rows = len(blocks)
    cols = len(blocks[0])
    neighbors = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            real_blocks = blocks[i][j]
            neighbor_count = 0

            for x in range(max(0, i - 1), min(rows, i + 2)):
                for y in range(max(0, j - 1), min(cols, j + 2)):
                    if x != i or y != j:
                        neighbor_count += blocks[x][y]

            neighbors[i][j] = neighbor_count

    return neighbors

def gol(blocks):
    rows = len(blocks)
    cols = len(blocks[0])
    new_blocks = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            real_blocks = blocks[i][j]
            neighbor_count = 0

            for x in range(max(0, i - 1), min(rows, i + 2)):
                for y in range(max(0, j - 1), min(cols, j + 2)):
                    if x != i or y != j:
                        neighbor_count += blocks[x][y]

            if neighbor_count == 3 and real_blocks == 0:
                new_blocks[i][j] = 1
            
            elif neighbor_count < 2 and real_blocks == 1:
                new_blocks[i][j] = 0
            
            elif (neighbor_count == 2 or neighbor_count == 3) and real_blocks == 1:
                new_blocks[i][j] = 1
            elif neighbor_count > 3 and real_blocks == 1:
                new_blocks[i][j] = 0

    return new_blocks


def draw_cells(window):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 165, -1) # Violett # https://i.stack.imgur.com/7AtMc.png
    curses.init_pair(2, 83, -1) # Lime green
    curses.init_pair(3, 197, -1) # red
    curses.init_pair(4, 87, -1) # cyan
    curses.init_pair(5,-1,-1)
    global blocks
    global threshold
    window.addstr(3, 43, "OFF", curses.color_pair(3))
    

    random_mode = False
    while True:
        window.addstr(1, 1, "Draw cells!", curses.color_pair(1))
        window.addstr(2, 1, "Press ", curses.color_pair(1))
        window.addstr(2, 7, "'SPACE'", curses.color_pair(4))
        window.addstr(2, 14, " to run the simulation.", curses.color_pair(1))
        window.addstr(3, 1, """Press """, curses.color_pair(1))
        window.addstr(3, 7, "'R'", curses.color_pair(4))
        window.addstr(3, 10, """ to toggle random mode! Current: """, curses.color_pair(1))

        

        key = window.getch()
        if key == ord('r'):
            window.addstr(3,43,"    ")
            if random_mode == True:
                random_mode = False
                window.clear()
                window.addstr(3, 43, "OFF", curses.color_pair(3))
                blocks = generate_blocks(False)
                
            elif random_mode == False:
                random_mode = True
                
                blocks = generate_blocks()
                
                for y, row in enumerate(blocks):
                    for x, pixel in enumerate(row):
                        if pixel == 1:
                            # Set the color pair and display the pixel
                            window.attron(curses.color_pair(5))
                            try:
                                # Adjust X-coordinate to skip every other character
                                window.addstr(y, x * 2, "██")
                            except curses.error:
                                pass  # Ignore errors if the position is out of bounds
                            window.attroff(curses.color_pair(5))
                window.addstr(3, 43, "ON", curses.color_pair(2))
        
            
        if key == ord(' '):
            break
        if key == curses.KEY_MOUSE:
            _, mouse_x, mouse_y, _, _ = curses.getmouse()  # Get mouse event details
            if mouse_x >= 0 and mouse_y >= 0 and not mouse_x % 2 and not random_mode:
                window.addstr(mouse_y, mouse_x, "██")  # Place an 'X' at the clicked position
                mouse_x_even = mouse_x
                row_index = mouse_y
                col_index = mouse_x_even // 2  # Convert even X coordinate to column index

                # Update the blocks list
                while len(blocks) <= row_index:
                    blocks.append([])  # Add new rows as needed

                if len(blocks[row_index]) <= col_index:
                    blocks[row_index].extend([0] * (col_index - len(blocks[row_index]) + 1))
                blocks[row_index][col_index] = 1

                window.refresh()
                sleep(0.01)


        

    

# Define the draw_pixel function
def draw_pixel(window):
    global blocks  # Declare 'blocks' as a global variable
    

    

    while True:
        for y, row in enumerate(blocks):
            for x, pixel in enumerate(row):
                if pixel == 1:
                    # Set the color pair and display the pixel
                    window.attron(curses.color_pair(1))
                    try:
                        # Adjust X-coordinate to skip every other character
                        window.addstr(y, x * 2, "██")
                    except curses.error:
                        pass  # Ignore errors if the position is out of bounds
                    window.attroff(curses.color_pair(1))
        window.addstr(1, 1, """Press "Ctrl+C" to quit""")
        
        window.refresh()
        sleep(refresh_time)

        # Update the blocks list with a new layout
        blocks = gol(blocks)
        window.clear()



# Initialize curses
try:
    curses.wrapper(draw_cells) 
    curses.wrapper(draw_pixel) 
except KeyboardInterrupt:
    sys.exit(0)