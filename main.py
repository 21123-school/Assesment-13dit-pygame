import mapload  # custom
import pygame
import sys
import math
import socket
from pygame.locals import QUIT

# basic math definitions
size = 2
aspect = (16,  9)
cellsize = 32
halfcellsize = cellsize / 2

# camera
camera = pygame.Rect(0,  0,  0,  0)
starthp = 2

# pygame set up
pygame.init()

screen = pygame.display.set_mode(((aspect[0] * size) * cellsize,  (aspect[1] * size) * cellsize))

clock = pygame.time.Clock()
fps = 120
dt = 1

# functions

def pygametext(txt):
    # sets up text for display
    sans = pygame.font.SysFont("Comic Sans MS",  20)
    return sans.render(txt,  False,  (155,  155,  155))


def loadnewlevel(nextlevel, nextlevelrand="null", starthp=3, message='q'):
    level = nextlevel
    
    nonplayer = []

    # puts all sounds of type *.wav into a dictionary
    sound = {}
    for i in mapload.ZipFile(sys.argv[1],  "r").namelist():
        if i.startswith(f"{arg}/sounds/") and i.endswith(".wav"):
            sound[i.split("/")[-1].split(".")[0]] = pygame.mixer.Sound(
                mapload.loadpakitem(sys.argv[1],  i)
            )

    # puts all images of type *bmp/*.png into a dictionary
    texture = {}
    for i in mapload.ZipFile(sys.argv[1],  "r").namelist():
        if i.startswith(f"{arg}/textures/") and i.endswith(".bmp"):
            texture[i.split("/")[-1].split(".")[0]] = pygame.image.load(
                mapload.loadpakitem(sys.argv[1],  i)
            )
        elif i.startswith(f"{arg}/textures/") and i.endswith(".png"):
            texture[i.split("/")[-1].split(".")[0]] = pygame.image.load(
                mapload.loadpakitem(sys.argv[1],  i)
            )

    # resets processes loop remakes the tilemap,  and player objects and gets name of next level
    if nextlevelrand == "null":
        newmap,  nextlevel,  message = mapload.buildmap(mapload.loadpaktext(sys.argv[1],  f"{arg}/maps/{nextlevel}"))
    else:
        newmap,  nextlevel,  message = mapload.buildmap(mapload.loadpaktext(sys.argv[1],  f"{arg}/maps/{nextlevelrand}"))

    tilemap = tilemaps(texture, newmap)

    try:
        player = players(texture, sound, tilemap,  player.hp)
    except:
        player = players(texture, sound, tilemap,  starthp)

    processes = [tilemap.drawlevel,  player.playermove]

    tempspawn = []
    for y in range(len(tilemap.currentlevel)):
        for x in range(len(tilemap.currentlevel[0])):
            if tilemap.currentlevel[y][x] == 5:
                tempspawn.append([x,  y])
    for i in range(len(tempspawn)):
        nonplayer.append(nonplayers(texture,  tilemap,  int(tempspawn[i][0]),  int(tempspawn[i][1])))
        processes.append(nonplayer[-1].playermove)

    return nextlevel,  newmap,  camera,  tilemap,  player,  processes,  sound,  texture,  level,  nonplayer,  message

# classes

class players:
    def __init__(self,  texture,  sound,  tilemap,  hp=3):
        # vars set up
        self.sound = sound
        self.hp = hp
        self.isonfloor = False
        self.velocityY = 0
        self.velocityX = 0
        self.moving = True
        self.animation = True
        self.currentanimationdelay = 0
        self.tilemap = tilemap
        self.lasttime = 0
        self.direction = 1
        self.maxfallspeed = 100
        self.maxspeed = 40
        self.gravity = 25
        self.jumphight = -75
        self.speed = 15

        try:
            # setup player rect
            self.playeranimations = [
                pygame.transform.scale(texture["playerstand"],  (cellsize,  cellsize)), 
                pygame.transform.scale(texture["playerwalk"],  (cellsize,  cellsize)), 
            ]
        except:
            pass

        self.playerrect = pygame.Rect((len(self.tilemap.currentlevel[0]) * halfcellsize - halfcellsize, len(self.tilemap.currentlevel) * halfcellsize - halfcellsize,  ), (10,  10))

        # find map start tile if available
        for y in range(len(self.tilemap.currentlevel)):
            for x in range(len(self.tilemap.currentlevel[0])):
                if self.tilemap.currentlevel[y][x] == 0:
                    self.start = pygame.math.Vector2(x * cellsize,  y * cellsize)
                    self.playerrect.x = self.start.x
                    self.playerrect.y = self.start.y
                    return

    def move_towards(self,  mfrom,  mto,  bmuch):
        if abs(mto - mfrom) <= bmuch:
            return mto
        direction = int(math.copysign(1,  mto - mfrom))
        return mfrom + direction * bmuch

    def hitbox(self,  tile):
        self.collisions = [pygame.Vector2(self.playerrect.x + 16,  self.playerrect.y),  pygame.Vector2(self.playerrect.x + 16,  self.playerrect.y + 32),  pygame.Vector2(self.playerrect.x + 6,  self.playerrect.y + 18),  pygame.Vector2(self.playerrect.x + 26,  self.playerrect.y + 18) ] 
        self.hits = []
        for i in range(len(self.collisions)):
            self.hit = pygame.math.Vector2(self.collisions[i].x / 32,  self.collisions[i].y / 32)
            if self.tilemap.currentlevel[max(0,  min(len(self.tilemap.currentlevel) - 1,  int(self.hit.y)))][max(0,  min(len(self.tilemap.currentlevel[0]) - 1,  int(self.hit.x)))] == tile:
                self.hits.append(i)
        return self.hits

    def died(self):
        self.sound["hit"].play()
        self.playerrect.x = self.start.x
        self.playerrect.y = self.start.y
        self.hp -= 1

    def playermove(self):
        # sets animation to run 8 times a second i hope
        self.animationdelay = int(clock.get_fps()) / 8
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_0]:
            try:
                mapload.savefile(sys.argv[2],  level,  self.hp)
            except:
                mapload.savefile("",  level,  self.hp)

        # used for converting the bools from keys[pygame.K_*]] into movement speed
        self.BoolToInt = {True: 0,  False: self.speed}
        # gets wasd into a vector
        self.movevector = pygame.math.Vector2((self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]]), (self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]]), )

        if self.movevector.x != 0 and abs(self.velocityX) < self.maxspeed:
            self.velocityX = self.move_towards(self.velocityX,  self.maxspeed * self.direction,  self.speed * dt)
            if abs(self.velocityX) < 2:
                self.velocityX = self.move_towards(self.velocityX,  self.maxspeed * self.direction,  (self.speed * dt) * 6)
        else:
            if self.isonfloor == True:
                self.velocityX = self.move_towards(self.velocityX,  0,  (self.speed * 1.5) * dt)
            else:
                self.velocityX = self.move_towards(self.velocityX,  0,  self.speed * dt)
        
        # do gravity acceleration or jump
        if not self.velocityY >= self.maxfallspeed:
            self.velocityY += self.gravity * dt
        if (self.keys[pygame.K_w] or self.keys[pygame.K_SPACE]) and self.isonfloor:
            self.sound["jump"].play()
            self.playerrect.y -= 1 
            self.velocityY += self.jumphight

        self.isonfloor = False
        
        # checks if level end reacheds
        if self.hitbox(4):
            self.died()
        # checks if off solid tile if yes gravity added if not reset velocityY and check if solid tile it roof if no is on floor true
        if not (1 in self.hitbox(2) or 0 in self.hitbox(2)):
            self.playerrect.y += self.velocityY * dt
        else:
            if not 0 in self.hitbox(2):
                self.isonfloor = True
                while 1 in self.hitbox(2):
                    self.playerrect.y += -1
                self.playerrect.y += 1
            else:
                self.playerrect.y += 1
            self.velocityY = 0

        # checks if moving will put you in wall if not move
        if not (2 in self.hitbox(2) or 3 in self.hitbox(2)):
            self.playerrect.x += self.velocityX * dt
        else:
            self.playerrect.x += int(int(2 in self.hitbox(2)) - int(3 in self.hitbox(2)))
            self.velocityX = 0

        self.draw()

    def draw(self):
        # if moving update direction
        if self.movevector.x != 0:
            self.direction = math.copysign(1,  self.movevector.x)

        # if moving or jumping use walking animation if not use standing sprite
        if self.movevector.x != 0:
            if self.direction < 0:
                screen.blit(pygame.transform.flip(self.playeranimations[{True: 1,  False: 0}[self.animation]], True, False, ), (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))
            else:
                screen.blit(self.playeranimations[{True: 1,  False: 0}[self.animation]], (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))

            # if animation needs to change flip animation
            if self.currentanimationdelay >= self.animationdelay:
                self.animation = not self.animation
                self.currentanimationdelay = 0
                self.sound["walk"].play()
            else:
                self.currentanimationdelay += 1
        else:
            if self.direction < 0:
                screen.blit(pygame.transform.flip(self.playeranimations[0],  True,  False), (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))
            else:
                screen.blit(self.playeranimations[0], (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))


class nonplayers:
    def __init__(self,  texture, tilemap,  x,  y,  hp=3):
        # vars set up
        self.texture = texture
        self.hp = hp
        self.isonfloor = False
        self.velocityY = 0
        self.velocityX = 0
        self.moving = True
        self.animation = True
        self.currentanimationdelay = 0
        self.tilemap = tilemap
        self.direction = 1
        self.maxfallspeed = 100
        self.gravity = 25
        self.maxspeed = 20
        self.speed = self.maxspeed

        try:
            # setup player rect
            self.playeranimations = [
                pygame.transform.scale(texture["nonplayerstand"],  (cellsize,  cellsize)), 
                pygame.transform.scale(texture["nonplayerwalk"],  (cellsize,  cellsize)), 
            ]
        except:
            pass
        self.playerrect = pygame.Rect((x * cellsize,  y * cellsize),  (10,  10))

    def move_towards(self,  mfrom,  mto,  bmuch):
        if abs(mto - mfrom) <= bmuch:
            return mto
        direction = int(math.copysign(1,  mto - mfrom))
        return mfrom + direction * bmuch

    def playermove(self):
        # sets animation to run 8 times a second i hope
        self.animationdelay = int(clock.get_fps()) / 8

        self.movevector = pygame.math.Vector2(self.direction,  0)

        # do gravity acceleration or jump
        if not self.isonfloor:
            self.velocityY += self.gravity * dt

        if player.playerrect.colliderect(self.playerrect):
            player.died()

        self.isonfloor = False

        # used for collison math converts global coords to tilemap coords with some modifiers
        self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + (13 * self.direction),  self.playerrect.y + 14))
        self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + (self.velocityY * dt) + halfcellsize))

        self.tempx.x = max(0,  self.tempx.x)
        self.tempx.x = min(len(self.tilemap.currentlevel[0]) - 1,  self.tempx.x)
        self.tempx.y = max(0,  self.tempx.y)
        self.tempx.y = min(len(self.tilemap.currentlevel) - 1,  self.tempx.y)
        self.tempy.x = max(0,  self.tempy.x)
        self.tempy.x = min(len(self.tilemap.currentlevel[0]) - 1,  self.tempy.x)
        self.tempy.y = max(0,  self.tempy.y)
        self.tempy.y = min(len(self.tilemap.currentlevel) - 1,  self.tempy.y)

        if self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
            self.playerrect.y += self.velocityY * dt
        else:
            if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tempy.x)]!= 2:
                self.isonfloor = True
            self.velocityY = 0

        if self.movevector.x != 0 and abs(self.velocityX) < self.maxspeed:
            self.velocityX = self.move_towards(self.velocityX,  self.maxspeed * self.direction,  self.speed)
        else:
            self.velocityX = self.move_towards(self.velocityX,  0,  self.speed)
            
        # checks if moving will put you in wall if not move
        if self.tilemap.currentlevel[int(self.tempx.y)][int(self.tempx.x)] != 2 and self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] == 2:
            self.playerrect.x += self.velocityX * dt
        else:
            self.direction = 0 - self.direction
            self.velocityX = self.move_towards(self.velocityX,  self.maxspeed * self.direction,  self.speed)
            self.playerrect.x += self.velocityX * dt
            
        if self.playerrect.x + camera.x > camera.x and self.playerrect.x + camera.x < ((aspect[0] * size) * cellsize):
            self.draw()

    def draw(self):
        if self.direction < 0:
            screen.blit(pygame.transform.flip( self.playeranimations[{True: 1,  False: 0}[self.animation]], True, False, ), (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))
        else:
            screen.blit(self.playeranimations[{True: 1,  False: 0}[self.animation]],  (self.playerrect.x + camera.x,  self.playerrect.y + camera.y))

        # if animation needs to change flip animation
        if self.currentanimationdelay >= self.animationdelay:
            self.animation = not self.animation
            self.currentanimationdelay = 0
        else:
            self.currentanimationdelay += 1


class tilemaps:
    def __init__(self,  texture,  map):
        # get local verson of textures
        self.currentlevel = map
        self.textures = list(texture.values())

    def drawlevel(self):
        start_row = max(0,  int(0 - self.global_to_map(camera).y))
        end_row = min(len(self.currentlevel), int(self.global_to_map(pygame.math.Vector2(0,  abs(camera.y - (aspect[1] * size) * cellsize))).y) + 1)

        start_column = max(0,  int(0 - self.global_to_map(camera).x))
        end_column = min(len(self.currentlevel[0]), int(self.global_to_map(pygame.math.Vector2(abs(camera.x - (aspect[0] * size) * cellsize),  0)).x) + 1)

        # display tile if texture available for tile *note map doesn't have to be square
        for i in range(start_row,  end_row):
            for j in range(start_column,  end_column):
                self.tilerect = pygame.Rect(((j * cellsize) + camera.x,  (i * cellsize) + camera.y), (cellsize,  cellsize))
                try:
                    if self.currentlevel[i][j] == 4 or self.currentlevel[i][j] == 0 or self.currentlevel[i][j] == 1:
                        if self.currentlevel[i - 1][j] != 2:
                            screen.blit(self.textures[self.currentlevel[i - 1][j]],  self.tilerect)
                        else:
                            screen.blit(self.textures[3],  self.tilerect)
                        
                    screen.blit(self.textures[self.currentlevel[i][j]],  self.tilerect)
                    
                    if self.currentlevel[i][j] == 5:
                        screen.blit(self.textures[self.currentlevel[i - 1][j]],  self.tilerect)
                except:
                    pass

    def global_to_map(self,  vector):
        # converts global units to tilemap coords
        x = int((vector.x + halfcellsize) // cellsize)
        y = int((vector.y + halfcellsize) // cellsize)
        return pygame.math.Vector2(x,  y)

# main

# find used *.pak
arg = str(sys.argv[1]).split(".")[0]
# set starting map
level = ""
nextlevel = "a1m1.map"

nextlevel,  newmap,  camera,  tilemap,  player,  processes,  sound,  texture,  level,  nonplayer,  message = loadnewlevel(nextlevel,  nextlevel)

levelnum = 1

host = sys.argv[2]
port = 49152
client_socket = socket.socket()
client_socket.connect((host,  port))
client_id = client_socket.recv(1024)
clientdatalist = {}
clientanimations = [pygame.transform.scale(texture["playerstand"],  (cellsize,  cellsize)),  pygame.transform.scale(texture["playerwalk"],  (cellsize,  cellsize))]
clientanimation = True
clientcurrentanimationdelay = 0
clientanimationdelay = 60
clientname = sys.argv[3]
    
while True:
    # center camera
    camera.x = 0 - player.playerrect.x + (aspect[0] * cellsize) - cellsize
    camera.y = 0 - player.playerrect.y + (aspect[1] * (cellsize * 1.25)) - (cellsize * 1.25)

    screen.fill(pygame.Color(11,  11,  11))  # to be removed

    # runs objects
    for process in processes:
        process()

    # x/y coords
    screen.blit(pygametext("X: "+ str(player.playerrect.x) + " Y: "+ str(player.playerrect.y)), (1,  1,  1,  1))
    screen.blit(pygametext("Hp: " + str(player.hp)), ((aspect[0] * (cellsize * 2)) - 60,  1,  1,  1))

    for event in pygame.event.get():
        if event.type == QUIT:
            client_socket.send(b'\xef')
            pygame.quit()
            sys.exit()

    if player.hitbox(1):
        sound["goal"].play()
        nextlevel,  newmap,  camera,  tilemap,  player,  processes,  sound,  texture,  level,  nonplayer,  message = loadnewlevel(nextlevel, 'null', 3, message)
        levelnum += 1
    if player.hp < 1:
        player.hp = 3
        nextlevel,  newmap,  camera,  tilemap,  player,  processes,  sound,  texture,  level,  nonplayer,  message = loadnewlevel(nextlevel, "a1m1.map", 3, message)
        levelnum = 1
		
    clientanimationdelay = int(clock.get_fps())
    try:
        message = client_id + player.playerrect.x.to_bytes(2,  'little') + player.playerrect.y.to_bytes(2,  'little') + int(player.direction + 1).to_bytes(1,  'little') + int(player.movevector.x == 0).to_bytes(1,  'little') + levelnum.to_bytes(1,  'little') + clientname.encode("utf-8")
    except:
        message = client_id + player.playerrect.x.to_bytes(2,  'little') + player.playerrect.y.to_bytes(2,  'little') + int(player.direction + 1).to_bytes(1,  'little') + int(0).to_bytes(1,  'little') + levelnum.to_bytes(1,  'little') + clientname.encode("utf-8")
    
    client_socket.send(message)
	
    data = client_socket.recv(1024)
    if data:
        data = data.split(b'\xff')
        for client in data:
            client_data = list(client)
            if client:
                try:
                    clientdatalist[client_data[0]] = {'x': client_data[1].to_bytes(1,  'little') + client_data[2].to_bytes(1,  'little'),  'y': client_data[3].to_bytes(1,  'little') + client_data[4].to_bytes(1,  'little'),  'd': client_data[5] - 1,  'm': client_data[6],  'l': client_data[7]}
                    clientdatalist[client_data[0]]['n'] = chr(client_data[8]) + chr(client_data[9]) + chr(client_data[10])
                except:
                    print('Packet malformed: ignoring')
            if clientcurrentanimationdelay >= clientanimationdelay:
                clientcurrentanimationdelay = 0
                clientanimation = not clientanimation 
            else:
                clientcurrentanimationdelay += 1      
    for c in clientdatalist.keys():
        if c.to_bytes(1,  'little') != client_id and clientdatalist[c]['l'] == levelnum:
            screen.blit(pygametext(clientdatalist[c]['n']),  (int.from_bytes(clientdatalist[c]['x'],  "little") + camera.x,  int.from_bytes(clientdatalist[c]['y'],  "little") - 20 + camera.y))
            if not clientdatalist[c]['m']:
                if clientdatalist[c]['d'] < 0:
                    screen.blit(pygame.transform.flip(clientanimations[clientanimation],  True,  False),  (int.from_bytes(clientdatalist[c]['x'],  "little") + camera.x,  int.from_bytes(clientdatalist[c]['y'],  "little") + camera.y))
                else:
                    screen.blit(clientanimations[clientanimation],  (int.from_bytes(clientdatalist[c]['x'],  "little") + camera.x,  int.from_bytes(clientdatalist[c]['y'],  "little") + camera.y))
            else:
                if clientdatalist[c]['d'] < 0:
                    screen.blit(pygame.transform.flip(clientanimations[0],  True,  False),  (int.from_bytes(clientdatalist[c]['x'],  "little") + camera.x,  int.from_bytes(clientdatalist[c]['y'],  "little") + camera.y))
                else:
                    screen.blit(clientanimations[0],  (int.from_bytes(clientdatalist[c]['x'],  "little") + camera.x,  int.from_bytes(clientdatalist[c]['y'],  "little") + camera.y))
	
    # displays fps on title bar
    pygame.display.set_caption("FPS: " + str(int(clock.get_fps())))

    # update pygame and get deltatime
    pygame.display.update()
    dt = clock.tick(60) / 100
