import pygame
import random

# Initialize Pygame
pygame.init()

win_width = 640
win_height = 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 30

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

def create_snake():
    return [(win_width // 2, win_height // 2)]  # Fix: Remove * snake_block

opposite_dirs = {
    pygame.K_UP: pygame.K_DOWN,
    pygame.K_DOWN: pygame.K_UP,
    pygame.K_LEFT: pygame.K_RIGHT,
    pygame.K_RIGHT: pygame.K_LEFT
}

def change_direction(new_dir):
    global direction
    if new_dir != opposite_dirs[direction]:
        direction = new_dir

def move_snake():
    global snake, food
    head = snake[0]
    directions = {
        pygame.K_UP: (head[0], head[1] - snake_block),
        pygame.K_DOWN: (head[0], head[1] + snake_block),
        pygame.K_LEFT: (head[0] - snake_block, head[1]),
        pygame.K_RIGHT: (head[0] + snake_block, head[1])
    }
    next_head = directions[direction]
    snake.insert(0, next_head)
    if not is_collision():
        if snake[0] == food:  # Fix: Check if snake has eaten the food
            food = create_food()
        else:
            snake.pop()  # Fix: Only remove the tail if no food is eaten
    else:
        game_over()

def draw_snake():
    for segment in snake:
        pygame.draw.rect(win, green, pygame.Rect(segment[0], segment[1], snake_block, snake_block))

def create_food():
    return (random.randint(0, (win_width // snake_block - 1)) * snake_block, random.randint(0, (win_height // snake_block - 1)) * snake_block)

def draw_food(food):
    pygame.draw.rect(win, red, pygame.Rect(food[0], food[1], snake_block, snake_block))

def is_collision():
    if (snake[0][0] < 0 or
            snake[0][0] >= win_width or  # Fix: Remove * snake_block
        # Update score
            snake[0][1] < 0 or
            snake[0][1] >= win_height):  # Fix: Remove * snake_block
        return True
            score += 10
    for segment in snake[1:]:
        if segment == snake[0]:
            return True
    return False
        font = pygame.font.SysFont("consolas", 30)
def game_over():
    pygame.quit()
    main()
direction = pygame.K_DOWN
snake = create_snake()
food = create_food()
score = 0

def main():
    global direction, win, snake, food, score
if __name__ == "__main__":
    main()
    run = True

    while run:
        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            change_direction(pygame.K_UP)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            change_direction(pygame.K_DOWN)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            change_direction(pygame.K_LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            change_direction(pygame.K_RIGHT)

        # Move the snake
        move_snake()

        draw_food(food)
        draw_snake()

        # Show text on screen
        font = pygame.font.SysFont("consolas", 30)
        score_text = font.render(f"Score: {len(snake)}", True, white)  # Fix: Score is the length of the snake
        win.blit(score_text, (5, 10))

        # Update the display
        pygame.display.update()

        # Set frame rate and wait for next frame
        clock.tick(snake_speed)

    game_over()

if __name__ == "__main__":
    main()