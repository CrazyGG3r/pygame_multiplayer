
import pygame
from allclass import Ball
import random as r
import sys
import socket
import threading
import ast
import logging
import json



pygame.init()
#client-log
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
#server details
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '26.1.98.217'
port = 5555
try:
    client.connect((ip,port))
    logging.info("Successfully connected to the server")
except socket.error as e:
    logging.error(f"Could not connect to the server: {e}")


radius = 20
speed = 5

width, height = 640, 480

screen = pygame.display.set_mode((width, height))
restball = Ball((0,0),20,5,' ',(0,0,0))
rb = {}
def listenserver(sock, screen):
 logging.info("Listening from: {}:{}".format(ip, port))
 logging.info("created otherplayers")

 while True:
     try:
         data = sock.recv(65536)  # mera buffer meri marzi
         if data:
             player_data = json.loads(data.decode('utf-8'))
             logging.info("Received player_data: %s", player_data)

             for player_id, player_dat in player_data.items():
                 print(player_dat['name'])

                 if player_id in rb:
                 
                     rb[player_id].x = player_dat['x']
                     rb[player_id].y = player_dat['y']
                     rb[player_id].name = player_dat['name']
                     rb[player_id].color = tuple(player_dat['color']) 
                 else:
                
                     rb[player_id] = Ball((player_dat['x'], player_dat['y']), 20, 5, player_dat['name'], tuple(player_dat['color']))

     except Exception as e:
         logging.error("An error occurred: %s", e)
         break


# Assuming 'client' is your connected socket object
thread = threading.Thread(target=listenserver, args=(client,screen,))
thread.start()


# Create a Ball instance
pname = 'seeweiwueiwuie'
color = (r.randint(100, 255), r.randint(100, 255), r.randint(100, 255))
ball = Ball((width // 2, height // 2),20, 5, pname, color)
clock = pygame.time.Clock()
logging.info("Player = {}".format(pname))
rblist = []
#restball instance


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

    if moving_right:
        ball.move(pygame.K_RIGHT, screen,client)
    if moving_left:
        ball.move(pygame.K_LEFT, screen,client)
    if moving_up:
        ball.move(pygame.K_UP, screen,client)
    if moving_down:
        ball.move(pygame.K_DOWN, screen,client)
    
    screen.fill((0, 0, 0))

    #ball.draw(screen)
 
    for pid,a in rb.items():
        a.bname()
        a.draw(screen)

   
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
