from zipfile import ZipFile

scramble = {'g':0,'f':1,'t':2,'s':3,'e':4,'m':8}

""" depricated
def loadrawdata(filepath):
    with open(filepath, "r") as file:
        content = file.read()
    return content
"""

def buildmap(map):
    temp = []
    newmap = []
    for i in range(len(map)):
        if map[i] != 'm':
            temp = temp + [scramble[map[i]]]
        else:
            newmap.append(temp)
            temp = []
    return newmap

def loadpakitem(pak,filename):
	with ZipFile(pak, 'r') as pakref:
		with pakref.open(filename, 'r') as file:
			read = file.read()
			content = read
		return content