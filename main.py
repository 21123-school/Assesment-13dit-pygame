import pygame
import sys
import json

# pygame set up
pygame.init()
screen = pygame.display.set_mode((18*45, 14*45))
clock = pygame.time.Clock()
fps = 120


sans = pygame.font.SysFont('Comic Sans MS', 50)
starttxt = sans.render('Dungeon Run', False, (0, 0, 0))
sans = pygame.font.SysFont('Comic Sans MS', 20)
start = sans.render('Press ENTER to start', False, (0, 0, 0))

#musicsound = pygame.mixer.Sound("sound/music.wav")

def loadjson(f):
    with open(f, 'rb') as file:
        o = json.load(file)
    return o

#musicsound.play(-1)

while True:
    keys = pygame.key.get_pressed()

    screen.fill((34, 34, 34))

    screen.blit(sans.render('score: ' + 'beans', False, (255, 255, 255)), (15, 0, 50, 50))

    pygame.display.update()
    clock.tick(fps)
