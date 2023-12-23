import pygame
import socket
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
pygame.init()
WIDTH,HEIGHT = 800,600

class Ball:
    def __init__(self,coords, radius, speed, name, color):
        self.fnt = pygame.font.Font(None, 15)
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.radius = int(radius)
        self.tname = str(name)
        self.name = self.fnt.render(self.tname, True, (255, 255, 255))
        self.speed = int(speed)
        self.color = tuple(color)
    def bname(self):
       self.name = self.fnt.render(self.tname, True, (255, 255, 255))
    def move(self,event,screen,client):
         if event == pygame.K_RIGHT:
              if screen.get_width()> self.x:
                self.x +=self.speed
              else: 
                self.x = screen.get_width()
                
         if event == pygame.K_LEFT:
              if 0 < self.x:
                self.x -=self.speed
              else: 
                self.x = 0
                
         if event == pygame.K_UP:
             if 0 < self.y:
                 self.y -= self.speed
             else :
                 self.y = 0 
                 
         if event== pygame.K_DOWN:
             if screen.get_height() >  self.y:
                self.y += self.speed
             else: 
                self.y = screen.get_height()
         ball_data = {
             'x': self.x,
             'y': self.y,
             'name': self.tname,
             'color': list(self.color)  
         }
         serialized_data = json.dumps(ball_data) + "\n"  
         try:
             client.sendall(serialized_data.encode('utf-8'))
             logging.info("Data sent")
         except socket.error as e:
             logging.error("Socket error: %s", e)
         
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        screen.blit(self.name,((self.x-self.radius),(self.y + self.radius +10)))
        
    def updatewholeball(self,data):
       self.tname = str(data['name'])
       self.bname()
       self.x = data['x']
       self.y = data['y']
       self.color = data['color']
    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'radius': self.radius}