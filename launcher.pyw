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

root = Tk()
root.title("Game Launcher")

frm = ttk.Frame(root, padding=20)
frm.grid()

# Title label
ttk.Label(frm, text="---------game launcher---------").grid(column=0, row=0, columnspan=2, pady=(0, 15))

# Dropdown label + combobox for GamePack (.pak files)
selected_file_pak = StringVar()
if files:
    selected_file_pak.set(files[0])

# Dropdown label + combobox for Sav (.sav files)
ttk.Label(frm, text="HOST IP: ").grid(column=0, row=3, pady=(0, 15))
file_dropdown_sav = ttk.Entry(frm)
file_dropdown_sav.grid(column=1, row=3, pady=(0, 15))

ttk.Label(frm, text="USERNAME: ").grid(column=0, row=4, pady=(0, 15))
file_dropdown_nam = ttk.Entry(frm)
file_dropdown_nam.grid(column=1, row=4, pady=(0, 15))

# Start button
def start_game():
    pak = selected_file_pak.get()
    sav = file_dropdown_sav.get()
    nam = file_dropdown_nam.get()
    #for i in range(5):
    subprocess.Popen([sys.executable, "main.py", pak, sav, nam[:3]])

ttk.Button(frm, text="Start", command=start_game).grid(column=0, row=5, pady=(0, 15))

# Quit button
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=6, pady=(0, 15))

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
