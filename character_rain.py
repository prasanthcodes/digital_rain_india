import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#---input params---
fps_rate=100
#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


hex1=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
devachar=[]
for i in range(38):
    devachar.append(chr(int('0x'+str(904+i),16)))


max_time=1e3


N_chars=1000

#---initializations-------
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


font = pygame.font.Font("Nirmala.ttf", 20)
fontB = pygame.font.Font("NirmalaB.ttf", 20)

labelstack=[]
label_positions=[]
for i in range(N_chars):
    label_positions.append([SCREEN_WIDTH*random.random(),SCREEN_HEIGHT*random.random(),2+3*random.random()])


time_count=1
running = True
clock = pygame.time.Clock()

while running:

    #----window closing conditions-------
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        if time_count > max_time:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    label = fontB.render(devachar[0], 1, (0,255,0))
    for i in range(N_chars):
        labelstack.append(fontB.render(devachar[i%(len(devachar))], 1, (0,255,0)))
        # put the label object on the screen at point x=100, y=100
        x_pos_char=label_positions[i][0]
        label_positions[i][1]+=label_positions[i][2]
        y_pos_char=label_positions[i][1]
        if y_pos_char>SCREEN_HEIGHT:
            label_positions[i]=[SCREEN_WIDTH*random.random(),(SCREEN_HEIGHT*0)*random.random(),2+3*random.random()]
        screen.blit(labelstack[i], (x_pos_char, y_pos_char))
        
    pygame.display.flip()
    time_count+=1

    clock.tick(fps_rate)
    fps=clock.get_fps()
    # # ---save screenshot---
    # pygame.image.save(screen, "screenshot.png")

pygame.quit()



