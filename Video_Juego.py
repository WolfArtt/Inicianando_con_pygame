"""
Iniciamos a hacer nuestro juego y comenzamos con la pantalla de juego
"""
import pygame
import sys

ancho = 640
alto = 480
color_azul = (0,0,64) # Color azul para el fondo

class Bolita(pygame.sprite.Sprite):
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

# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')

# Crear objeto reloj
reloj = pygame.time.Clock()
# Ajustar repeticion de evento de la tecla precionada
pygame.key.set_repeat(30)

bolita = Bolita()
paleta = Paleta()

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

    #Actualizar posicion de la bolita
    bolita.update()     

    # Rellenar pantalla
    pantalla.fill(color_azul)

    #Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)

    #Dibujar paleta del jugador en pantalla
    pantalla.blit(paleta.image, paleta.rect)

    #Actualizar los elementos en pantalla
    pygame.display.flip()