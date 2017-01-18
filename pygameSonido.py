import pygame
from pygame.locals import *
import sys,os

class Ventana():
    def __init__(self,Pared_x,Pared_y):
        self.cont=0
        self.listarec=[]
        self.Pared_x=Pared_x
        self.Pared_y=Pared_y
        self.rSalida=pygame.Rect(0,0,40,40)
        self.rLlegada=pygame.Rect(560,560,40,40)
    def CargarFondo(self,matriz,pantalla):
        for i in range(15):
            for j in range(15):
                if (matriz[i][j]==1):
                    self.listarec.append(pygame.Rect(self.Pared_x,self.Pared_y,40,40))
                    self.Pared_x+=40
                else:
                    self.Pared_x+=40
            self.Pared_x=0
            self.Pared_y+=40


    def Seleccion(self,Ven,cont):
        Da=Datos()
        if cont ==0:
            Ven.CargarFondo(self.N1,self.pantalla)
        elif cont==1:
            Ven.CargarFondo(self.N2,self.pantalla)
        elif cont==2:
            Ven.CargarFondo(self.N3,self.pantalla)
            

                
class Datos():
    def __init__ (self):
        self.archivo=open("puntuacion.txt","a")
        self.fichero=[]

    def agregarPunt(self,puntaje):
        self.archivo.write(puntaje+"\n")
        sel.archivo.close()

    def Vpuntuacion(self):
        f=open("puntuacion.txt","r")
        lineas=f.readline()
        while lineas !="":
            self.fichero.append(lineas)
            lineas=f.readline()
        self.archivo.close()

class Text:
    def __init__(self,FontName = None,FontSize=30):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size= FontSize
        
    def render(self,surface,text,color,pos):
        x,y=pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i,1,color), (x,y))
            y += self.size

            

def main(num):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('sonido.mp3')
    pygame.mixer.music.play(loops=0, start =0.0)
    white=(255,255,255)
    color = (0,0,0)
    Da = Datos()
    text=Text()
    Pared_x= 0
    Pared_y= 0
    pantalla=pygame.display.set_mode((600,600))
    pygame.display.set_caption('Laberinto Mortal JAJAJA')
    Pos_x = 0
    Pso_y = 0
    termino = False
    salir = False
    
main(200)
