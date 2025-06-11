I don't rememeber what this doc is  normally used for so I will info dump here so I don't forget.

------------
launcher.pyw

this just automates starting main.py has a *.pak selecter so you can have multiple *.pak files this leads to a possibility for easy mod making although it will most likey be unused this also has a *.sav selector

I might remove this file before hand in as it's not required and I don't think it will.

------------
main.py

this is the main file and is the most of the engine logic it contains the player class, the tilemap class, and the main game loop

in the main game loop there is a list of funcions that run every frame that can be hot added to so things like object spawners can exist just by an append.

------------
mapload.py

currently used as a import in main.py it handles loading textbased items from a *.pak, loading non textbased items from a *.pak,and also handles building maps from its coded form to it's usable state it also returns the name of the next level. there is also a funcion I have deemed depricated that reads from a file.

------------
paktool.py

this automates paking the data folder into the *.pak file.

------------
data.pak

this contains game data like level data, and sprites.

------------
data folder

this is a folder that has the unpacked verson of a *.pak file for testing.
