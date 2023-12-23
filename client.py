import pygame
import sys
import socket
import threading
import ast
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))
logging.info("Connected to the server")

def receive_data():
    while True:
        try:
            data = client.recv(1024).decode()
            positions = ast.literal_eval(data)
            # Update game state based on received positions
        except:
            logging.error("Error receiving data", exc_info=True)
            client.close()
            break

class Ball:
    def __init__(self, x, y, radius, speed, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.screen = screen
        self.color = (255, 255, 255)  # White

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Keep the ball within the screen bounds
        self.x = max(self.radius, min(self.x, width - self.radius))
        self.y = max(self.radius, min(self.y, height - self.radius))

   

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 640, 480

# Create the screen
screen = pygame.display.set_mode((width, height))

# Create a Ball instance
ball = Ball(width // 2, height // 2, 20, 5, screen)

threading.Thread(target=receive_data).start()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for key presses
    keys = pygame.key.get_pressed()
    ball.move(keys)
    client.sendall(f"{ball.x},{ball.y}".encode())
    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the ball
    ball.draw()

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
