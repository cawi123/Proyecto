import pygame
from tkinter import *
tk =Tk()

canvas = Canvas(tk, width=1000 , height=900)
canvas.pack()
imgfondo=PhotoImage(file='fondo.png')
my_image = PhotoImage(file="s1.png")
canvas.create_image(0,0,anchor=NW, image=imgfondo)
canvas.create_image(0,0,anchor=NW, image=my_image)

def mover(event):
    if event.keysym =='Left':
        canvas.move(1,-3,0)
    else:
        canvas.move(1,3,0)

canvas.bind_all('<KeyPress-Left>',mover)
canvas.bind_all('<KeyPress-Right>',mover)

tk.mainloop()
