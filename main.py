import pygame
import sys
import json
import mapload
from pygame.locals import QUIT

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*32, 14*32))
clock = pygame.time.Clock()
fps = 60
deltatime = 1

#musicsound = pygame.mixer.Sound("sound/music.wav")
#musicsound.play(-1)

class player:
	def __init__(self, tilemap):
		self.isonfloor = False
		self.vely = 0
		self.tilemap = tilemap
		self.lasttime = 0
		self.playerrect = pygame.Rect(( len(self.tilemap.currentlevel[0]) * 16 - 5, len(self.tilemap.currentlevel) * 16 - 5),(10,10))
	
	def playermove(self):
		self.keys = pygame.key.get_pressed()
		
		self.BoolToInt = {True: 0, False: 3}
		self.movevector = pygame.math.Vector2( ( self.BoolToInt[self.keys[pygame.K_a]] + 0 - self.BoolToInt[self.keys[pygame.K_d]] ), ( self.BoolToInt[self.keys[pygame.K_w]] + 0 - self.BoolToInt[self.keys[pygame.K_s]] ) )
		
		self.tempx = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x + self.movevector.x, self.playerrect.y))
		#self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + self.movevector.y))

		if not self.vely >= 6:
			self.vely += 0.2
		if self.keys[pygame.K_w] and self.isonfloor:
			self.vely = -7

		self.isonfloor = False

		self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + (0.6 + self.vely) + 5))

		if self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
			self.playerrect.y += self.vely
		else:
			while self.tilemap.currentlevel[int(self.tempy.y)][int(self.tempy.x)] != 2:
				self.playerrect.y += -1
				self.tempy = self.tilemap.global_to_map(pygame.math.Vector2(self.playerrect.x, self.playerrect.y + self.vely))
			if self.tilemap.currentlevel[int(self.tilemap.global_to_map(self.playerrect).y)][int(self.tempy.x)] != 2:
				self.isonfloor = True
			self.vely = 0

		if self.tilemap.currentlevel[int(self.tempx.y)][int(self.tempx.x)] != 2:
			self.playerrect.x += self.movevector.x

		self.draw()

	def draw(self):
		pygame.draw.rect(screen, pygame.Color(150,0,150), player.playerrect) 

class tilemap:
	def __init__(self,map):
		self.currentlevel = map

	def drawlevel(self):
		tempcolor = [pygame.Color(100,255,0), pygame.Color(255,255,255), pygame.image.load(mapload.loadpakitem(sys.argv[1],f'{arg}/textures/missing.bmp'))]
		for i in range(len(self.currentlevel)):
			for j in range(len(self.currentlevel[i])):
				tilerect = ( (j*32, i*32), (32,32) )
				try:
					screen.blit(tempcolor[self.currentlevel[i][j]],tilerect)
				except:
					try:
						pygame.draw.rect(screen, tempcolor[self.currentlevel[i][j]], tilerect) 
					except:
						pygame.draw.rect(screen, pygame.Color(255,255,255), tilerect) 

	def global_to_map(self, vector):
		x = int((vector.x + 5) // 32)
		y = int((vector.y + 5) // 32)
		return pygame.math.Vector2(x, y)

def pygametext(txt):
	sans = pygame.font.SysFont('Comic Sans MS', 20)
	return sans.render(txt, False, (255, 255, 255))

def loadjson(f):
	with open(f, 'rb') as file:
		o = json.load(file)
	return o

arg = str(sys.argv[1]).split('.')[0]

try:
	tilemap = tilemap(mapload.buildmap(mapload.loadpaktext(sys.argv[1], f"{arg}/maps/local.map")))
except:
	print('failed..')
	input('')
#tilemap = tilemap(mapload.buildmap(mapload.loadpakitem('data.pak',f'{arg}/maps/local.map').decode('utf-8')))

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
	clock.tick(120)