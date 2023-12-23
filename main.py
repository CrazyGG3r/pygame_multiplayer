import pygame
from allclass import Ball
import random as r
import sys
import socket
import threading
import ast
import logging

pygame.init()
#loggerr
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
#connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 5555))
    logging.info("Successfully connected to the server")
except socket.error as e:
    logging.error(f"Could not connect to the server: {e}")
# Screen dimensions
width, height = 640, 480

# Create the screen
screen = pygame.display.set_mode((width, height))

# Create a Ball instance
pname = 'blabla'
color = (r.randint(100, 255), r.randint(100, 255), r.randint(100, 255))
ball = Ball(width // 2, height // 2, 20, 5, pname, color)
clock = pygame.time.Clock()
logging.info("~~Player = {}".format(pname))
# Initialize movement states
moving_right = False
moving_left = False
moving_up = False
moving_down = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_DOWN:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_DOWN:
                moving_down = False

    # Move the ball based on key states
    if moving_right:
        ball.move(pygame.K_RIGHT, screen)
    if moving_left:
        ball.move(pygame.K_LEFT, screen)
    if moving_up:
        ball.move(pygame.K_UP, screen)
    if moving_down:
        ball.move(pygame.K_DOWN, screen)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the ball
    ball.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

pygame.quit()
