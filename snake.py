import random
import curses

stdscr = curses.initscr() # returns a window object representing the entire screen
curses.noecho() # turn off automatic echoing of keys to the screen
curses.cbreak() # Enter cbreak mode from the usual buffered input mode, so no Enter needed
curses.curs_set(False) # Make cursor invisible
sh, sw = stdscr.getmaxyx() # Figure out terminal height and width
w = curses.newwin(sh, sw, 0, 0) # Create a new window of the same size as the terminal
w.keypad(True) # Enable keyboard input
w.timeout(100) # window reads blocks for delay 100 milliseconds 

# Objects on a 2-d board are defined by 2 numbers - x, y coordinates
snake_x = sw // 4
snake_y = sh // 2
snake = [[snake_y, snake_x], [snake_y, snake_x - 1], [snake_y, snake_x - 2]]
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_BLOCK) # Print char on the window
key = curses.KEY_RIGHT # Initially snake moves to the right

while True:
    next_key = w.getch() # refreshes the screen and then waits for the user to hit a key
    if next_key != -1: # -1 signals "no input from the user"
        key = next_key
    # Check losing conditions: going out of bounds or inside its own body
    if snake[0][0] in [0, int(sh) - 1] or snake[0][1] in [0, int(sw) - 1] or snake[0] in snake[1:]:
        curses.nocbreak()
        w.keypad(False)
        curses.echo()
        curses.endwin()
        quit()
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    snake.insert(0, new_head) # we always insert new_head
    if snake[0] == food:
        food = None
        while food is None:
            nf = [random.randint(1, sh-1), random.randint(1, sw - 1)]
            if nf not in snake:
                food = nf 
        w.addch(food[0], food[1], curses.ACS_BLOCK)
    else:
        tail = snake.pop() # we delete tail if no food is consumed
        w.addch(tail[0], tail[1], ' ')
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)