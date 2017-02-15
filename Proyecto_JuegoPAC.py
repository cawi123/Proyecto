import pygame
import sys, copy, random, os
from pygame.locals import *            
 
class MiSprite ( pygame.sprite.Sprite ):

    def __init__(self, fichero_imagen = None, pos_inicial = [0,0]):
        pygame.sprite.Sprite.__init__(self) 
        

        if not fichero_imagen is None:
            self.image = cargar_imagen(fichero_imagen)
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_inicial
        
    def update (self):
        pygame.sprite.Sprite.update ( self )
        
  

class SpriteMovil ( MiSprite ):
    def __init__(self, fichero_imagen, pos_inicial, velocidad):
        MiSprite.__init__(self, fichero_imagen, pos_inicial) 
        self.rect.topleft = pos_inicial
        self.velocidad = velocidad
        
    def update (self):       
        #la funcion "copy" crea una copia del rectangulo  
        copia_rect = copy.copy(self.rect)
       
        self.rect.move_ip ( self.velocidad[0], self.velocidad[1]) 
        colisiones = pygame.sprite.spritecollide(self, sprites, False)
        for colision in colisiones:
            if colision != self:
                if hasattr ( colision, "infranqueable" ):
                    if colision.infranqueable:
                        self.velocidad[0]=0
                        self.velocidad[1]=0
                        self.rect = copia_rect
                        return     
            
        screen = pygame.display.get_surface () 
            
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidad[1] = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.velocidad[1] = 0
            
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocidad[0] = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velocidad[0] = 0
                   
 
class Pacman ( SpriteMovil ):
    NUMERO_FOTOGRAMAS = 8
    
    def __init__(self, fichero_imagen, pos_inicial):
        SpriteMovil.__init__(self, fichero_imagen, pos_inicial, [1,0]) 
        self.vidas = 3
        self.puntos = 0
        self.disparos = 5
        
        self.__imagenArriba = {}
        self.__imagenAbajo = {}
        self.__imagenDerecha = {}
        self.__imagenIzquierda = {}
        
        for i in range(0, self.NUMERO_FOTOGRAMAS, 1):
            self.__imagenIzquierda[i] = cargar_imagen("pacman-izquierda" + str(i+1) + ".gif")
            self.__imagenDerecha[i] = cargar_imagen("pacman-derecha" + str(i+1) + ".gif")
            self.__imagenArriba[i] = cargar_imagen("pacman-arriba" + str(i+1) + ".gif")
            self.__imagenAbajo[i] = cargar_imagen("pacman-abajo" + str(i+1) + ".gif")
        
        self.__fotogramasActuales = self.__imagenDerecha
        self.__fotogramaActual = 1
        self.__tiempoCambioFotograma = pygame.time.get_ticks()


    def update (self):
        global eventos # explicitamente declaramos que "eventos" es una variable global

        #v = 1
        v=3
        for event in eventos:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.velocidad[0] = -v
                    self.velocidad[1] = 0
                elif event.key == pygame.K_RIGHT:
                    self.velocidad[0] = v
                    self.velocidad[1] = 0
                elif event.key == pygame.K_UP:
                    self.velocidad[1] = -v
                    self.velocidad[0] = 0
                elif event.key == pygame.K_DOWN:
                    self.velocidad[1] = v
                    self.velocidad[0] = 0
                elif event.key == pygame.K_SPACE:
                    if self.disparos > 0:
                        if self.velocidad == [0,0]:
                            bala = Bala (self, [3, 0])
                        else:
                            bala = Bala (self, [self.velocidad[0] * 3, self.velocidad[1] * 3])
                        sprites.add ( bala )
                        self.disparos -= 1
                    

        SpriteMovil.update(self)
        
        #se cambia la imagen de pacman segun la direccion
        if self.velocidad[0] > 0:
            self.__fotogramasActuales = self.__imagenDerecha
        elif self.velocidad[0] < 0:
            self.__fotogramasActuales = self.__imagenIzquierda
        elif self.velocidad[1] > 0:
            self.__fotogramasActuales = self.__imagenAbajo
        elif self.velocidad[1] < 0:
            self.__fotogramasActuales = self.__imagenArriba        
       
        if pygame.time.get_ticks() - self.__tiempoCambioFotograma > 100:
            self.__fotogramaActual = (self.__fotogramaActual + 1) % self.NUMERO_FOTOGRAMAS 
            self.__tiempoCambioFotograma = pygame.time.get_ticks()

        self.image = self.__fotogramasActuales[self.__fotogramaActual]
        
        #global sprites  
        #se obtiene todos los sprites con los que colisiona. El ultimo parametro indica que no queremos destruir automaticamente los sprites con los que colisiona  
        sprites_choque = pygame.sprite.spritecollide(self, sprites, False)
        for sprite in sprites_choque:
            if sprite != self:
                if hasattr ( sprite, "disparos" ):
                    self.disparos += sprite.disparos
                    informar ( self.rect.topright, "disparos %d" % (sprite.disparos) )
                if hasattr ( sprite, "comestible" ): #comprobamos si el sprite tiene un atributo llamado "comestible"
                    if sprite.comestible:
                        if hasattr ( sprite, "puntos" ):
                            self.puntos += sprite.puntos
                            informar ( self.rect.bottomright, "puntos %d" % (sprite.puntos) )
                        if hasattr ( sprite, "vidas" ):
                            self.vidas += sprite.vidas
                            informar ( self.rect.bottomright, "vidas %d" % (sprite.vidas) )
                        kill(sprite) #destruimos el sprite
        


class Fantasma ( SpriteMovil ):
    def __init__(self, fichero_imagen, pos_inicial, velocidad):
        SpriteMovil.__init__(self, fichero_imagen, pos_inicial, velocidad) 
        self.vidas = 1
        Fantasma.tiempo_reproduccion = pygame.time.get_ticks()

    def reproducirse(self):
        '''cada 20 segundos los fantasmas se reproducen'''
        if pygame.time.get_ticks() - Fantasma.tiempo_reproduccion > 10000:
            nuevo_fantasma = Fantasma ( "fantasma.gif", self.rect.topleft, 
                                            [-self.velocidad[0], -self.velocidad[1]] )
            sprites.add ( nuevo_fantasma )
            nuevo_fantasma2 = Fantasma ( "fantasma1.png", self.rect.topleft, 
                                            [-self.velocidad[0], -self.velocidad[1]] )
            nuevo_fantasma3 = Fantasma ( "fantasma2.png", self.rect.topleft, 
                                            [-self.velocidad[0], -self.velocidad[1]] )
            sprites.add ( nuevo_fantasma, nuevo_fantasma2, nuevo_fantasma3)

    def update (self):  
        self.reproducirse()
                
        #comprobamos si el fantasma ha capturado al pacman 
        global sprites
        sprites_choque = pygame.sprite.spritecollide(self, sprites, False)
        for sprite in sprites_choque:
            if sprite!= self:
                if not isinstance(sprite,Fantasma) and hasattr(sprite, "vidas"):
                    sprite.vidas -= 1
                    cargar_sonido("kill.wav").play()
                    if sprite.vidas <= 0:
                        kill(sprite)
                    else:
                        cargar_sonido ("death.wav").play()
                        sprite.rect.topleft = [21,42]  
        
        #su velocidad es 0 si ha colisionado con un objeto infranqueable   
        if self.velocidad[0] == 0 and self.velocidad[1] == 0:
            self.velocidad[0]= random.choice([-2, -1, 1 , 2])
            self.velocidad[1] = random.choice([-2, -1, 1 , 2])
        else:
            if self.rect.top <= 0:
                self.velocidad[1] = random.choice([1,2])
                self.velocidad[0]= random.choice([-2, -1, 1 , 2])
            elif self.rect.bottom >= pygame.display.get_surface().get_height():
                self.velocidad[1] = -random.choice([1,2])
                self.velocidad[0]= random.choice([-2, -1, 1 , 2])
            
            if self.rect.left <= 0:
                self.velocidad[0] = random.choice([1,2])
                self.velocidad[1]= random.choice([-2, -1, 1 , 2])
            elif self.rect.right >= pygame.display.get_surface().get_width():
                self.velocidad[0] = -random.choice([1,2])
                self.velocidad[1]= random.choice([-2, -1, 1 , 2])
        
        SpriteMovil.update (self)
      
    

class Pared ( MiSprite ):
    def __init__(self, color, pos_inicial, dimension):
        MiSprite.__init__(self)
    
        self.image = pygame.Surface(dimension) #creamos una superficie de las dimensiones indicadas
        self.image.fill(color)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_inicial
        self.infranqueable = True

    
    def update(self):
        MiSprite.update(self)

class Pared2 ( MiSprite ):
    def __init__(self, color, pos_inicial, dimension):
        MiSprite.__init__(self)
    
        self.image = pygame.Surface(dimension) #creamos una superficie de las dimensiones indicadas
        self.image.fill(color)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_inicial
        self.infranqueable = False
    def update(self):
        MiSprite.update(self)
    

class Bala ( MiSprite ):
    RADIO = 4
    COLOR = [255,0,0]
    
    def __init__(self, disparador, velocidad):
        MiSprite.__init__(self)
        
        self.velocidad = velocidad
        self.disparador = disparador
            
        pos_disparo = [disparador.rect.center[0], disparador.rect.center[1]]                         
        
        self.image = pygame.Surface([Bala.RADIO * 2, Bala.RADIO * 2]) #creamos una superficie de las dimensiones indicadas
        pygame.draw.circle(self.image, Bala.COLOR, [Bala.RADIO, Bala.RADIO], Bala.RADIO)        
        
            
        self.rect = self.image.get_rect()
        self.rect.topleft = pos_disparo
        
        cargar_sonido ( "disparo.wav" ).play()


    
    def update(self):
        sprites_choque = pygame.sprite.spritecollide(self, sprites, False)
        for sprite in sprites_choque:
            if sprite != self and sprite != self.disparador: # a chocado con algo
                if hasattr(sprite, "vidas"):
                    sprite.vidas -= 1
                    cargar_sonido("kill.wav").play()
                    if sprite.vidas <= 0:
                        if hasattr ( sprite, "puntos" ) and hasattr (self.disparador, "puntos"):
                            self.disparador.puntos += sprite.puntos
                            informar ( sprite.rect.bottomright, "puntos %d" % (sprite.puntos) )
                        kill(sprite)            
                if not isinstance(sprite, Mensaje):
                    self.kill() # se autodestruye
                    return
 
        self.rect.move_ip ( self.velocidad[0], self.velocidad[1]) 
        
        #la bala se autodestruye cuando sale fuera de la pantalla
        if self.rect.top < 0 or self.rect.bottom > screen.get_height() or \
            self.rect.left < 0 or self.rect.right > screen.get_width():
                self.kill()
                return
                
        MiSprite.update(self)
  
    
