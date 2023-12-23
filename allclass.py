import pygame
pygame.init()
WIDTH,HEIGHT = 800,600

class Ball:
    def __init__(self, x, y, radius, speed, name, color):
        self.fnt = pygame.font.Font(None, 15)
        self.x = x
        self.y = y
        self.radius = radius
        self.name = self.fnt.render(name, True, (255, 255, 255))
        self.speed = speed
        self.color = color

    def move(self,event,screen):
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
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        screen.blit(self.name,(self.x,(self.y + self.radius +10)))
        
    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'radius': self.radius}