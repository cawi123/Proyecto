
import time
from tkinter import *
tk=Tk()
canvas=Canvas(tk,width=500,height=500)
canvas.pack()

def ladrih(xi,yi):
    xf=xi+75
    yf=yi+25
    canvas.create_rectangle(xi,yi,xf,yf,fill='light green')

def ladriv (xi,yi):
    xf=xi+25
    yf=yi+75
    canvas.create_rectangle(xi,yi,xf,yf,fill='red')

def pared1():
    for i in range(25,450,75):
        ladrih(i,25)
pared1()

def pared2():
    for i in range(100,425,75):
        ladriv(25,i)
pared2()

def pared3():
    for i in range(25,450,75):
        ladrih(i,475)
pared3()
def pared4():
    for i in range(50,425,75):
        ladrih(450,i)
pared4()

def interiorh():
    ladrih(100,100)
    ladrih(175,100)
    ladrih(300,100)
    ladrih(375,100)
    ladrih(100,175)
    ladrih(175,175)
    ladrih(250,175)
    ladrih(375,175)
    ladrih(300,250)
    ladrih(175,300)
    ladrih(50,325)
    ladrih(375,325)
    ladrih(50,400)
    ladrih(125,400)
    ladrih(250,400)
    ladrih(400,400)
interiorh()

def interiorv():
    ladriv(225,50)
    ladriv(100,200)
    ladriv(100,275)
    ladriv(175,250)
    ladriv(175,325)
    ladriv(300,400)
    ladriv(300,275)
    ladriv(375,200)
interiorv()

image=PhotoImage(file="soccer.png")
#robot=canvas.create_image(0,0,ancho=NW,image=image)
robot=canvas.create_oval(25,60,50,90,fill='pink')

def move1():
    for x in range (0,80,1):
        canvas.move(robot,2,0)
        tk.update()
        time.sleep(0.005)

def back1():
    for x in range(0,60,1):
        canvas.move(robot,-2,0)
        tk.update()
        time.sleep(0.005)
move1()
back1()

def move2():
    for x in range (0,45,1):
        canvas.move(robot,0,5)
        tk.update()
        time.sleep(0.005)
def back2():
    for x in range(0,30,1):
        canvas.move(robot,0,-5)
        tk.update()
        time.sleep(0.005)
move2()
back2()

def move3():
    for x in range (0,170,1):
        canvas.move(robot,2,0)
        tk.update()
        time.sleep(0.005)
def back3():
    for x in range (0,30,1):
        canvas.move(robot,-2,0)
        tk.update()
        time.sleep(0.005)
move3()
back3()
   

def move4():
    for x in range (0,9,1):
        canvas.move(robot,-2,0)
        tk.update()
        time.sleep(0.005)
move4()
        
    

