import mapload #custom
import pygame
import sys
import math
from pygame.locals import QUIT

#basic math definitions
size = 2
aspect = (16,9)
cellsize = 32
halfcellsize = cellsize / 2

#camera
camera = pygame.Rect(0,0,0,0)
starthp = 3

#pygame set up
pygame.init()
screen = pygame.display.set_mode(((aspect[0]*size)*cellsize, (aspect[1]*size)*cellsize))
clock = pygame.time.Clock()
fps = 120
dt = 1

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class players:
        def __init__(self, tilemap,hp=3):
                #vars set up
                self.hp = hp
                self.isonfloor = False
                self.velocityY = 0
                self.moving = True
                self.animation = True
                self.currentanimationdelay = 0
                self.tilemap = tilemap
                self.lasttime = 0
                self.direction = 1
                self.maxfallspeed = 100
                self.gravity = 25
                self.jumphight = -80
                self.speed = 36

                #setup player rect
                self.playeranimations = [pygame.transform.scale(texture['playerstand'], (cellsize,cellsize)), pygame.transform.scale(texture['playerwalk'], (cellsize,cellsize))]
                self.playerrect = pygame.Rect(( len(self.tilemap.currentlevel[0]) * halfcellsize - halfcellsize, len(self.tilemap.currentlevel) * halfcellsize - halfcellsize),(10,10))

                #find map start tile if available
                for y in range(len(self.tilemap.currentlevel)):
                        for x in range(len(self.tilemap.currentlevel[0])):
                                if self.tilemap.currentlevel[y][x] == 0:
                                        self.start =  pygame.math.Vector2(x * cellsize, y * cellsize - halfcellsize)
                                        self.playerrect.x = self.start.x
                                        self.playerrect.y = self.start.y
                                        return

        def playermove(self):
                #checks if dead
                if self.hp < 1:
                        self.hp = 3
                        loadnewlevel('local.map')

                #sets animation to run 8 times a second i hope
                self.animationdelay = int(clock.get_fps()) / 8
                self.keys = pygame.key.get_pressed()

                if self.keys[pygame.K_0]:
                        try:
                                mapload.savefile(sys.argv[2],level,self.hp)
                        except:
                                mapload.savefile('',level,self.hp)

                #used for converting the bools from keys[pygame.K_*]] into movement speed
                self.BoolToInt = {True: 0, False: self.speed}
                #gets wasd into a vector
                self.movevector = pygame.math.Vector2( ( self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]] ), ( self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]] ) )

                #do gravity acceleration or jump
                if not self.velocityY >= self.maxfallspeed:
                        self.velocityY += self.gravity * dt
                if self.keys[pygame.K_w] and self.isonfloor:
                        sound['jump'].play()
                        self.velocityY += self.jumphight

                self.isonfloor = False

                #used for collison math converts global coords to tilemap coords with some modifiers
                self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + (13 * self.direction), self.playerrect.y + 14))
                self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + (self.velocityY * dt) + halfcellsize))

                #checks if level end reached
                if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tilemap.global_to_map(self.playerrect).x)] == 1:
                        sound['goal'].play()
                        loadnewlevel()
                elif self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tilemap.global_to_map(self.playerrect).x)] == 4:
                        sound['jump'].play()
                        self.playerrect.x = self.start.x
                        self.playerrect.y = self.start.y
                        self.hp -= 1


                #checks if off solid tile if yes gravity added if not reset velocityY and check if solid tile it roof if no is on floor true
                if self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
                        self.playerrect.y += self.velocityY * dt
                else:
                        if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tempy.x)] != 2:
                                self.isonfloor = True
                        self.velocityY = 0

                #checks if moving will put you in wall if not move
                if self.tilemap.currentlevel[int(self.tempx.y)][int(self.tempx.x)] != 2:
                        self.playerrect.x += self.movevector.x * dt

                self.draw()

        def draw(self):
                #if moving update direction
                if self.movevector.x != 0:
                        self.direction = math.copysign(1,self.movevector.x)

                #if moving or jumping use walking animation if not use standing sprite
                if self.movevector.x != 0 or self.movevector.y != 0:
                        if self.direction < 0:
                                screen.blit(pygame.transform.flip(self.playeranimations[{True:1,False:0}[self.animation]], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
                        else:
                                screen.blit(self.playeranimations[{True:1,False:0}[self.animation]],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

                        #if animation needs to change flip animation
                        if self.currentanimationdelay >= self.animationdelay:
                                self.animation = not self.animation
                                self.currentanimationdelay = 0
                        else:
                                self.currentanimationdelay += 1
                else:
                        if self.direction < 0:
                                screen.blit(pygame.transform.flip(self.playeranimations[0], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
                        else:
                                screen.blit(self.playeranimations[0],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

#####################################
class nonplayers:
        def __init__(self, tilemap,hp=3):
                #vars set up
                self.hp = hp
                self.isonfloor = False
                self.velocityY = 0
                self.moving = True
                self.animation = True
                self.currentanimationdelay = 0
                self.tilemap = tilemap
                self.direction = 1
                self.maxfallspeed = 100
                self.gravity = 25
                self.speed = 16

                #setup player rect
                self.playeranimations = [pygame.transform.scale(texture['playerstand'], (cellsize,cellsize)), pygame.transform.scale(texture['playerwalk'], (cellsize,cellsize))]
                self.playerrect = pygame.Rect(( len(self.tilemap.currentlevel[0]) * halfcellsize - halfcellsize, len(self.tilemap.currentlevel) * halfcellsize/2),(10,10))

        def playermove(self):
                #sets animation to run 8 times a second i hope
                self.animationdelay = int(clock.get_fps()) / 8

                self.movevector = pygame.math.Vector2( self.direction * self.speed, 0 )

                #do gravity acceleration or jump
                if not self.isonfloor:
                        self.velocityY += self.gravity * dt

                self.isonfloor = False

                #used for collison math converts global coords to tilemap coords with some modifiers
                self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + (13 * self.direction), self.playerrect.y + 14))

                if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tempx.x)] != 2:
                        self.isonfloor = True
                        self.velocityY = 0
                else:
                        self.playerrect.y +=  self.velocityY * dt

                #checks if moving will put you in wall if not move
                if self.tilemap.currentlevel[int(self.tempx.y)][int(self.tempx.x)] != 2:
                        self.playerrect.x += self.movevector.x * dt
                        print('move')
                else:
                        self.direction = 0 - self.direction

                self.draw()

        def draw(self):
                if self.direction < 0:
                        screen.blit(pygame.transform.flip(self.playeranimations[{True:1,False:0}[self.animation]], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
                else:
                        screen.blit(self.playeranimations[{True:1,False:0}[self.animation]],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

                #if animation needs to change flip animation
                if self.currentanimationdelay >= self.animationdelay:
                        self.animation = not self.animation
                        self.currentanimationdelay = 0
                else:
                        self.currentanimationdelay += 1

#####################################

class tilemaps:
        def __init__(self,map):
                #get local verson of textures
                self.currentlevel = map
                self.textures = list(texture.values())

        def drawlevel(self):
                #display tile if texture available for tile *note map doesn't have to be square
                for i in range(len(self.currentlevel)):
                        for j in range(len(self.currentlevel[i])):
                                self.tilerect = pygame.Rect( ((j*cellsize) + camera.x, (i*cellsize) + camera.y), (cellsize,cellsize) )
                                try:
                                        screen.blit(self.textures[self.currentlevel[i][j]],self.tilerect)
                                except:
                                        pass

        def global_to_map(self, vector):
                #converts global units to tilemap coords
                x = int((vector.x + halfcellsize) // cellsize)
                y = int((vector.y + halfcellsize) // cellsize)
                return pygame.math.Vector2(x, y)

def pygametext(txt):
        #sets up text for display
        sans = pygame.font.SysFont('Comic Sans MS', 20)
        return sans.render(txt, False, (155, 155, 155))

def loadnewlevel(nextlevelrand='null'):
        global nextlevel,newmap,camera,tilemap,player,processes,sound,texture,level
        level = nextlevel
        print(nextlevel)
        #puts all sounds of type *.wav into a dictionary
        sound = {}
        for i in mapload.ZipFile(sys.argv[1],'r').namelist():
                if i.startswith(f'{arg}/sounds/') and i.endswith('.wav'):
                        sound[i.split('/')[-1].split('.')[0]] = pygame.mixer.Sound(mapload.loadpakitem(sys.argv[1], i))

        #puts all images of type *bmp/*.png into a dictionary
        texture = {}
        for i in mapload.ZipFile(sys.argv[1],'r').namelist():
                if i.startswith(f'{arg}/textures/') and i.endswith('.bmp'):
                        texture[i.split('/')[-1].split('.')[0]] = pygame.image.load(mapload.loadpakitem(sys.argv[1], i))
                elif i.startswith(f'{arg}/textures/') and i.endswith('.png'):
                        texture[i.split('/')[-1].split('.')[0]] = pygame.image.load(mapload.loadpakitem(sys.argv[1], i))
        #resets processes loop remakes the tilemap, and player objects and gets name of next level
        if nextlevelrand == 'null':
                newmap, nextlevel = mapload.buildmap(mapload.loadpaktext(sys.argv[1], f"{arg}/maps/{nextlevel}"))
        else:
                newmap, nextlevel = mapload.buildmap(mapload.loadpaktext(sys.argv[1], f"{arg}/maps/{nextlevelrand}"))
        tilemap = tilemaps(newmap)
        try:
                player = players(tilemap, player.hp)
        except:
                player = players(tilemap, starthp)
        processes = [tilemap.drawlevel, player.playermove]

def loadsav():
        nextlevel, starthp = mapload.buildsav(sys.argv[2])
        player.hp = starthp
        loadnewlevel(nextlevel)

#start of game logic
#find used *.pak
arg = str(sys.argv[1]).split('.')[0]
#set starting map
level = ''
nextlevel = 'local.map'

loadnewlevel()
try:
        loadsav()
except:
        pass

nonplayer = [ nonplayers(tilemap) ]
processes.append(nonplayer[0].playermove)

while True:
        #center camera
        camera.x = 0 - player.playerrect.x + (aspect[0] * cellsize) - cellsize
        camera.y = 0 - player.playerrect.y + (aspect[1] * (cellsize * 1.25)) - (cellsize * 1.25)

        screen.fill(pygame.Color(11,11,11))#to be removed

        #runs objects
        for process in processes:
                process()

        #x/y coords
        screen.blit( pygametext( 'X: ' + str(tilemap.global_to_map(player.playerrect).x) + ' Y: ' + str(tilemap.global_to_map(player.playerrect).y) ) , (1,1,1,1))
        screen.blit( pygametext( 'Hp: ' + str(player.hp) ),  ((aspect[0] * (cellsize * 2)) - 60, 1, 1, 1))

        #idk what this does but if i remove it pygame crashes
        for event in pygame.event.get():
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

        #displays fps on title bar
        pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

        #update pygame and get deltatime
        pygame.display.update()
        dt = clock.tick()/100
