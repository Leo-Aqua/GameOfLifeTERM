import os
import random
from time import sleep
import curses
import sys


#dict

#options_dict = {
#    "fps" : 30,
#    "random_threshold" : 0.7
#}

#jsonified = json.dumps(options_dict, indent=4)




global fps
# Options
threshold = .7  # Only allows values between 0 and 1. Higher values give less starting dots



# Variables

term_size_x, term_size_y = os.get_terminal_size()
term_size_x = int(round(term_size_x / 2))
blocks = []



# init 
curses.initscr()
curses.mousemask(1)  # Enable mouse event tracking for button click events
curses.curs_set(0)
sys.stdout.write("\x1b]2;%s\x07" % "Game of life")




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


import curses

def set_console_title(title):
    curses.setupterm()
    tsl_seq = (curses.tigetstr('tsl') or b'\x1b[1;1f\x1b[J').decode('utf-8')  # Decode bytes to a string
    sys.stdout.write(tsl_seq)
    sys.stdout.write(f"\033]0;{title}\007")
    sys.stdout.flush()

set_console_title("Game of life")



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
    
    window.nodelay(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 165, -1) # Violett # https://i.stack.imgur.com/7AtMc.png
    curses.init_pair(2, 83, -1) # Lime green
    curses.init_pair(3, 197, -1) # red
    curses.init_pair(4, 87, -1) # cyan
    curses.init_pair(5,-1,-1) # reset
    #curses.init_pair(6, curses.COLOR_BLACK, 87) #select
    global blocks
    global threshold
    global fps
    global refresh_time
    global term_size_x
    global term_size_y
    fps=30
    
    window.addstr(3, 30, "OFF", curses.color_pair(3))
    window.addstr(6, 7, "Draw ", curses.color_pair(4))
    window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
    window.addstr(4, 19, str(threshold) + " ", curses.color_pair(4))
    window.addstr(7, 13, str(term_size_x) + "x" + str(term_size_y), curses.color_pair(4))
    active_tool = "draw"
    option_cursor = 0
    random_mode = False
    while True:
        curses.update_lines_cols()
        term_size_y, term_size_x = window.getmaxyx()

        window.addstr(7, 13, str(term_size_x) + "x" + str(term_size_y), curses.color_pair(4))
          
        window.addstr(1, 1, "Draw cells!", curses.color_pair(1))
        if option_cursor == 0:
            window.addstr(2, 1, "R", curses.color_pair(2) | curses.A_BLINK | curses.A_UNDERLINE)
            window.addstr(2, 2, "un simulation", curses.color_pair(2) | curses.A_BLINK)
        else:
            window.addstr(2, 1, "R", curses.color_pair(2) | curses.A_UNDERLINE)
            window.addstr(2, 2, "un simulation", curses.color_pair(2))


        
        if option_cursor == 1:
            
            window.addstr(3, 1, """Toggle random mode! Current:""", curses.color_pair(1) | curses.A_BLINK)
        else:
            window.addstr(3, 1, """Toggle random mode! Current:""", curses.color_pair(1))

        if option_cursor == 2:
            
            window.addstr(4, 1, """Random threshold:""", curses.color_pair(1) | curses.A_BLINK)
        else:
            window.addstr(4, 1, """Random threshold:""", curses.color_pair(1))

        if option_cursor == 3:
            
            window.addstr(5, 1, """FPS:""", curses.color_pair(1) | curses.A_BLINK)
        else:
            window.addstr(5, 1, """FPS:""", curses.color_pair(1))


        if option_cursor == 4:
            window.addstr(6, 1, """T""", curses.color_pair(1) | curses.A_BLINK | curses.A_UNDERLINE)
            window.addstr(6, 2, """ool: """, curses.color_pair(1) | curses.A_BLINK)

        else:
            window.addstr(6, 2, """ool: """, curses.color_pair(1))
            window.addstr(6, 1, """T""", curses.color_pair(1) | curses.A_UNDERLINE)
        
        
            
        
        window.addstr(7, 1, """Resolution:""", curses.color_pair(1))
        

        

        key = window.getch()
        
            
        if key == curses.KEY_DOWN:
            option_cursor += 1
        elif key == curses.KEY_UP:
            option_cursor -=1
        
        if option_cursor < 0:
            option_cursor = 0
        if option_cursor > 4:
            option_cursor = 4

        if key == ord("\n") and option_cursor == 0 or key == ord("r"): ## start sim
            break

        if key == ord("\n") and option_cursor == 1: ## toggle random mode
            window.addstr(3,30,"    ")
            if random_mode == True:
                random_mode = False
                window.clear()
                window.addstr(3, 30, " OFF", curses.color_pair(3))
                window.addstr(4, 19, str(threshold) + "  ", curses.color_pair(4))
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
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
                window.addstr(3, 30, " ON", curses.color_pair(2))
                window.addstr(4, 19, str(threshold) + "  ", curses.color_pair(4))
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
        
        if option_cursor == 2: #random threshold
            if key == curses.KEY_RIGHT: 
            
                threshold += .1
                threshold = round(threshold, 2)
                if threshold >= 1:
                    threshold = 1
                
                window.clear()
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
                window.addstr(3, 30, " ON", curses.color_pair(2))
                window.addstr(4, 19, str(threshold) + "  ", curses.color_pair(4))
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
                random_mode = True
                      
                
            if key == curses.KEY_LEFT:
            
                threshold -= .1
                threshold = round(threshold, 2)
                if threshold <= 0:
                    threshold = 0
                
                window.clear()
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
                window.addstr(3, 30, " ON", curses.color_pair(2))
                window.addstr(4, 19, str(threshold) + "  ", curses.color_pair(4))
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
                random_mode = True
                
        if option_cursor == 3: ## fps
            if key == curses.KEY_RIGHT: ## fps +
            
                fps += 1
                
                if fps > 1000:
                    fps = 1000
                window.refresh()
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
                
                
            if key == curses.KEY_LEFT: ## fps -
            
                fps -= 1
                
                if fps < 1:
                    fps = 1
                window.refresh()
                window.addstr(5, 6, str(fps) + "  ", curses.color_pair(4))
                
                
            global refresh_time
            refresh_time = 1/fps
        
        if key == ord("\n") and option_cursor == 4 or key == ord("t"): ## toggle draw/erase mode
            
            
            if active_tool == "erase":
                active_tool = "draw"
                window.addstr(6, 7, "Draw ", curses.color_pair(4))
            elif active_tool == "draw":
                active_tool = "erase"
                window.addstr(6, 7, "Erase", curses.color_pair(4))
                
        
              
            

        if key == curses.KEY_MOUSE and active_tool == "draw":
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
                #sleep(0.01)
        
        
        if key == curses.KEY_MOUSE and active_tool == "erase":
            _, mouse_x, mouse_y, _, _ = curses.getmouse()  # Get mouse event details
            if mouse_x >= 0 and mouse_y >= 0 and not mouse_x % 2 and not random_mode:
                window.addstr(mouse_y, mouse_x, "  ")  # Place an 'X' at the clicked position
                mouse_x_even = mouse_x
                row_index = mouse_y
                col_index = mouse_x_even // 2  # Convert even X coordinate to column index

                # Update the blocks list
                while len(blocks) <= row_index:
                    blocks.append([])  # Add new rows as needed

                if len(blocks[row_index]) <= col_index:
                    blocks[row_index].extend([0] * (col_index - len(blocks[row_index]) + 1))
                blocks[row_index][col_index] = 0

                window.refresh()
                #sleep(0.01)

        
        

    

# Define the draw_pixel function
def draw_pixel(window):
    refresh_time = 1/fps
    global blocks  # Declare 'blocks' as a global variable
    global threshold

    

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
        window.addstr(1, 1, """Press "ESC" to restart""")
        window.addstr(2, 1, """Press "Ctrl+C" to quit""")
        key = window.getch()
        if key == 27:
            window.clear()
            break
        window.refresh()
        sleep(refresh_time)

        # Update the blocks list with a new layout
        blocks = gol(blocks)
        window.clear()



# Initialize curses
try:   
    while True:
        curses.wrapper(draw_cells) 
        curses.wrapper(draw_pixel) 
except KeyboardInterrupt:
    sys.exit(0)