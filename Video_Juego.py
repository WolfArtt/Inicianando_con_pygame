"""
Iniciamos a hacer nuestro juego y comenzamos con la pantalla de juego

"""
import pygame
import sys # para usar exit()

ancho = 640 # ancho pantalla
alto = 480  # alto pantalla
color_azul = (0,0,64) # Color azul para el fondo

class Bolita(pygame.sprite.Sprite):
    #Constructor de bolita
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Cargar Imagen
        self.image = pygame.image.load('imagenes/bolita.png')
        
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()

        # Posicion inicial centrada en pantalla
        self.rect.centerx = ancho/2
        self.rect.centery = alto/2

        # Establecer velocidad inicial
        self.speed = [3,3]

    def update(self):
        #Evitar que salga por debajo la bolita
        if self.rect.bottom >= alto or self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

        #Evitar que salga por la derecha
        if self.rect.right >= ancho or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]

        # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)

class Paleta(pygame.sprite.Sprite):
    #Constructor de paleta
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Cargar Imagen
        self.image = pygame.image.load('imagenes/paleta.png')
        
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()

        # Posicion inicial centrada en X
        self.rect.midbottom = (ancho/2, alto - 20)

        # Establecer velocidad inicial
        self.speed = [0,0]

    def update(self, evento):
        # Buscar si se presiono flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5,0]

        # Si se presiona la flecha derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < ancho:
            self.speed = [5,0]   

        # Si no presionamos nada
        else:
            self.speed = [0,0]
    
          # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    #Constructor de ladrillo
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)

        # Cargar Imagen
        self.image = pygame.image.load('imagenes/ladrillo.png')
        
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()

        # Posicion inicial, provista externamente
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidad_ladrillos):
        pygame.sprite.Group.__init__(self)
        
        # Definimos la posicion en x y y 
        pos_x = 0
        pos_y = 20
        ''' Borramos nuestros 2 constructores creados y 
            agregaremos un for para crear mas Ladrillos
        '''
        for i in range(cantidad_ladrillos):
            ladrillo = Ladrillo((pos_x,pos_y))  # Llamamos a nuestra clase Ladrillo con parametros posicion
            self.add(ladrillo)  # Aniadimos los ladrillos
            
            pos_x += ladrillo.rect.width    # Decidimos en que posicion iran nuestros ladrillos, aca le decimos que iran en lo ancho(width)
            # Con este if acomodamos nuestros ladrillos, cada vez que no haya espacio en el ancho e ira un espacio abajo para acomodarse
            if pos_x >= ancho:  # Con este if acomodamos nuestros ladrillos, cada vez que no haya espacio en el ancho e ira un espacio abajo para acomodarse
                pos_x = 0
                pos_y += ladrillo.rect.height   # Toma la posicion en el alto(heigth) el siguiente ladrillo es decir por debajo de el 1er ladrillo a la izquierda

# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')

# Crear objeto reloj
reloj = pygame.time.Clock()
# Ajustar repeticion de evento de la tecla precionada
pygame.key.set_repeat(30)

# Lamamos a nuestros constructores de las clases
bolita = Bolita()
paleta = Paleta()
muro = Muro(100)

while True:
    #Establecer FPS
    reloj.tick(60)

    # Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

        # Buscar eventos por teclado
        elif evento.type == pygame.KEYDOWN:
            paleta.update(evento)

    # Actualizar posicion de la bolita
    bolita.update()

    # Colision entre bolita y jugador
    if pygame.sprite.collide_rect(bolita, paleta):
         bolita.speed[1] = -bolita.speed[1]

    # Colision bolita con el Muro
    lista = pygame.sprite.spritecollide(bolita,muro, False)
    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)
    
    # Rellenar pantalla
    pantalla.fill(color_azul)

    # Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)

    # Dibujar paleta del jugador en pantalla
    pantalla.blit(paleta.image, paleta.rect)

    # Dibujar Ladrillos
    muro.draw(pantalla)

    # Actualizar los elementos en pantalla
    pygame.display.flip()