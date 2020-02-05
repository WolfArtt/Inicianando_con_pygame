"""
Iniciamos a hacer nuestro juego y comenzamos con la pantalla de juego
"""
import pygame
import sys

ancho = 640
alto = 480

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

# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')

bolita = Bolita()

while True:
    # Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    #Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)

    #Actualizar los elementos en pantalla
    pygame.display.flip()