from MazeGenerator import MazeGenerator
from tkinter import *
from PIL import Image, ImageTk

root = Tk(None, None, 'Maze')

maz = MazeGenerator()
maz.save('test')
# image = ImageTk.PhotoImage(maz.solved)
# Label(root, image=image).pack()
# root.mainloop()
