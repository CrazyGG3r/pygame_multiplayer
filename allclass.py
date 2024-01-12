
from quopri import decodestring
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
    def __init__(self,color = (255,255,255),x = 0,y = 0, Duration = 3, size = 5):
        self.x = x
        self.y = y
        self.cx = self.x
        self.cy = self.y
        self.size = size                                        
        self.color = color
        self.shooting = False
        self.duration = Duration * 60  #duration defines speed
        self.speed = None #the unitvector.
        self.startvec = (self.x,self.y)
        self.currentvec = (self.cx,self.cy)
        self.destvector = (0,0)
        self.unitvector = (0,0)# speed
        self.tick = 0
        #------ grad
        
  
    def shot(self,charx,chary,mousex,mousey):
        self.x  = charx
        self.y  = chary
        self.cx = charx
        self.cy = chary
        self.xd = mousex
        self.yd = mousey
        self.currentvec = (self.cx,self.cy)
        self.destvector = (float(self.xd),float(self.yd))
        self.unitvector = ((self.destvector[0] - self.currentvec[0])/self.duration,(self.destvector[1] - self.currentvec[1])/self.duration)
        self.shooting = True
        logging.info("Bullet Shot. Unit Vector created")

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,self.currentvec,self.size)
        
    def move(self):
        self.tick+=1
        if self.tick == self.duration:
            self.shooting = False
        if self.shooting == True:
            if self.currentvec == self.destvector:
                self.shooting = False
            else:
                self.currentvec = (float(self.currentvec[0]+ self.unitvector[0]),float(self.currentvec[1]+self.unitvector[1]))

            
            
       
            
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
