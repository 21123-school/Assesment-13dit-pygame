import pygame
import sys
import json
from pygame.locals import QUIT

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*45, 14*45))
clock = pygame.time.Clock()
fps = 120

playerrect = pygame.Rect((0,0),(10,10))

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class tilemap:
    def __init__(self):
        self.currentlevel= [
            [0,0,0,0,0,0],
            [0,1,2,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,1,0,0],
            [0,0,0,0,0,0],
            ]

    def drawlevel(self):
        tempcolor = [pygame.Color(50,150,0), pygame.Color(50,0,0), pygame.Color(0,150,150)]
        for i in range(len(self.currentlevel)):
            for j in range(len(self.currentlevel[i])):
                tilerect = ( (j*45, i*45), (45,45) )
                pygame.draw.rect(screen, tempcolor[self.currentlevel[i][j]], tilerect) 

    def map_to_global(self, vector):
        x = int(str((vector.x + 5) / 45)[0])
        y = int(str((vector.y + 5) / 45)[0])
        return pygame.math.Vector2(x, y)

def pygametext(txt):
    sans = pygame.font.SysFont('Comic Sans MS', 20)
    return sans.render(txt, False, (0, 0, 0))

def loadjson(f):
    with open(f, 'rb') as file:
        o = json.load(file)
    return o

def playermove():
    pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))
    global keys
    
    test = {True: 0, False: 1}

    movevector = pygame.math.Vector2( ( test[keys[pygame.K_a]] + 0 - test[keys[pygame.K_d]] ) , ( test[keys[pygame.K_w]] + 0 - test[keys[pygame.K_s]] ) )

    playerrect.x += movevector.x
    playerrect.y += movevector.y

tilemap = tilemap()

while True:
    keys = pygame.key.get_pressed()

    screen.fill((34, 34, 34))

    tilemap.drawlevel()

    playermove()

    screen.blit( pygametext( 'X: ' + str(tilemap.map_to_global(playerrect).x) + ' Y: ' + str(tilemap.map_to_global(playerrect).y) ) , (1,1,1,1))

    pygame.draw.rect(screen, pygame.Color(150,0,150), playerrect) 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    

    pygame.display.update()
    clock.tick(fps)
