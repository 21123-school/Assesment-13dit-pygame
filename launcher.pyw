from tkinter import *
from tkinter import ttk
import glob
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get all .py files except main.py
filetype = "*.pak"
files = []
for f in glob.glob(filetype):
	files.append(os.path.basename(f))

root = Tk()
root.title("Game Launcher")

frm = ttk.Frame(root, padding=20)
frm.grid()

# Title label
ttk.Label(frm, text="---------game launcher---------").grid(
    column=0, row=0, columnspan=2, pady=(0, 15)
)

# Dropdown label + combobox
ttk.Label(frm, text="Select GamePack:").grid(
    column=0, row=1, sticky=W, padx=5, pady=5
)

selected_file = StringVar()
file_dropdown = ttk.Combobox(frm, textvariable=selected_file, values=files, state="readonly", width=30)
file_dropdown.grid(column=1, row=1, padx=5, pady=5)
if files:
    selected_file.set(files[0])

# Start button with vertical spacing
ttk.Button(frm, text="Start", command=lambda: subprocess.Popen([sys.executable, "main.py", selected_file.get()])).grid(
    column=0, row=2, columnspan=2, pady=(15, 5)
)

# Quit button with a bit of space below
ttk.Button(frm, text="Quit", command=root.destroy).grid(
    column=0, row=3, columnspan=2, pady=(5, 0)
)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.mainloop()
