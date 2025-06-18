import pygame, sys
import json
import os
from pygame.locals import QUIT
from re import X

pygame.init()

clock = pygame.time.Clock()
fps = 120

tred = pygame.image.load("spikered.png")
tblu = pygame.image.load("spikeblue.png")
trep = pygame.image.load("spikeredup.png")
tblp = pygame.image.load("spikeblueup.png")
t002 = pygame.image.load("tile002.png")
t006 = pygame.image.load("tile006.png")
t009 = pygame.image.load("tile009.png")
t021 = pygame.image.load("tile021.png")


col = t002.get_rect()

level1 = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ,[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1]
        ,[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
        ,[1,1,1,1,2,2,2,1,2,2,2,2,2,2,2,2,2,1]
        ,[1,4,4,4,2,2,2,1,2,2,2,2,2,2,2,2,2,1]
        ,[1,0,0,0,2,2,2,3,2,2,2,2,2,2,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,1]
        ,[1,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,2,9]
        ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

screen = pygame.display.set_mode((len(level1[0])*45, len(level1)*45))

mode = input('mode ')
if mode == "MLL":
    n = []
    for i in range(2):
        n.append(input('.'))
    test = 'lvl.json'
    with open(test, "w") as file:
            json.dump(n, file)
    print(n)
    pygame.quit()
    sys.exit()

filename = input('input file name ') 

filename = "maps/" + filename

if os.path.exists(filename):
    print('The file exists!')
    with open(filename, 'rb') as file:
        level1 = json.load(file)
    print('opened')
else:
    print('The file does not exist.')
    print('making new level')

def editmap():
    global keys
    mx, my = pygame.mouse.get_pos()
    mx, my = (int(mx/45),int(my/45))
    if keys[pygame.K_1]:
        level1[my][mx] = 0
    if keys[pygame.K_2]:
        level1[my][mx] = 1
    if keys[pygame.K_3]:
        level1[my][mx] = 2
    if keys[pygame.K_4]:
        level1[my][mx] = 3
    if keys[pygame.K_5]:
        level1[my][mx] = 4
    if keys[pygame.K_6]:
        level1[my][mx] = 5
    if keys[pygame.K_7]:
        level1[my][mx] = 6
    if keys[pygame.K_9]:
        level1[my][mx] = 9
    if keys[pygame.K_i]:
        level1[my][mx] = 7
    if keys[pygame.K_o]:
        level1[my][mx] = 8
    if keys[pygame.K_b]:
        level1[my][mx] = -1
        
    if keys[pygame.K_s]:
        for i in range(len(level1)):
            print(level1[i])
            
            with open(filename, "w") as file:
                json.dump(level1, file)
            
while True:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    if mode == "MMM":
        editmap()
    
    screen.fill((34,34,34))
    
    for i in range(len(level1)):
        for j in range(len(level1[i])):
            if level1[i][j] == 0:
                screen.blit(t006, (j*45, i*45))
            elif level1[i][j] == 1:
                screen.blit(t002, (j*45, i*45))
            elif level1[i][j] == 2:
                screen.blit(t009, (j*45, i*45))
            elif level1[i][j] == 3:
                screen.blit(tred, (j*45, i*45))
            elif level1[i][j] == 4:
                screen.blit(tblu, (j*45, i*45))
            elif level1[i][j] == 5:
                screen.blit(trep, (j*45, i*45))
            elif level1[i][j] == 6:
                screen.blit(tblp, (j*45, i*45))
            elif level1[i][j] == 9:
                screen.blit(t021, (j*45, i*45))
            elif level1[i][j] == -1:
                screen.blit(t021, (j*45, i*45))
            elif level1[i][j] == 7:
                screen.blit(t009, (j*45, i*45))
            elif level1[i][j] == 8:
                screen.blit(trep, (j*45, i*45))
                
            col.x = j*45
            col.y = i*45

    pygame.display.update()
    clock.tick(fps)