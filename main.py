import pygame
import sys
import json
import mapload
from pygame.locals import QUIT

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*45, 14*45))
clock = pygame.time.Clock()
fps = 120

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class player:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.playerrect = pygame.Rect((0,0),(10,10))

    def playermove(self):
        self.keys = pygame.key.get_pressed()

        self.BoolToInt = {True: 0, False: 1}
        self.movevector = pygame.math.Vector2( ( self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]] ), ( self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]] ) )

        self.temp = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + self.movevector.x, self.playerrect.y + self.movevector.y))
        if self.tilemap.currentlevel[int(self.temp.y)][int(self.temp.x)] == 0:
            self.playerrect.x += self.movevector.x
            self.playerrect.y += self.movevector.y

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, pygame.Color(150,0,150), player.playerrect) 

class tilemap:
    def __init__(self,map):
        self.currentlevel = map

    def drawlevel(self):
        tempcolor = [pygame.Color(50,150,0), pygame.Color(50,0,0), pygame.Color(0,150,150)]
        for i in range(len(self.currentlevel)):
            for j in range(len(self.currentlevel[i])):
                tilerect = ( (j*45, i*45), (45,45) )
                pygame.draw.rect(screen, tempcolor[self.currentlevel[i][j]], tilerect) 

    def global_to_map(self, vector):
        x = int((vector.x + 5) // 45)
        y = int((vector.y + 5) // 45)
        return pygame.math.Vector2(x, y)

def pygametext(txt):
    sans = pygame.font.SysFont('Comic Sans MS', 20)
    return sans.render(txt, False, (0, 0, 0))

def loadjson(f):
    with open(f, 'rb') as file:
        o = json.load(file)
    return o

tilemap = tilemap(mapload.buildmap(mapload.loadrawdata(f'local.map')))
player = player(tilemap)

processes = [tilemap.drawlevel, player.playermove]

while True:
    screen.fill((34, 34, 34))

    for process in processes:
        process()

    screen.blit( pygametext( 'X: ' + str(tilemap.global_to_map(player.playerrect).x) + ' Y: ' + str(tilemap.global_to_map(player.playerrect).y) ) , (1,1,1,1))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))
    pygame.display.update()
    clock.tick(fps)
