import select
import mapload  # custom
import pygame
import sys
import math
from pygame.locals import QUIT

# basic math definitions
size = 2
aspect = (16, 9)
cellsize = 32
halfcellsize = cellsize / 2

# camera
camera = pygame.Rect(0, 0, 0, 0)
starthp = 3

# pygame set up
pygame.init()

clock = pygame.time.Clock()
fps = 120
dt = 1

class players:
    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.speed = 2
        self.playerrect = pygame.Rect((0,0),(10, 10))

    def playermove(self):
        self.keys = pygame.key.get_pressed()

        self.BoolToInt = {True: 0, False: self.speed}
        self.movevector = pygame.math.Vector2((self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]]),(self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]]))
        self.playerrect.x += self.movevector.x
        self.playerrect.y += self.movevector.y

class tilemaps:
    def __init__(self, map):
        # get local verson of textures
        self.currentlevel = map
        self.textures = list(texture.values())

    def drawlevel(self):
        # display tile if texture available for tile *note map doesn't have to be square
        for i in range(len(self.currentlevel)):
            for j in range(len(self.currentlevel[0])):
                self.tilerect = pygame.Rect(((j * cellsize) + camera.x, (i * cellsize) + camera.y),(cellsize, cellsize),)
                try:
                    screen.blit(self.textures[self.currentlevel[i][j]], self.tilerect)
                except:
                    pass

    def global_to_map(self, vector):
        # converts global units to tilemap coords
        x = int((vector.x + halfcellsize) // cellsize)
        y = int((vector.y + halfcellsize) // cellsize)
        return pygame.math.Vector2(x, y)


texture = {}
for i in mapload.ZipFile('debug.pak', "r").namelist():
    if i.startswith(f"debug/textures/") and i.endswith(".bmp"):
        texture[i.split("/")[-1].split(".")[0]] = pygame.image.load(mapload.loadpakitem('debug.pak', i))
    elif i.startswith(f"debug/textures/") and i.endswith(".png"):
        texture[i.split("/")[-1].split(".")[0]] = pygame.image.load(mapload.loadpakitem('debug.pak', i))

def save(level):
    if input('save?: [Y/n]').lower() == 'y':
        scramble = {'g':0,'f':1,'t':2,'s':3,'e':4,'m':8,'b':5}
        newlevel = ''

        unscramble = dict([(value, key) for key, value in scramble.items()])

        for y in range(len(level)):
            for x in range(len(level[0])):
                newlevel = newlevel + str(unscramble[level[y][x]])
            newlevel = newlevel + 'm'
            
        newlevel = newlevel + 'x' + input('nextlevel name: ')
        
        newlevel = newlevel + 'q' + input('message name: ')
        
        print(newlevel)
        
        with open('.\\data\\maps\\' + input('name of current level: '), 'w') as f:
            f.write(newlevel)

try:
    n = input('loadmap: ')
    with open(f'.\data\maps\{n}', 'r') as file:
        read = file.read()
    newmap, nextlevel = mapload.buildmap(read)
except:
    newmap = []
    tem = []
    for x in range(int(input('x: '))):
        tem.append(3)
    for y in range(int(input('y: '))):
        newmap.append(tem)

    newmap = str(newmap)
    newmap = eval(newmap)

screen = pygame.display.set_mode(((aspect[0] * size) * cellsize, (aspect[1] * size) * cellsize))

tilemap = tilemaps(newmap)
player = players(tilemap)
selected = 0

while True:
    # center camera
    camera.x = 0 - player.playerrect.x + (aspect[0] * cellsize) - cellsize
    camera.y = 0 - player.playerrect.y + (aspect[1] * (cellsize * 1.25)) - (cellsize * 1.25)

    screen.fill(pygame.Color(11, 11, 11))  # to be removed

    tilemap.drawlevel()
    player.playermove()

    keys = pygame.key.get_pressed()

    mx, my = pygame.mouse.get_pos()
    mx, my = tilemap.global_to_map(pygame.Vector2(round(mx) - camera.x - halfcellsize, round(my) - camera.y - halfcellsize))
    
    if pygame.mouse.get_pressed()[0]:
        tilemap.currentlevel[int(my)][int(mx)] = selected

    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            selected += event.y
            if selected > len(list(texture.values())) - 1:
                selected = 0
            elif selected < 0:
                selected = len(list(texture.values())) - 1

    screen.blit(list(texture.values())[selected], (0,0))

    if keys[pygame.K_SPACE]:
        save(tilemap.currentlevel)

    # idk what this does but if i remove it pygame crashes
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # displays fps on title bar
    pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))

    # update pygame and get deltatime
    pygame.display.update()
    dt = clock.tick() / 100
