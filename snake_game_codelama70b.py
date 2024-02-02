#Codelama 70b , 3/2/2024
#prompt: write snake game in python with pygame library
import pygame
import random
import time

pygame.init()

# Define the screen size
screen_width = 600
screen_height = 400

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Snake Game")

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the snake's initial position and size
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Define the food's position and size
food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
food_spawn = True

# Define the direction and speed of the snake
direction = "RIGHT"
change_to = direction

# Define the score and the game's state
score = 0
game_over = False

# Define the font for displaying the score
font = pygame.font.SysFont("monospace", 18)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Check if the user pressed a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    # Check if the user pressed a key that is not the current direction
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # Move the snake
    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    # Insert the new snake position at the beginning of the snake body
    snake_body.insert(0, list(snake_pos))

    # Check if the snake has hit itself or the wall
    if snake_pos[0] < 0 or snake_pos[0] > screen_width - 10:
        game_over = True
    if snake_pos[1] < 0 or snake_pos[1] > screen_height - 10:
        game_over = True
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over = True

    # Check if the snake has eaten the food
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width // 10)) * 10, random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True

    # Draw the screen
    screen.fill(BLACK)

    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Display the score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, [0, 0])

    # Check if the game is over
    if game_over:
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, [screen_width // 2 - 50, screen_height // 2 - 10])

    pygame.display.update()
    time.sleep(0.1)