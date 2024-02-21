import curses
import random

# Initialize curses
stdscr =  curses.initscr()
curses.curs_set(0)
stdscr.nodelay(True)

# Set up the game window 
win = curses.newwin(20, 60, 0, 0)
win.border(0)
win.keypad(True)

# Initialize the snake
snake = [(4, 10), (4, 9), (4, 8)]
 direction = curses.KEY_RIGHT

# Initialize the food
food = (10, 20)

# Initialize the score
score = 0

# Main game loop
while True:
    # Get the next keypress
    key = win.getch()

    # If the keypress is a valid direction, change the direction of the snake
    if key in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN]:
        direction = key

    # Move the snake
    head = snake[0]
     if direction == curses.KEY_LEFT:
        head = (head[0] - 1, head[1])
    elif direction == curses.KEY_RIGHT:
        head = (head[0] + 1, head[1])
    elif direction == curses.KEY_UP:
        head = (head[0], head[1] - 1)
    elif direction == curses.KEY_DOWN:
        head = (head[0], head[1] + 1)

    # Add the new head to the snake and remove the tail
    snake.insert(0, head)
    snake.pop()

    # Check if the snake has hit itself or the walls
    if head in snake[1:] or head[0] < 0 or head[0] > 19 or head[1] < 0 or head[1] > 59:
        break

    # Check if the snake has eaten the food
    if head == food:
        # Increase the score
        score += 1

        # Generate new food
        food = (random.randint(1, 19), random.randint(1 , 59))

        # Make the snake longer
        snake.append(snake[-1])

    # Draw the game board
    win.clear()
    win.addstr(0, 2, 'Score: {}'.format(score))
    for y, x in snake:
        win.addstr(y, x, '#')
    win.addstr(food[0], food[1], '@')
    win.refresh()

# End the game
curses.endwin()
