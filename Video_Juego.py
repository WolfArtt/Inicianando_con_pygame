"""
Iniciamos a hacer nuestro juego y comenzamos con la pantalla de juego
"""
import pygame
import sys

ancho = 640
alto = 480

# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')
while True:
    # Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()