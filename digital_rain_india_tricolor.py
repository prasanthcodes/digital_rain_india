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

def set_tricolor(SCREEN_HEIGHT,y_pos_char_tmp,gradient,flag):
    india_tricolor=[[255,154,51],[255,255,255],[19,136,7]]
    chakra_color=[1,1,128]
    #char_color=(0,int(gradient*255),0)
    if gradient<0.7: gradient=0.7+0.1*gradient
    gradient=1
    if flag==1:
        char_color=(250,255,250)
        # random values added to make the border smooth
        if (y_pos_char_tmp>=0)&(y_pos_char_tmp<(SCREEN_HEIGHT/3)+50*random.random()):
            #char_color=(int(gradient*255),255,int(gradient*255))
            char_color=(india_tricolor[0][0],india_tricolor[0][1],india_tricolor[0][2]-india_tricolor[0][2]*gradient)
        if (y_pos_char_tmp>=(SCREEN_HEIGHT/3))&(y_pos_char_tmp<(SCREEN_HEIGHT/3)*2+50*random.random()):
            char_color=(128+india_tricolor[1][0]*gradient/2,128+india_tricolor[1][1]*gradient/2,128+india_tricolor[1][2]*gradient/2)
        if (y_pos_char_tmp>=(2*SCREEN_HEIGHT/3))&(y_pos_char_tmp<(3*SCREEN_HEIGHT/3)+50*random.random()):
            char_color=(india_tricolor[2][0],india_tricolor[2][1]+(255-india_tricolor[2][1])*gradient,india_tricolor[2][2])
                        
    return char_color
    
    
#---input parameters---

fps_rate=70

#SCREEN_WIDTH = 800
#SCREEN_HEIGHT = 600

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# maximum count to run the main loop
max_time=1000


transition_percentage=1 #(0-100)#how many percentage of total characters transition to another character in one time
N_chains=50 #number of 'character chains'. should be less than len(start_positions) i.e less than 76

#---initializations-------
pygame.init()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

#font = pygame.font.Font("Nirmala.ttf", 20)
fontB = pygame.font.Font("NirmalaB.ttf", 20)

#---create and store 38 devanagari characters---
hex1=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
devachar=[]
for i in range(38):
    devachar.append(chr(int('0x'+str(904+i),16)))


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

print('char_width=',char_width)#26
print('char_height=',char_height)#27

#---to allocate top most postions for 'character chain'-----
start_positions=[]
for i in range(SCREEN_WIDTH):
    start_positions.append(i*char_width)
    if i*char_width>(SCREEN_WIDTH-char_width): break
#print('start_positions=',start_positions)

rand_start_indices=list(range(len(start_positions)))
random.shuffle(rand_start_indices)

#---make the character chain---
chains=[]
chain_heights=list(range(25,math.floor(SCREEN_HEIGHT/(1+char_height))))# maximum is SCREEN_HEIGHT/(1+char_height) #i.e (864/28)=30
#N_chains=40#should be less than len(start_positions) i.e less than 76
rand_start_indices=rand_start_indices[0:N_chains]
chain_data=[]
for i in range(N_chains):
    x_pos=start_positions[rand_start_indices[i]]
    y_pos=SCREEN_HEIGHT*0*random.random()
    speed=2+5*random.random()
    chain_height=chain_heights[random.randint(0,len(chain_heights)-1)]
    char_list=[]
    for j in range(chain_height):
        gradient=0.05+0.8*(j/chain_height)
        char_list.append([devachar[random.randint(0,len(devachar)-1)],gradient])
    chain_data.append([x_pos,y_pos,speed,chain_height,char_list])
    

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
    screen.fill((0, 0, 0))

    for i in range(N_chains):
        x_pos_char=chain_data[i][0]
        chain_height=chain_data[i][3]
        for j in range(chain_height):
            if random.random()<(transition_percentage/100):
                letter_now=devachar[random.randint(0,len(devachar)-1)]
                chain_data[i][4][j][0]=letter_now
            if j==0: char_color=(250,255,250)
            gradient=chain_data[i][4][j][1]
            #char_color=(int(gradient*255),255,int(gradient*255))
            y_pos_char=chain_data[i][1]-j*(1+char_height)
            letter_now=chain_data[i][4][j][0]
            char_color=set_tricolor(SCREEN_HEIGHT,y_pos_char,gradient,1)
            char_now=fontB.render(letter_now, 1, char_color)
            if y_pos_char<0: break
            screen.blit(char_now, (x_pos_char, y_pos_char))
            
        #---if 'character chain' goes down below the screen, it creates new one from top---
        if y_pos_char>SCREEN_HEIGHT:
            x_pos=start_positions[random.randint(0,len(start_positions)-1)]
            y_pos=SCREEN_HEIGHT*0*random.random()
            speed=2+5*random.random()
            chain_height=chain_heights[random.randint(0,len(chain_heights)-1)]
            char_list=[]
            for j in range(chain_height):
                gradient=0.05+0.8*(j/chain_height)
                char_list.append([devachar[random.randint(0,len(devachar)-1)],gradient])
                
            chain_data[i]=[x_pos,y_pos,speed,chain_height,char_list]
            
        chain_data[i][1]+=chain_data[i][2]

        
    pygame.display.flip()
    time_count+=1

    clock.tick(fps_rate)
    fps=clock.get_fps()
    # # ---save screenshot---
    # pygame.image.save(screen, "screenshot.png")

pygame.quit()



