import pygame
from allclass import * 
import random as r 

pygame.init()
i = pygame.display.Info()
width,height = 1280,720
#width ,height = i.current_w, i.current_h
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((width, height))
#col = (r.randint(100,255),r.randint(100,255),r.randint(100,255))
col = (0,200,200)
p1 = person((width//2,height//2),20,5,'test',col,100,100,5)

bg = (0,20,20)
movr = False
keyy = None
clock = pygame.time.Clock()
keys_pressed = set()
bullets= []
btick = 0
fps = 60
ti =  0
players = [p1]
enemies = []
spaw = spawner(screen)
while True:
    screen.fill(bg)
    clock.tick(fps)
    ti +=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        if event.type == pygame.KEYUP:
           keys_pressed.discard(event.key)
           
    for a in keys_pressed:
        for p in players:
            p.decision(a,screen,ti)
    if ti % spaw.speed*fps == 0:
        enemies.append(spaw.spawn())
    
    for e in enemies:
        m = pygame.mouse.get_pos()
        if e :
            if ti%5 ==0:
                e.move1(screen,p1.x,p1.y)
            e.draw(screen)
    for p in players:
        if p.bullets:
            for b in p.bullets:
                if b == None:
                    continue
                if b.shooting == False:
                    p.bullets.remove(b)
                else:
                    
                    b.move()
                    b.draw(screen)
        p.draw(screen)           
    pygame.display.flip()
