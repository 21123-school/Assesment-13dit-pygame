import pygame
import sys
import json
import mapload
from pygame.locals import QUIT

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*32, 14*32))
clock = pygame.time.Clock()
fps = 120
dt = 1

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class player:
	def __init__(self, tilemap):
		self.playeranimations = [pygame.transform.scale(pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/playerstand.png')), (32,32)), pygame.transform.scale(pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/playerwalk.png')), (32,32))]
		self.isonfloor = False
		self.vely = 0
		self.moving = True
		self.animation = True
		self.animationdelay = fps / 8
		self.currentanimationdelay = 0
		self.tilemap = tilemap
		self.lasttime = 0
		self.dir = 1
		self.playerrect = pygame.Rect(( len(self.tilemap.currentlevel[0]) * 16 - 16, len(self.tilemap.currentlevel) * 16 - 16),(10,10))
	
	def playermove(self):
		self.keys = pygame.key.get_pressed()
		
		self.BoolToInt = {True: 0, False: 19}
		self.movevector = pygame.math.Vector2( ( self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]] ), ( self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]] ) )

		if not self.vely >= 35:
			self.vely += 1
		if self.keys[pygame.K_w] and self.isonfloor:
			self.vely = -55

		self.isonfloor = False

		self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + self.movevector.x, self.playerrect.y))
		self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + (self.vely * dt) + 16))

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
		if self.movevector.x != 0 or self.movevector.y != 0:
			if self.movevector.x < 0:
				screen.blit(pygame.transform.flip(self.playeranimations[{True:1,False:0}[self.animation]], True, False),(self.playerrect.x + camera.x, self.playerrect.y + camera.y))
			else:
				screen.blit(self.playeranimations[{True:1,False:0}[self.animation]],(self.playerrect.x + camera.x, self.playerrect.y + camera.y))

			if self.currentanimationdelay >= self.animationdelay:
				self.animation = not self.animation
				self.currentanimationdelay = 0
			else:
				self.currentanimationdelay += 1
		else:
			screen.blit(self.playeranimations[0], (self.playerrect.x + camera.x, self.playerrect.y + camera.y))

class tilemap:
	def __init__(self,map):
		self.currentlevel = map

	def drawlevel(self):
		tempcolor = [pygame.Color(100,255,0), pygame.Color(255,255,255), pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/missing.bmp'))]
		for i in range(len(self.currentlevel)):
			for j in range(len(self.currentlevel[i])):
				self.tilerect = pygame.Rect( ((j*32) + camera.x, (i*32) + camera.y), (32,32) )
				try:
					screen.blit(tempcolor[self.currentlevel[i][j]],self.tilerect)
				except:
					try:
						pygame.draw.rect(screen, tempcolor[self.currentlevel[i][j]], self.tilerect) 
					except:
						pygame.draw.rect(screen, pygame.Color(255,255,255), self.tilerect) 

	def global_to_map(self, vector):
		x = int((vector.x + 16) // 32)
		y = int((vector.y + 16) // 32)
		return pygame.math.Vector2(x, y)

def pygametext(txt):
	sans = pygame.font.SysFont('Comic Sans MS', 20)
	return sans.render(txt, False, (255, 255, 255))

def loadjson(f):
	with open(f, 'rb') as file:
		o = json.load(file)
	return o

arg = str(sys.argv[1]).split('.')[0]
newmap, nextlevel = mapload.buildmap(mapload.loadpaktext(sys.argv[1], f"{arg}/maps/local.map"))

camera = pygame.Rect(0,0,0,0)

tilemap = tilemap(newmap)
print(nextlevel)

player = player(tilemap)

processes = [tilemap.drawlevel, player.playermove]

while True:
	camera.x = 0 - player.playerrect.x + (18 * 16) - 16
	camera.y = 0 - player.playerrect.y + (14 * 26) - 24

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
	dt = clock.tick(fps)/100