import pygame
import sys
import json
import mapload
from pygame.locals import QUIT

size = 2
aspect = (16,9)
cellsize = 32
halfcellsize = cellsize / 2

# pygame set up
pygame.init()
screen = pygame.display.set_mode(((aspect[0]*size)*cellsize, (aspect[1]*size)*cellsize))
clock = pygame.time.Clock()
fps = 120
dt = 1

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class player:
	def __init__(self, tilemap):
		self.playeranimations = [pygame.transform.scale(pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/playerstand.png')), (cellsize,cellsize)), pygame.transform.scale(pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/playerwalk.png')), (cellsize,cellsize))]
		self.isonfloor = False
		self.vely = 0
		self.moving = True
		self.animation = True
		self.currentanimationdelay = 0
		self.tilemap = tilemap
		self.lasttime = 0
		self.dir = 1
		self.maxfallspeed = 100
		self.gravity = 40
		self.jumphight = -120
		self.speed = 38
		self.playerrect = pygame.Rect(( len(self.tilemap.currentlevel[0]) * halfcellsize - halfcellsize, len(self.tilemap.currentlevel) * halfcellsize - halfcellsize),(10,10))
	
	def playermove(self):
		self.animationdelay = int(clock.get_fps()) / 8
		self.keys = pygame.key.get_pressed()
		
		self.BoolToInt = {True: 0, False: self.speed}
		self.movevector = pygame.math.Vector2( ( self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]] ), ( self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]] ) )

		if not self.vely >= self.maxfallspeed:
			self.vely += self.gravity * dt
		if self.keys[pygame.K_w] and self.isonfloor:
			self.vely += self.jumphight

		self.isonfloor = False

		self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + self.movevector.x, self.playerrect.y))
		self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + (self.vely * dt) + halfcellsize))

		if self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
			self.playerrect.y += self.vely * dt
		else:
			while self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
				self.playerrect.y += -1
			if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tempy.x)] != 2:
				self.isonfloor = True
			self.vely = 0

		if self.tilemap.currentlevel[int(self.tempx.y)][int(self.tempx.x)] != 2:
			self.playerrect.x += self.movevector.x * dt

		self.draw()

	def draw(self):
		if self.movevector.x != 0: 
			self.dir = self.movevector.x 

		if self.movevector.x != 0 or self.movevector.y != 0:
			if self.dir < 0:
				screen.blit(pygame.transform.flip(self.playeranimations[{True:1,False:0}[self.animation]], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
			else:
				screen.blit(self.playeranimations[{True:1,False:0}[self.animation]],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

			if self.currentanimationdelay >= self.animationdelay:
				self.animation = not self.animation
				self.currentanimationdelay = 0
			else:
				self.currentanimationdelay += 1
		else:
			if self.dir < 0:
				screen.blit(pygame.transform.flip(self.playeranimations[0], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
			else:
				screen.blit(self.playeranimations[0],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

class tilemap:
	def __init__(self,map):
		self.currentlevel = map

	def drawlevel(self):
		tempcolor = [pygame.Color(100,255,0), pygame.Color(255,0,255), pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/missing.bmp'))]
		for i in range(len(self.currentlevel)):
			for j in range(len(self.currentlevel[i])):
				self.tilerect = pygame.Rect( ((j*cellsize) + camera.x, (i*cellsize) + camera.y), (cellsize,cellsize) )
				try:
					screen.blit(tempcolor[self.currentlevel[i][j]],self.tilerect)
				except:
					try:
						pygame.draw.rect(screen, tempcolor[self.currentlevel[i][j]], self.tilerect) 
					except:
						pygame.draw.rect(screen, pygame.Color(255,255,255), self.tilerect) 

	def global_to_map(self, vector):
		x = int((vector.x + halfcellsize) // cellsize)
		y = int((vector.y + halfcellsize) // cellsize)
		return pygame.math.Vector2(x, y)

def pygametext(txt):
	sans = pygame.font.SysFont('Comic Sans MS', 20)
	return sans.render(txt, False, (155, 155, 155))

arg = str(sys.argv[1]).split('.')[0]
newmap, nextlevel = mapload.buildmap(mapload.loadpaktext(sys.argv[1], f"{arg}/maps/local.map"))

camera = pygame.Rect(0,0,0,0)

tilemap = tilemap(newmap)
print(nextlevel)

player = player(tilemap)

processes = [tilemap.drawlevel, player.playermove]

while True:
	camera.x = 0 - player.playerrect.x + (aspect[0] * cellsize) - cellsize
	camera.y = 0 - player.playerrect.y + (aspect[1] * (cellsize * 1.25)) - (cellsize * 1.25)

	screen.fill(pygame.Color(11,11,11))#to be removed

	for process in processes:
		process()

	screen.blit( pygametext( 'X: ' + str(tilemap.global_to_map(player.playerrect).x) + ' Y: ' + str(tilemap.global_to_map(player.playerrect).y) ) , (1,1,1,1))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.set_caption('FPS: ' + str(int(clock.get_fps())))

	pygame.display.update()
	dt = clock.tick()/100