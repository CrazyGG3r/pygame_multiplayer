
from re import X
from telnetlib import XASCII
from turtle import speed
import pygame
import socket
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
pygame.init()
WIDTH,HEIGHT = 800,600

class Ball:
    def __init__(self,coords, radius, speed, name, color):
        self.fnt = pygame.font.Font(None, 20)
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.radius = int(radius)
        self.tname = str(name)
        self.name = self.fnt.render(self.tname, True, (255, 255, 255))
        self.speed = int(speed)
        self.color = tuple(color)
    def bname(self):
       self.name = self.fnt.render(self.tname, True, (255, 255, 255))
    def move(self,event,screen,client = None):
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
         if client:
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
class bullet:
    def __init__(self,color = (255,255,0),x = 0,y = 0, Duration = 10, speed = 1,size = 5):
        self.x = x
        self.y = y
        self.xd = None #destination x
        self.yd = None #destination y
        self.speed = speed
        self.size = size
        self.color = color
        self.shooting = False
        logging.info("Bullet created")
        #self.duration = Duration
        #self.currdur = 0
        
        
    def shot(self,charx,chary,mousex,mousey):
        self.x  = charx
        self.y  = chary
        self.cx = charx
        self.cy = chary
        self.xd = mousex
        self.yd = mousey
        self.shooting = True
      

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.cx,self.cy),self.size)
        
    def move(self):
       
        if self.shooting == True:
            dx = self.xd - self.x
            dy = self.yd - self.y
            if dx == 0: 
                grad = float('inf') 
            else:
                grad = dy / dx

            step_x = self.speed if dx > 0 else -self.speed
            step_y = step_x * grad

            if (step_x > 0 and self.cx < self.xd) or (step_x < 0 and self.cx > self.xd):
                self.cx += step_x
            if (step_y > 0 and self.cy < self.yd) or (step_y < 0 and self.cy > self.yd):
                self.cy += step_y

            if (step_x > 0 and self.cx >= self.xd) or (step_x < 0 and self.cx <= self.xd):
                self.cx = self.xd
                self.shooting = False
            if (step_y > 0 and self.cy >= self.yd) or (step_y < 0 and self.cy <= self.yd):
                self.cy = self.yd
                self.shooting = False
            
class gun:
    def __init__(self,ammo = 100,cooldown = 1):
        self.ammo = ammo
        self.guncooldown = cooldown
        
class person(Ball,gun):#is a ball for now
    def __init__(self,coords, radius, speed, name, color,ammo,health,lives):
        super().__init__(coords, radius, speed, name, color)
        gun.__init__(self)
        self.maxhp = health
        self.currenthp = health
        self.lives = lives
        
        
    def draw(self, screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
        screen.blit(self.name,((self.x-self.radius),(self.y + self.radius +10)))
        barwidth = 40
        barheight = 6
        healthpercent = self.currenthp/self.maxhp
        reed = 0
        green = 255
        if healthpercent < 0.4:
            reed = min(((reed + 5),255))
            green = max(((green - 5),0))
        else:
            green = 255
            reed = 0
        barcolor = (reed,green,0)
        currentfullhealthbarwidth =  healthpercent* barwidth
        o = 10
        currentfullhealthbarheight = barheight - 2
        bgrect = pygame.Rect((self.x - self.radius),(self.y-(self.radius + o+1)),barwidth,barheight)
        pygame.draw.rect(screen,(230,230,230),bgrect)      
        currbgrect = pygame.Rect((self.x - self.radius),(self.y-(self.radius + o)),currentfullhealthbarwidth,currentfullhealthbarheight)
        pygame.draw.rect(screen,barcolor,currbgrect)
    
    def shoot(self,mx,my):
        
        
        b = bullet()
        b.shot(self.x,self.y,mx,my)
        return bullet
        