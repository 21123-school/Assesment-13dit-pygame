from tkinter import *
from tkinter import ttk
import glob
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get all .pak files
filetype = "*.pak"
files = [os.path.basename(f) for f in glob.glob(filetype)]

# Get all .sav files
filetype2 = "SAVES/*.sav"
files2 = [os.path.basename(f) for f in glob.glob(filetype2)]

root = Tk()
root.title("Game Launcher")

frm = ttk.Frame(root, padding=20)
frm.grid()

# Title label
ttk.Label(frm, text="---------game launcher---------").grid(
    column=0, row=0, columnspan=2, pady=(0, 15)
)

# Dropdown label + combobox for GamePack (.pak files)
ttk.Label(frm, text="SELECT GAMEPACK:").grid(
    column=0, row=1, sticky=W, padx=0, pady=15
)
selected_file_pak = StringVar()
file_dropdown_pak = ttk.Combobox(
        frm,
        textvariable=selected_file_pak,
        values=files, state="readonly",
        width=30
    )
file_dropdown_pak.grid(column=1, row=1, padx=0, pady=15)
if files:
    selected_file_pak.set(files[0])

# Dropdown label + combobox for Sav (.sav files)
# ttk.Label(frm, text="Select Sav:").grid(
#    column=0, row=2, sticky=W, padx=5, pady=5
# )
# selected_file_sav = StringVar()
# file_dropdown_sav = ttk.Combobox(frm, textvariable=selected_file_sav,
#  values=files2, state="readonly", width=30)
# file_dropdown_sav.grid(column=1, row=2, padx=5, pady=5)

ttk.Label(frm, text="MULTIPLAYER:").grid(column=0, row=3, pady=(0, 5))

ttk.Label(frm, text="HOST IP: ").grid(column=0, row=4, pady=(0, 5))
file_dropdown_sav = ttk.Entry(frm)
file_dropdown_sav.grid(column=1, row=4, pady=(0, 5))

ttk.Label(frm, text="USERNAME: ").grid(column=0, row=5, pady=(0, 5))
file_dropdown_nam = ttk.Entry(frm)
file_dropdown_nam.grid(column=1, row=5, pady=(0, 5))


# Start button
def start_game_S():
    pak = selected_file_pak.get()
    sav = file_dropdown_sav.get()
    nam = file_dropdown_nam.get()
    if not sav:
        sav = "localhost"
    if not nam:
        nam = "tes"
    subprocess.Popen([sys.executable, "server.py"])
    subprocess.Popen([sys.executable, "main.py", pak, sav, nam[:3]])


def start_game_M():
    pak = selected_file_pak.get()
    sav = file_dropdown_sav.get()
    nam = file_dropdown_nam.get()
    if not sav:
        sav = "localhost"
    if not nam:
        nam = "tes"
    subprocess.Popen([sys.executable, "main.py", pak, sav, nam[:3]])


def start_game_G():
    subprocess.Popen([sys.executable, "server.py"])


ttk.Button(frm, text="SINGLE PLAYER", command=start_game_S).grid(
    column=0, row=7, columnspan=2, pady=(25, 15)
)

ttk.Button(frm, text="JOIN MULTIPLAYER", command=start_game_M).grid(
    column=0, row=8, columnspan=3, pady=(0, 15)
)

ttk.Button(frm, text="START SERVER", command=start_game_G).grid(
    column=0, row=9, columnspan=2, pady=(0, 15)
)

# Quit button
ttk.Button(frm, text="QUIT", command=root.destroy).grid(
    column=0, row=10, columnspan=4, pady=(0, 15)
)

# Center window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.mainloop()
