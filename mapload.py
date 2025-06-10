from zipfile import ZipFile
from io import BytesIO
import os
import random

scramble = {'g':0,'f':1,'t':2,'s':3,'e':4,'m':8}
randomfilename = str(random.randint(100, 999)) + '.sav'

def buildmap(map):
	temp = []
	newmap = []
	nextlevel = ''
	mapdataover = False
	for i in range(len(map)):
		if not mapdataover:
			if map[i] == "\r" or map[i] == "\n":
				i += 1
			elif map[i] == "x":
				mapdataover = True
			elif map[i] != 'm':
				temp = temp + [scramble[map[i]]]
			else:
				newmap.append(temp)
				temp = []
		else:
			nextlevel = nextlevel + str(map[i])

	return newmap , nextlevel

def loadpakitem(pak,filename):
	with ZipFile(pak, 'r') as pakref:
		with pakref.open(filename, 'r') as file:
			read = file.read()
			content = BytesIO(read)
		return content

def loadpaktext(pak,filename):
	with ZipFile(pak, 'r') as pakref:
		with pakref.open(filename, 'r') as file:
			read = file.read()
			content = read.decode('utf-8')
		return content

def buildsav(filename):
	with open('SAVES\\' + filename) as f:
		text = f.read()
		temp = text.split('x')
		return temp[0], int(temp[1])

def savefile(filename,levelname,hp):
	if filename == '':
		filename = randomfilename
	if not os.path.exists("SAVES"):
		os.makedirs("SAVES")
	with open('SAVES\\' + filename, "w") as file:
    		file.write(f"{levelname}x{hp}")