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
   
  
  
class Marcador (MiSprite):
    def __init__(self, pacman):
        MiSprite.__init__(self)
        self.pacman = pacman
        self.font = pygame.font.SysFont("Arial", 20)
        self.rect = pygame.rect.Rect(0,0,0,0)

    
    def update(self):
        self.texto = 'vidas: %d                 puntos: %d                 disparos: %d' % (self.pacman.vidas, self.pacman.puntos, self.pacman.disparos)
        self.image = self.font.render(self.texto, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        
        #situamos al marcador en la esquina inferior derecha
        self.rect.topleft = (pygame.display.get_surface().get_width() - 600, 
                     pygame.display.get_surface().get_height() - 600)
        print ("Su puntaje es " ,str ( self.pacman.puntos))
        MiSprite.update (self)

   

class Mensaje (MiSprite):
    def __init__(self, texto, posicion = None, dim_font = 60, tiempo = 0 ):

        MiSprite.__init__(self)

        self.texto = texto
        self.font = pygame.font.SysFont("None", dim_font)
        self.image = self.font.render(self.texto, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.tiempo = tiempo
        if self.tiempo > 0:
            self.inicio = pygame.time.get_ticks()
        
        if posicion is None:
            posicion =[(pygame.display.get_surface().get_width() - self.rect.width ) / 2, 
                        (pygame.display.get_surface().get_height() - self.rect.height ) / 2 ]
        
        self.rect.topleft = posicion

    
    def update(self):
        MiSprite.update (self)
        if self.tiempo > 0 and pygame.time.get_ticks() - self.inicio > self.tiempo:
            self.kill()


def ManejarEventos():
    global eventos # explicitamente declaramos que "eventos" es una variable global
    for event in eventos: 
      
        if event.type == pygame.QUIT: 
            sys.exit(0) #se termina el programa
        
     
imagenes = {}
def cargar_imagen ( fichero_imagen ):
    global imagenes
    imagen = imagenes.get ( fichero_imagen, None )
    if imagen is None:
        imagen = pygame.image.load(os.path.join("imagenes",fichero_imagen)).convert()
        imagenes[fichero_imagen] = imagen
        imagen.set_colorkey (  imagen.get_at((0,0)) , pygame.RLEACCEL )
    return imagen


sonidos = {}
def cargar_sonido ( fichero_sonido ):
    global sonidos
    sonido = sonidos.get ( fichero_sonido, None )
    if sonido is None:
        sonido = pygame.mixer.Sound ( os.path.join ("sonidos", fichero_sonido))
        sonidos[fichero_sonido] = sonido
    return sonido


def kill(sprite):
    cargar_sonido("kill.wav").play()
    sprite.kill()
  
  
def game_over():
    '''El juego finaliza cuando no exista ningun pacman o fantasma'''
    existen_fantasmas = existen_pacman = False
    for sprite in sprites:
        if isinstance(sprite, Fantasma):
            existen_fantasmas = True
        elif isinstance (sprite, Pacman):
            existen_pacman = True
    
    return not ( existen_fantasmas and existen_pacman )
 
def informar ( posicion, texto ):
    mensaje = Mensaje ( texto, posicion, 20, 2000)
    sprites.add ( mensaje )
    
class Opcion:

    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, (0, 0, 0))
        self.imagen_destacada = fuente.render(titulo, 1, (200, 0, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self):
        destino_x = 105
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    
    def __init__(self, opciones):
        self.opciones = []
    #Archivo de fuente del menu
        fuente = pygame.font.Font('dejavu.ttf', 20)
        x = 105
        y = 105
        paridad = 1

        self.cursor = Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.seleccionado += 1
            elif k[K_RETURN]:
                # Invoca a la función asociada a la opción.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()
     
        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):

        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)
def comenzar_nuevo_juego():
    print(" Función que muestra un nuevo juego.")
    main()
 
def mostrar_opciones():
    print ("Función que muestra otro menú de opciones.")

def creditos():
    print ("Función que muestra los creditos del programa.")

def salir_del_programa():
    import sys
    print (" Gracias por utilizar este programa.")
    sys.exit(0) 
def main():
    global sprites,eventos,screem
    #inicializamos pygame y la pantalla de juego
    pygame.init()
    
    #Indicamos la dimension de la pantlla de juego
    window = pygame.display.set_mode([900,600])
    pygame.display.set_caption("pacman")  

    #Inicializamos la pantalla con fondo negro
    screen = pygame.display.get_surface()
    screen.fill ([0,0,0])
    
    #creamos una copia de la pantalla para evitar su repintado completo cuando
    #    se redibujen los sprites
    background = screen.copy()


    #creamos los sprites
    sprites = pygame.sprite.RenderUpdates()
    
    pacman = Pacman("pacman.gif", [21,42])
    sprites.add ( pacman )
    
    sprite = Fantasma("fantasma.gif",[100,100], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma.gif",[750,45], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma.gif",[20,150], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma.gif",[20,400], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )

    sprite = Fantasma("fantasma1.png",[500,600], [20, 10] )
    sprite.puntos = 300
    sprites.add ( sprite )
    sprite = Fantasma("fantasma1.png",[610,100], [10, 10] )
    sprite.puntos = 300
    sprites.add ( sprite )
    sprite = Fantasma("fantasma1.png",[420,50], [10, 10] )
    sprite.puntos = 300
    sprites.add ( sprite )
    sprite = Fantasma("fantasma1.png",[80,580], [10, 10] )
    sprite.puntos = 300
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[220,150], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[230,350], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[700,350], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[450,350], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[320,350], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma2.png",[690,400], [1, 2] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma.gif",[750,430], [1, 2] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma1.png",[660,220], [1, 0] )
    sprite.puntos = 300
    sprites.add ( sprite )
    sprite = Fantasma("pacmanevil.png",[305,510], [0, 0] )
    sprite.puntos = 1000
    sprites.add ( sprite )
    

    sprite = Pared ( [150,150,150], [0,30], [900,10] )#-|..--
    sprites.add ( sprite )

    sprite = Pared ( [150,150,150], [140,30], [10,140] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [60,160], [90,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [730,110], [10,50] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [0,110], [70,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [0,210], [120,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [120,210], [10,130] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [120,270], [130,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [170,270], [10,110] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [170,380], [130,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [230,315], [140,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [370,220], [10,230] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [370,220], [200,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [570,160], [10,70] )#|
    sprites.add ( sprite )#falsa
    sprite = Pared ( [150,150,150], [430,280], [150,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [430,280], [10,100] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [60,270], [10,170] )#|
    sprites.add ( sprite )#fantasma
    sprite = Pared ( [150,150,150], [60,385], [50,10] )#|
    sprites.add ( sprite )

    sprite = Pared ( [150,150,150], [200,30], [10,170] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [200,200], [100,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [300,160], [10,100] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [300,160], [220,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [520,110], [10,60] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [580,160], [80,10] )#-
    sprites.add ( sprite )
    #trampa1
    sprite = Pared ( [250,150,150], [530,160], [80,10] )#-
    sprites.add ( sprite )

    
    sprite = Pared ( [150,150,150], [730,160], [80,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [650,80], [10,80] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [590,80], [90,10] )#-
    sprites.add ( sprite )
    sprite = Pared2 ( [250,150,150], [680,40], [10,50] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [460,30], [10,70] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [250,110], [150,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [250,150,150], [300,120], [10,40] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [320,30], [10,50] )#|
    sprites.add ( sprite )
    sprite = Pared ( [250,150,150], [250,70], [10,40] )#|
    sprites.add ( sprite )

    
    sprite = Pared ( [150,150,150], [400,50], [10,70] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [250,30], [10,40] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [190,440], [10,70] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [60,440], [140,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [260,440], [110,10] )#-
    sprites.add ( sprite )#pared
    sprite = Pared ( [150,150,150], [250,500], [200,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [450,430], [10,80] )#|
    sprites.add ( sprite )#pared
    #trampa2
    sprite = Pared2 ( [250,150,150], [250,440], [10,60] )#|
    sprites.add ( sprite )
    sprite = Pared ( [250,150,150], [450,430], [150,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [600,430], [10,90] )#|
    sprites.add ( sprite )
    #trampa
    sprite = Pared2 ( [250,150,150], [600,515], [10,80] )#|
    sprites.add ( sprite )
    
    sprite = Pared ( [150,150,150], [525,340], [10,90] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [525,340], [200,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [660,260], [10,80] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [660,260], [100,10] )#-
    sprites.add ( sprite )
    sprite = Pared2 ( [250,150,150], [660,160], [80,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [760,210], [10,60] )#|
    sprites.add ( sprite )
    sprite = Pared ( [250,150,150], [760,170], [10,40] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [790,90], [110,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [810,210], [90,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [250,150,150], [580,280], [10,60] )#|
    sprites.add ( sprite )
    ####
    sprite = Pared2 ( [250,150,150], [570,222], [10,65] )#|
    sprites.add ( sprite )
    
    sprite = Pared ( [150,150,150], [0,500], [130,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [130,500], [10,70] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [60,550], [10,50] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [250,500], [10,100] )#|
    sprites.add ( sprite )#fantasma
    sprite = Pared ( [150,150,150], [400,500], [10,50] )#|
    sprites.add ( sprite )#fantasma M
    sprite = Pared ( [150,150,150], [530,500], [10,100] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [660,500], [10,100] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [660,500], [150,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [600,430], [70,10] )#-
    sprites.add ( sprite )#fantasma
    sprite = Pared ( [150,150,150], [730,400], [10,100] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [730,400], [100,10] )#-
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [830,320], [10,90] )#|
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [720,555], [100,10] )#-
    sprites.add ( sprite )#vida
    
    
   #items o premios
    sprite = MiSprite ("fruta.gif", [0, 80])
    sprite.comestible = True
    sprite.puntos = 10
    sprites.add ( sprite )

    sprite = MiSprite ("fruta.gif", [220, 50])
    sprite.comestible = True
    sprite.puntos = 10
    sprites.add ( sprite )
    sprite = MiSprite ("fruta2.gif", [870, 350])
    sprite.comestible = True
    sprite.puntos = 20
    sprites.add ( sprite )
    sprite = MiSprite ("fruta0.gif", [300, 420])
    sprite.comestible = True
    sprite.puntos = 15
    sprites.add ( sprite )
 
    sprite = MiSprite ("bola.gif", [30, 330])
    sprite.comestible = True
    sprite.puntos = 5
    sprite.disparos = 20
    sprites.add ( sprite )
    sprite = MiSprite ("bola.gif", [780, 140])
    sprite.comestible = True
    sprite.puntos = 5
    sprite.disparos = 20
    sprites.add ( sprite )
    sprite = MiSprite ("bola.gif", [220, 170])
    sprite.comestible = True
    sprite.puntos = 5
    sprite.disparos = 20
    sprites.add ( sprite )
    sprite = MiSprite ("vida.png", [5, 580])
    sprite.comestible = True
    sprite.vidas = 2
    sprites.add ( sprite )
    sprite = MiSprite ("vida.png", [470, 50])
    sprite.comestible = True
    sprite.vidas = 2
    sprites.add ( sprite )
    sprite = MiSprite ("vida.png", [760, 575])
    sprite.comestible = True
    sprite.vidas = 2
    sprites.add ( sprite )
       
    
    marcador = Marcador ( pacman )
    sprites.add ( marcador )

       
    #bucle de redibujado de los screens
    reloj = pygame.time.Clock() 
      
    sonido_fondo = cargar_sonido ("sonido_fondo.wav").play(-1) #este sonido se repetira indefinidamente al indicar -1 como parametro   
    while not game_over(): 
        eventos = pygame.event.get()
        ManejarEventos ()
        
        sprites.update ()
        sprites.clear (screen, background) 
        pygame.display.update (sprites.draw (screen))        
        
        reloj.tick (40) #tiempo de espera entre frames
    
    #el juego ha finalizado
    sonido_fondo.stop()
    cargar_sonido ( "game_over.wav" ).play()
    sprites.add ( Mensaje ( "Game over" ) )    
    pygame.display.update (sprites.draw (screen))  
  
    #esperamos un cierto tiempo para que se pueda ver lo que ha ocurrido al final del juego
    pygame.time.delay(2000)

    sprites.empty()    
    sprites.add ( Mensaje ( "Game over" ) )    
    screen.fill ([0,0,0])
    pygame.display.update(sprites.draw(screen))
    cargar_sonido ( "game_over.wav" ).play(2)
    
    while True:
        eventos = pygame.event.get()
        ManejarEventos()
if __name__ == '__main__':
    salir = False
    opciones = [
        ("Jugar", comenzar_nuevo_juego),
       # ("Opciones", mostrar_opciones),
       # ("Creditos", creditos),
        ("Salir", salir_del_programa)
        ]

    pygame.font.init()
    screen = pygame.display.set_mode((320, 240))
    fondo = pygame.image.load("fondo.png").convert()
    menu = Menu(opciones)
    

    while not salir:
        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)
