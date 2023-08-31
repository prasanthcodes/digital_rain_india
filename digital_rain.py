import pygame
import random
import math

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


N_chars=100

#---initializations-------
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


font = pygame.font.Font("Nirmala.ttf", 20)
fontB = pygame.font.Font("NirmalaB.ttf", 20)

#---characters initializatiion---
labelstack=[]
label_positions=[]
for i in range(N_chars):
    label_positions.append([SCREEN_WIDTH*random.random(),SCREEN_HEIGHT*random.random(),1+3*random.random()])


#---to find character height and width---
screen.fill((255, 255, 255))

char_width=0#initializatiion
char_height=0#initializatiion
tmp_h=[]
for i in range(len(devachar)):
    char_now=fontB.render(devachar[i], 1, (255,255,255))
    tmp_w=char_now.get_width()
    tmp_h=char_now.get_height()
    if tmp_w>char_width: char_width=tmp_w
    if tmp_h>char_height: char_height=tmp_h

print('char_width=',char_width)
print('char_height=',char_height)
start_positions=[]
for i in range(SCREEN_WIDTH):
    start_positions.append(i*char_width)
    if i*char_width>SCREEN_WIDTH: break
#print('start_positions=',start_positions)

rand_start_indices=list(range(len(start_positions)))
random.shuffle(rand_start_indices)

chains=[]
chain_heights=list(range(5,math.floor(SCREEN_HEIGHT/(1+char_height))))# maximum is SCREEN_HEIGHT/(1+char_height)
N_chains=40#should be less than len(start_positions) i.e approximately 76
rand_start_indices=rand_start_indices[0:N_chains]
chain_positions=[]
for i in range(N_chains):
    chain_positions.append([start_positions[rand_start_indices[i]],SCREEN_HEIGHT*0*random.random(),1+3*random.random(),chain_heights[random.randint(0,len(chain_heights)-1)]])
    


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

    # label = fontB.render(devachar[0], 1, (0,255,0))
    # for i in range(N_chars):
        # labelstack.append(fontB.render(devachar[i%(len(devachar))], 1, (0,255,0)))
        # #print(labelstack[i].get_height())
        # # put the label object on the screen at point x=100, y=100
        # x_pos_char=label_positions[i][0]
        # label_positions[i][1]+=label_positions[i][2]
        # y_pos_char=label_positions[i][1]
        # if y_pos_char>SCREEN_HEIGHT:
            # label_positions[i]=[SCREEN_WIDTH*random.random(),(SCREEN_HEIGHT*0)*random.random(),1+3*random.random()]
        # screen.blit(labelstack[i], (x_pos_char, y_pos_char))
        
    for i in range(N_chains):
        x_pos_char=chain_positions[i][0]
        chain_height=chain_positions[i][3]
        for j in range(chain_height):
            cnow=fontB.render(devachar[random.randint(0,len(devachar)-1)], 1, (0,255,0))
            #labelstack.append(fontB.render(devachar[i%(len(devachar))], 1, (0,255,0)))
            y_pos_char=chain_positions[i][1]-j*(1+char_height)
            if y_pos_char<0: break
            screen.blit(cnow, (x_pos_char, y_pos_char))
            
        if y_pos_char>SCREEN_HEIGHT:
            chain_positions[i]=[start_positions[random.randint(0,len(start_positions)-1)],SCREEN_HEIGHT*0*random.random(),1+3*random.random()]
        chain_positions[i][1]+=chain_positions[i][2]

        
    pygame.display.flip()
    time_count+=1

    clock.tick(fps_rate)
    fps=clock.get_fps()
    # # ---save screenshot---
    # pygame.image.save(screen, "screenshot.png")

pygame.quit()



