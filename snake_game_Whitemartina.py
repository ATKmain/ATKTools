import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = 'RIGHT'

    def move(self):
        x, y = self.body[0]
        if self.direction == 'UP':
            y -= CELL_SIZE
        elif self.direction == 'DOWN':
            y += CELL_SIZE
        elif self.direction == 'LEFT':
            x -= CELL_SIZE
        elif self.direction == 'RIGHT':
            x += CELL_SIZE
        self.body.insert(0, (x, y))
        self.body.pop()

    def grow(self):
        x, y = self.body[-1]
        self.body.append((x, y))

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH // CELL_SIZE) * CELL_SIZE
        self.y = random.randint(0, HEIGHT // CELL_SIZE) * CELL_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, CELL_SIZE, CELL_SIZE))

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
snake = Snake()
food = Food()

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.direction = 'RIGHT'

    snake.move()

    if snake.body[0] == (food.x, food.y):
        snake.grow()
        food = Food()

    if snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT:
        running = False

    for segment in snake.body[1:]:
        if segment == snake.body[0]:
            running = False

    snake.draw(screen)
    food.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
