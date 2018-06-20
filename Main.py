from MazeGenerator import MazeGenerator
from tkinter import *
from PIL import Image, ImageTk

root = Tk(None, None, 'Maze')

maz = MazeGenerator()
maz.save('maze')
image = ImageTk.PhotoImage(maz.solved)
Label(root, image=image).pack()
root.mainloop()
