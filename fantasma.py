 

class Fantasma ( SpriteMovil ):
    def __init__(self, fichero_imagen, pos_inicial, velocidad):
        SpriteMovil.__init__(self, fichero_imagen, pos_inicial, velocidad) 
        self.vidas = 1
        Fantasma.tiempo_reproduccion = pygame.time.get_ticks()

    def reproducirse(self):
        '''cada 20 segundos los fantasmas se reproducen'''
        if pygame.time.get_ticks() - Fantasma.tiempo_reproduccion > 20000:
            nuevo_fantasma = Fantasma ( "fantasma.gif", self.rect.topleft, 
                                            [-self.velocidad[0], -self.velocidad[1]] )
            sprites.add ( nuevo_fantasma )

    def update (self):  
        self.reproducirse()
                

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
                        sprite.rect.topleft = [0,0]  
        
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
        self.font = pygame.font.SysFont("None", 20)
        self.rect = pygame.rect.Rect(0,0,0,0)

    
    def update(self):
        self.texto = "vidas: %d - puntos: %d - disparos: %d" % (self.pacman.vidas, self.pacman.puntos, self.pacman.disparos)
        self.image = self.font.render(self.texto, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        
        #situamos al marcador en la esquina inferior derecha
        self.rect.topleft = (pygame.display.get_surface().get_width() - self.rect.width, 
                     pygame.display.get_surface().get_height() - self.rect.height)
        
        MiSprite.update (self)



class Mensaje (MiSprite):
    def __init__(self, texto, posicion = None, dim_font = 60, tiempo = 0 ):
        '''Muestra un mensaje en pantalla.
           Si indicamos un tiempo > 0, el mensaje desaparecera cuando transcurra dicho tiempo'''
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



