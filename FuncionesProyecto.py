

def ManejarEventos():
    global eventos 
    for event in eventos: 
      
        if event.type == pygame.QUIT: 
            sys.exit(0) 
        
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
    
if __name__ == "__main__":    
    pygame.init()
    window = pygame.display.set_mode([800,600])
    pygame.display.set_caption("pacman")  
    screen = pygame.display.get_surface()
    screen.fill ([0,0,0])
    background = screen.copy()
    sprites = pygame.sprite.RenderUpdates()
    pacman = Pacman("pacman.gif", [0,0])
    sprites.add ( pacman )
    sprite = Fantasma("fantasma.gif",[100,20], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Fantasma("fantasma.gif",[20,200], [1, 1] )
    sprite.puntos = 100
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [72,72], [100,10] )
    sprites.add ( sprite )
    sprite = Pared ( [150,150,150], [172,172], [10,100] )
    sprites.add ( sprite )
    sprite = MiSprite ("fruta.gif", [0, 100])
    sprite.comestible = True
    sprite.puntos = 10
    sprites.add ( sprite )
    sprite = MiSprite ("fruta.gif", [200, 150])
    sprite.comestible = True
    sprite.puntos = 10
    sprites.add ( sprite )
    sprite = MiSprite ("bola.gif", [130, 330])
    sprite.comestible = True
    sprite.puntos = 5
    sprite.disparos = 20
    sprites.add ( sprite )
       
    marcador = Marcador ( pacman )
    sprites.add ( marcador )

    reloj = pygame.time.Clock() 
      
    sonido_fondo = cargar_sonido ("sonido_fondo.wav").play(-1)   
    while not game_over(): 
        eventos = pygame.event.get()
        ManejarEventos ()
        
        sprites.update ()
        sprites.clear (screen, background) 
        pygame.display.update (sprites.draw (screen))        
        
        reloj.tick (40) 
  
    sonido_fondo.stop()
    cargar_sonido ( "game_over.wav" ).play()
    sprites.add ( Mensaje ( "Game over" ) )    
    pygame.display.update (sprites.draw (screen))  
  
    pygame.time.delay(2000)

    sprites.empty()    
    sprites.add ( Mensaje ( "Game over" ) )    
    screen.fill ([0,0,0])
    pygame.display.update(sprites.draw(screen))
    cargar_sonido ( "game_over.wav" ).play(2)
    
    while True:
        eventos = pygame.event.get()
        ManejarEventos()
            
