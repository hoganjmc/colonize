## The goal here is to draw the board so I can finally look at it.

import pygame, sys
from pygame.locals import *

pygame.init()

rows = 11
cols = 11

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50

WINDOW_WIDTH = cols * BLOCK_WIDTH
WINDOW_HEIGHT = rows * BLOCK_HEIGHT + 100

windowSurface = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) , 0, 32)
pygame.display.set_caption("Hello and good luck.")
squares = []
color_flag = False
for i in range(rows):
    for j in range(cols):        
        squares.append( {'rect':pygame.Rect(j*BLOCK_WIDTH,i*BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)} )
        if color_flag:
            squares[-1]['color'] = (0,0,0)
        else:
            squares[-1]['color'] = (150,150,150)
        color_flag = not(color_flag)
        squares[-1]['name'] = i*rows + j
        #squares[-1]['color'] = 
        

i = 0
for rr in squares:
    pygame.draw.rect(windowSurface, rr['color'], rr['rect'])
    i += 2



pygame.display.update()
clicks = 0
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            locale = pygame.mouse.get_pos()
            for rr in squares:
                if rr['rect'].collidepoint(locale):
                    rr['color'] = (200+clicks,200+clicks,200+clicks)
                    pygame.draw.rect(windowSurface, rr['color'], rr['rect'])
                    pygame.display.update()
                    print rr['name']
                    clicks = (clicks +1 ) % 5
                    print clicks
                    
                
            
        
pygame.quit()
