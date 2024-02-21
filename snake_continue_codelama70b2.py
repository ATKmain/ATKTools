import pygame, random, sys

# Define constants for screen width/height and frame rate
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 15
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.x_pos = SCREEN_WIDTH / 2   # Set initial x position of snake in middle of screen
        self.y_pos = SCREEN_HEIGHT / 2  # Set initial y position of snake in middle of screen
        self.size = 10                  # Define size of each segment (pixel dimensions)
        self.color = WHITE              # Set color of the snake to white
        self.segments = []              # Initialize a list for storing segments
    
class Food:
    def __init__(self):
        self.x_pos = random.randrange(SCREEN_WIDTH - 20)   # Generate a random x position within screen bounds (excluding walls)
        self.y_pos = random.randrange(SCREEN_HEIGHT - 20) # Generate a random y position within screen bounds (excluding walls)
    
def main():
    pygame.init()   # Initialize the PyGame library
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   # Create a display surface for drawing on
    clock = pygame.time.Clock()  # Create a Clock object to help control frame rate
    
    snake = Snake()   # Create an instance of the Snake class
    food = Food()     # Create an instance of the Food class
    direction = "RIGHT"    # Set initial movement direction for the snake
    x_change, y_change = 10, 0   # Define changes in position based on current direction
    
    while True:     # Main game loop
        screen.fill((0, 0, 0))  # Fill the display surface with a black background
        
        for event in pygame.event.get():    # Check for any events (e.g., keyboard input)
            if event.type == pygame.QUIT:   # If user clicks "X" to close window, exit the game
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:  # Handle key presses for movement and exiting the game
                if event.key == pygame.K_LEFT and direction != "RIGHT":   # Only allow valid movements (e.g., cannot move left when facing right)
                    x_change = -10
                    y_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x_change = 10
                    y_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    x_change = 0
                    y_change = -10
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    x_change = 0
                    y_change = 10
                    direction = "DOWN"
            
        snake.x_pos += x_change   # Update the snake's position based on current movement direction
        snake.y_pos += y_change
        
        # Check for wall collisions and end game if collision occurs
        if snake.x_pos < 0 or snake.x_pos > SCREEN_WIDTH - snake.size or snake.y_pos < 0 or snake.y_pos > SCREEN_HEIGHT - snake.size:
            break   # Exit the main game loop and end the game
        
        # Check for collisions with food and generate new food position if collision occurs
        if (snake.x_pos, snake.y_pos) == (food.x_pos, food.y_pos):
            while True:     # Loop until finding a valid location for new food
                x = random.randrange(SCREEN_WIDTH - 20)   # Generate a random x position within screen bounds (excluding walls)
                y = random.randrange(SCREEN_HEIGHT - 20)  # Generate a random y position within screen bounds (excluding walls)
                if not any((x, y) == segment for segment in snake.segments):  # Check if new food location is valid (not on top of snake body)
                    break   # Break out of loop if location is valid, otherwise try again
            food = Food()   # Create a new piece of food at the random position generated above
            snake.size += 10      # Increase size of each segment by 10 pixels (increases snake length by 1)
        
        pygame.draw.rect(screen, (255, 0, 0), (food.x_pos, food.y_pos, snake.size, snake.size))    # Draw the piece of food on the display surface
        
        # Draw the snake's segments on the display surface
        for i in range(len(snake.segments)):
            pygame.draw.rect(screen, (0, 255, 0), (snake.segments[i][0], snake.segments[i][1], snake.size, snake.size))

        head = [(snake.x_pos, snake.y_pos)]   # Add a segment for the snake's head at its current position
        snake.segments.append(head)  # Update the list of segments to include the new head segment
        snake.segments = snake.segments[1:]    # Remove the oldest segment (creates "illusion" of movement)
        
        pygame.display.update()   # Update the display surface with all drawn objects from this frame
        clock.tick(FPS)  # Control the frame rate of the game to keep it consistent and smooth
    
    # Display a "Game Over!" message once the user collides with a wall or themself
    font = pygame.font.SysFont("impact", 64)   # Define a font object for rendering text
    text_surface = font.render("Game Over!", True, (255, 255, 255))   # Create a Surface object with the "Game Over!" message
    text_rectangle = text_surface.get_rect()   # Get a Rectangle object from the Surface for positioning purposes
    text_rectangle.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)  # Position the "Game Over!" message in the middle of the display surface
    screen.blit(text_surface, text_rectangle)   # Draw the "Game Over!" message onto the display surface
    
    pygame.display.update()   # Update the entire display to show the "Game Over!" message
    
    time.sleep(2)    # Pause the game for a moment to allow the user to digest the loss
    pygame.quit()     # Exit PyGame and close the window
    
if __name__ == "__main__":  # Ensure that main() is only called if this script is run directly (not when imported as a module)
    main()   # Call the main function to start the game!
