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
        nombre = i*rows + j
        squares[-1]['name'] = nombre
        squares[-1]['color'] = (nombre % 5**3, nombre % 5**2, nombre % 5)
        

i = 0
for rr in squares:
    pygame.draw.rect(windowSurface, rr['color'], rr['rect'])
    i += 2



pygame.display.update()
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            locale = pygame.mouse.get_pos()
            for rr in squares:
                if rr['rect'].collidepoint(locale):
                    True
                    
                    
                
            
        
pygame.quit()
