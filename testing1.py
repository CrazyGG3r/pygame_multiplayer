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
col = (100,100,0)
p1 = person((width//2,height//2),20,5,'test',col,100,100,5)

bg = (0,0,0)
movr = False
keyy = None
clock = pygame.time.Clock()
keys_pressed = set()
bullets= []
btick = 0
fps = 60
ti =  0
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
            if event.key == pygame.K_SPACE and (btick % fps == p1.guncooldown):
                btick = 0 
                m = pygame.mouse.get_pos()
                new_bullet = bullet(p1.x, p1.y)
                new_bullet.shot(p1.x,p1.y,m[0],m[1],)
                bullets.append(new_bullet)        
        if event.type == pygame.KEYUP:
           keys_pressed.discard(event.key)
    for a in bullets:
        if a.shooting == False:
            bullets.remove(a)
    for a in bullets:
        if a.shooting == False:
            bullets.remove(a)
            logging.info("Bullet removed")
            continue
        a.move()
        a.draw(screen)
    p1.draw(screen)
    btick +=  1
    for a in keys_pressed:
        p1.move(a,screen)
        if a == pygame.K_SPACE and (btick % fps == p1.guncooldown):
            btick =0 
            m = pygame.mouse.get_pos()
            new_bullet = bullet(p1.x, p1.y)
            new_bullet.shot(p1.x,p1.y,m[0],m[1],)
            bullets.append(new_bullet)
            print(len(bullets))
    pygame.display.flip()
