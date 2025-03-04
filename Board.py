# Code copied from https://github.com/whitneysattler/python-gui/blob/master/CheckerBoard.py

from tkinter import *

class checkerBoard:
    def __init__(self):
        window = Tk()
        window.title("Displaying a Checkerboard")

        for i in range(64):
            if i % 2 == (i // 8) % 2:
                color = "white"
            else:
                color = "black"
            Canvas(window, width=50, height = 50, bg = color).grid(row = i // 8, column = i % 8)

        window.mainloop()

checkerBoard()