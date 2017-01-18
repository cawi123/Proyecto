import sys, pygame
from pygame.locals import *

 
# Constantes
WIDTH = 900
HEIGHT = 500
MposX =300


cont=6
direc=True
i=0
xixf={}#xinicial y xfinal
Rxixf={}
#===========================================================
#=================IMAGEN====================================

def imagen(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error:
                raise SystemExit
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
#================================================================ 

#======================TECLADO===================================
#================================================================
def teclado():
    teclado = pygame.key.get_pressed()
     
    global MposX
    global cont, direc
    
        
    if teclado[K_RIGHT]:
        MposX+=2
        cont+=1
        direc=True
    elif teclado[K_LEFT]:
        MposX-=2
        cont+=1
        direc=False
    elif teclado[K_q]:
        #SALTO
        MposX-=2
    #else :
         #cont=6
        
    return 
    

#===================SPRITE===============================
#========================================================
def sprite():

    global cont
 
    xixf[0]=(0,0,33,45)
    xixf[1]=(33,0,34,45)
    xixf[2]=(67,0,34,45)
    xixf[3]=(101,0,33,45)
    xixf[4]=(130,0,29,45)
    xixf[5]=(159,0,29,45)
    xixf[6]=(192,0,33,44)
    xixf[7]=(225,0,34,45)
    xixf[8]=(262,0,37,45)
    xixf[9]=(299,0,37,45)
    xixf[10]=(331,0,32,45)
    xixf[11]=(364,0,33,45)
    
    
    Rxixf[0]=(364,0,33,45)
    Rxixf[1]=(331,0,32,45)
    Rxixf[2]=(299,0,37,45)
    Rxixf[3]=(262,0,37,45)
    Rxixf[4]=(225,0,34,45)
    Rxixf[5]=(192,0,33,44)
    Rxixf[6]=(159,0,29,45)
    Rxixf[7]=(130,0,29,45)
    Rxixf[8]=(101,0,33,45)
    Rxixf[9]=(67,0,34,45)
    Rxixf[10]=(33,0,34,45)
    Rxixf[11]=(0,0,33,45)
    
    p=6
    
    global i
        
    if cont==p:
        i=0
    
    if cont==p*2:
        i=1
    
    if cont==p*3:
        i=2
    
    if cont==p*4:
        i=3
    
    if cont==p*5:
        i=4
    
    if cont==p*6:
       i=5
       cont=0
    
    return





def main():
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")
    
 
    fondo = imagen("fondo.png")
    
          
    mario = imagen("P11.png",True)   
    mario_inv=pygame.transform.flip(mario,True,False);
     
    clock = pygame.time.Clock()
    
      
 
    # el bucle principal del juego
    while True:
        
        time = clock.tick(60)
        
        sprite()
        teclado()
        
       
    
        fondo = pygame.transform.scale(fondo, (1000, 400))
             
        screen.blit(fondo, (0, 0))
        
        if direc==True: 
            screen.blit(mario, ( MposX, 318),(xixf[i]))
    
        if direc==False: 
            screen.blit(mario_inv, ( MposX, 318),(Rxixf[i]))
    
        pygame.display.flip()
        
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    return 0



 
if __name__ == '__main__': 
    main()
