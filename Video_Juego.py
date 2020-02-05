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
        

        # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)


# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')

# Crear objeto reloj
reloj = pygame.time.Clock()

bolita = Bolita()

while True:
    #Establecer FPS
    reloj.tick(60)

    # Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    #Actualizar posicion de la bolita
    bolita.update()     

    # Rellenar pantalla
    pantalla.fill(color_azul)

    #Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)

    #Actualizar los elementos en pantalla
    pygame.display.flip()