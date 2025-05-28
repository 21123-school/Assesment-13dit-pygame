import pygame
import sys
import json
from pygame.locals import QUIT

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*45, 14*45))
clock = pygame.time.Clock()
fps = 120

sans = pygame.font.SysFont('Comic Sans MS', 20)
start = sans.render('test', False, (0, 0, 0))

playerrect = pygame.rect(10,10,10,10)

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

def loadjson(f):
    with open(f, 'rb') as file:
        o = json.load(file)
    return o

def drawlevel():
    currentlevel = [
        [0,0,0,0],
        [0,1,2,0],
        [0,0,0,0],
        ]

    for i in range(len(currentlevel)):

        for j in range(len(currentlevel[i])):

            tilerect = ( (j*45, i*45), (45,45) )

            if currentlevel[i][j] == 0:
                pygame.draw.rect(screen, pygame.Color(50,150,0), tilerect) 

            elif currentlevel[i][j] == 1:
                pygame.draw.rect(screen, pygame.Color(150,150,150), tilerect) 
            elif currentlevel[i][j] == 2:
                pygame.draw.rect(screen, pygame.Color(150,0,150), tilerect) 

def playermove():
    pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))
    global keys

    if keys[pygame.K_w]:
        playerrect.y += -10

while True:
    keys = pygame.key.get_pressed()

    screen.fill((34, 34, 34))

    drawlevel()
    playermove()

    screen.blit(start, (1,1,1,1))

    pygame.draw.rect(screen, pygame.Color(150,0,150), playerrect) 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    

    pygame.display.update()
    clock.tick(fps)
