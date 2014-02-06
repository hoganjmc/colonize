## Goal 1: Draw the board? Success.

import pygame, sys
from pygame.locals import *

pygame.init()

#A Star is a hex block, and always counts for 4x the block height.
star_rows = 2
star_cols = 3
rows = star_rows * 5 + 1
cols = star_cols * 5 + 1

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (150,150,150)
GREY = GRAY # Huh? Oh, right.  (Just in case.)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
AQUA = (0,255,255)
FUSCHIA = (255,0,255)
YELLOW = (255,255,0)
CORN = (100,150,240)
basicFont = pygame.font.SysFont(None, 28)

#Window size = 725 tall x 1000
WIDTH_OFFSET = 25
HEIGHT_OFFSET = 25
CARD_HEIGHT = 100
READ_WIDTH = 175 #Zooms in on the clicked thing.
READ_HEIGHT = 175 #i.e., a picture of the thing the player has most recently clicked.
BLOCK_HEIGHT = (725 - 3*HEIGHT_OFFSET - CARD_HEIGHT) / rows
BLOCK_WIDTH = BLOCK_HEIGHT
CARD_WIDTH = CARD_HEIGHT * 2 / 3
HEX_BLOCK_HEIGHT = BLOCK_HEIGHT * 4
HEX_BLOCK_WIDTH = HEX_BLOCK_HEIGHT
CARD_OFFSET = 15
WINDOW_WIDTH = cols * BLOCK_WIDTH + 2*WIDTH_OFFSET + READ_WIDTH
WINDOW_HEIGHT = rows * BLOCK_HEIGHT + HEIGHT_OFFSET * 3 + CARD_HEIGHT 

print BLOCK_HEIGHT
print BLOCK_HEIGHT * rows

windowSurface = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) , 0, 32)
pygame.display.set_caption("Hello and good luck.")

def distance( a, b):
#a, b are (x,y) tuples, please.
    return ( (a[0] - b[0])**2 + ( a[1] - b[1] ) **2) **.5
def find_min_index( listo):
# listo is a list of positive floats.
    if listo[0]>= 0: maxo = listo[0]
    for i in range(len(listo)):
        if listo[i] <= maxo:
            dex = i
            maxo = listo[i]
    return dex


#the rect argument takes in Rect objects. kind takes in one of the types utilized so far.
#color is a color tuple.
#Function first draws the shape, then returns the rectangle it's inscribed in.

def redraw(dicto,color):
    kind = dicto['type']
    rect = dicto['rect']
    if kind == 'square':
        pygame.draw.rect(windowSurface, color, rect)
        return rect
    elif kind == 'hex_nw' or kind == 'hex_sw':
        return pygame.draw.polygon(windowSurface, color,
                            ( rect.topleft,
                              (rect.left + BLOCK_WIDTH , rect.top),
                              rect.midright,
                              (rect.left + BLOCK_WIDTH , rect.bottom),
                              rect.bottomleft))
    elif kind == 'hex_n':
        return pygame.draw.polygon(windowSurface, color,
                            ( rect.topleft,
                              rect.topright,
                              (rect.right - BLOCK_HEIGHT / 2, rect.bottom),
                              (rect.left + BLOCK_HEIGHT / 2, rect.bottom) ))
    elif kind == 'hex_ne' or kind == 'hex_se':
        return pygame.draw.polygon(windowSurface, color,
                            ( (rect.right - BLOCK_WIDTH, rect.top),
                              rect.topright,
                              rect.bottomright,
                              (rect.right - BLOCK_WIDTH, rect.bottom),
                              rect.midleft) )
    elif kind == 'hex_s':
        return pygame.draw.polygon(windowSurface, color,
                            ( rect.bottomright,
                              rect.bottomleft,
                              (rect.left + BLOCK_WIDTH/2, rect.top),
                              (rect.right - BLOCK_WIDTH / 2, rect.top) ) )
    elif kind == 'hex_center':
        return pygame.draw.polygon(windowSurface, color,
                            ( (rect.left + BLOCK_WIDTH/2, rect.top),
                              (rect.right - BLOCK_WIDTH/2, rect.top),
                              rect.midright,
                              (rect.right - BLOCK_WIDTH/2, rect.bottom),
                              (rect.left + BLOCK_WIDTH/2, rect.bottom),
                              rect.midleft) )
        

#1. Draw the border squares. We use mod 5 here because the HEX height is 4, so we should
#   only need squares specifically at Row #0, #4+1, etc.
#Remember: squares[] contains dictionaries, with relevant data hashed. 
color_flag = False
squares = []
for i in range(rows):
    if star_cols%2 == 1: color_flag = not(color_flag)
    for j in range(cols):
        if (i * j) % 5 == 0:
            squares.append( {'rect': pygame.Rect(i*BLOCK_WIDTH + WIDTH_OFFSET, j*BLOCK_HEIGHT + HEIGHT_OFFSET, BLOCK_WIDTH, BLOCK_HEIGHT) } )
            if color_flag:
                squares[-1]['color'] = WHITE
            else:
                squares[-1]['color'] = GRAY
            squares[-1]['type'] = 'square'
            squares[-1]['special'] = 'none'
            color_flag = not(color_flag)
            
for rr in squares:
    pygame.draw.rect(windowSurface, rr['color'], rr['rect'])

#2. Draw the hex-type spaces.
hexes = []
for i in range(rows/5):
    for j in range(cols/5):
        hex_x = BLOCK_WIDTH + i*(HEX_BLOCK_WIDTH + BLOCK_WIDTH)+WIDTH_OFFSET
        hex_y = BLOCK_HEIGHT + j*(HEX_BLOCK_HEIGHT + BLOCK_HEIGHT)+HEIGHT_OFFSET
        
        northwest = pygame.draw.polygon(windowSurface, GREEN,
                                ( (hex_x, hex_y),
                                  (hex_x+BLOCK_WIDTH, hex_y),
                                  (hex_x+BLOCK_WIDTH*1.5, hex_y+BLOCK_HEIGHT),
                                  (hex_x+BLOCK_WIDTH, hex_y+ 2*BLOCK_HEIGHT),
                                  (hex_x, hex_y + 2*BLOCK_HEIGHT) )  )
        hexes.append( {'type':'hex_nw', 'rect':northwest,'color':GREEN,'special':'none'} )
        
        north = pygame.draw.polygon(windowSurface, BLUE,
                                (  (hex_x + BLOCK_WIDTH, hex_y),
                                   (hex_x + 3 * BLOCK_WIDTH, hex_y),
                                   (hex_x + BLOCK_WIDTH * 2.5, hex_y+BLOCK_HEIGHT),
                                   (hex_x + BLOCK_WIDTH*1.5, hex_y+BLOCK_HEIGHT) ) )
        hexes.append( {'type':'hex_n', 'rect':north,'color':BLUE,'special':'none'} )
        
        northeast = pygame.draw.polygon(windowSurface, YELLOW,
                                ( (hex_x + 3 * BLOCK_WIDTH, hex_y),
                                  (hex_x + 4 * BLOCK_WIDTH, hex_y),
                                  (hex_x + 4 * BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 3 * BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 2.5 * BLOCK_WIDTH, hex_y + BLOCK_HEIGHT) ))
        hexes.append( {'type':'hex_ne', 'rect':northeast, 'color':YELLOW,'special':'none'})
        
        southeast = pygame.draw.polygon(windowSurface, AQUA,
                                ( (hex_x + 2.5 * BLOCK_WIDTH, hex_y + 3*BLOCK_HEIGHT),
                                  (hex_x + 3 * BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 4 * BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 4 * BLOCK_WIDTH, hex_y + 4 * BLOCK_WIDTH),
                                  (hex_x + 3 * BLOCK_WIDTH, hex_y + 4 * BLOCK_WIDTH) ))
        hexes.append( {'type':'hex_se', 'rect':southeast,'color':AQUA,'special':'none'} )
        south = pygame.draw.polygon(windowSurface, FUSCHIA,
                                ( (hex_x + 3 * BLOCK_WIDTH, hex_y + 4 * BLOCK_WIDTH),
                                  (hex_x + 2.5 * BLOCK_WIDTH, hex_y + 3*BLOCK_HEIGHT),
                                  (hex_x + 1.5 * BLOCK_WIDTH, hex_y + 3*BLOCK_HEIGHT),
                                  (hex_x + BLOCK_WIDTH, hex_y + 4 * BLOCK_WIDTH) ))
        hexes.append( {'type':'hex_s', 'rect':south, 'color':FUSCHIA,'special':'none'} )
        southwest = pygame.draw.polygon(windowSurface, CORN,
                                ( (hex_x + BLOCK_WIDTH, hex_y + 4 * BLOCK_WIDTH),
                                  (hex_x + 1.5 * BLOCK_WIDTH, hex_y + 3*BLOCK_HEIGHT),
                                  (hex_x + BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x, hex_y + 4 * BLOCK_HEIGHT) ))
        hexes.append( {'type':'hex_sw', 'rect':southwest, 'color':CORN,'special':'none'} )
        center = pygame.draw.polygon(windowSurface, WHITE,
                                ( (hex_x + BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 1.5 * BLOCK_WIDTH, hex_y + BLOCK_HEIGHT),
                                  (hex_x + 2.5 * BLOCK_WIDTH, hex_y + BLOCK_HEIGHT),
                                  (hex_x + 3* BLOCK_WIDTH, hex_y + 2 * BLOCK_HEIGHT),
                                  (hex_x + 2.5 * BLOCK_WIDTH, hex_y + 3 * BLOCK_HEIGHT),
                                  (hex_x + 1.5 * BLOCK_WIDTH, hex_y + 3 * BLOCK_HEIGHT) ))
        hexes.append( {'type':'hex_center', 'rect':center, 'color':WHITE,'special':'none'} )
        
#3. Draw the hands/options.        

cards = []
card_types = ['adventurer', 'diplomat', 'prospector', 'conqueror', 'fanatic']
cards_y = WINDOW_HEIGHT - CARD_HEIGHT - HEIGHT_OFFSET / 2
cards_x = WIDTH_OFFSET / 2
for i in range(len(card_types)):
    cards.append( {'type':card_types[i]} )
    cards[-1]['rect'] = pygame.Rect( cards_x + i*CARD_WIDTH + CARD_OFFSET*i, cards_y, CARD_WIDTH, CARD_HEIGHT)
    cards[-1]['color'] = GRAY
    cards[-1]['name'] = card_types[i][:5]

for j in cards:
      pygame.draw.rect(windowSurface, j['color'], j['rect'])
      text = basicFont.render(j['name'], True, WHITE, GRAY)
      windowSurface.blit(text,j['rect'].move(4,4))
      
pygame.display.update()
game_on = True
click_flag = False
clicks = 0
card_clicked = 'none'

## Begin the game loop
while game_on:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:

            locale = pygame.mouse.get_pos()
            for rr in squares:
                if rr['rect'].collidepoint(locale):
                    if card_clicked == 'none':
                        print "It's a " + rr['special']
                    else:
                        rr['special'] = card_clicked
                        print "Turned to " + rr['special']
                        card_clicked = 'none'
                        
            boxes = []
            distances = []
            for hh in hexes:
                if hh['rect'].collidepoint(locale):
                    boxes.append(hh['rect'])
                    distances.append( distance( hh['rect'].center, locale))
            if len(boxes) > 0 :
                target = boxes[find_min_index(distances)]
                for hh in hexes:
                    if hh['rect'] == target:
                        if card_clicked != 'none':
                            redraw(hh, (20,40,100) )
                            hh['special'] = card_clicked
                            card_clicked = 'none'
                            print "Turned to " + hh['special']
                        else:
                            print "It's a " + hh['special']
                            
                            
            for card in cards:
                if card['rect'].collidepoint(locale):
                    card_clicked = card['type']
                    
                        
            pygame.display.update()
        
pygame.quit()

## So, here's an idea.
## Tiles have atk and def.
## You start with gold or money or w/e, which you spend to play tiles.
## Certain tiles give you money. You get money for capturing a tile, and some per turn.
## The game's over when some condition is met. I like the idea of the central hexes
##  providing the game end conditions.
## So like:
##  "prospector" has these abilities on 6: +1 gold/turn, +1 gold/turn to the winner
