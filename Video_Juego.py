"""
Iniciamos a hacer nuestro juego y comenzamos con la pantalla de juego

"""
import pygame
import sys # para usar exit()
import time # Para usar time

ancho = 640 # ancho pantalla
alto = 480  # alto pantalla
color_azul = (0,0,64) # Color azul para el fondo
color_blanco = (255,255,255) # Color blanco, para textos

pygame.init()

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
        if self.rect.top <= 0: # Borramos la parte en que la bolita rebota de la parte inferior
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

# Funcion llamada tras dejar ir la bolita
def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 42)
    texto = fuente.render('Juego Terminado Perdedor', True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.center = [ancho/2 , alto/2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Pausar por 3 segundos
    time.sleep(3)
    # Salir
    sys.exit()

def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0,0]
    pantalla.blit(texto, texto_rect)

def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, color_blanco)
    texto_rect = texto.get_rect()
    texto_rect.topright = [ancho,0]
    pantalla.blit(texto, texto_rect)    

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
puntuacion = 0
vidas = 3
esperando_saque = True

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

            if esperando_saque == True and evento.key == pygame.K_SPACE:
                esperando_saque = False
                if bolita.rect.centerx < ancho/2:
                    bolita.speed = [3,-3]
                else:
                    bolita.speed = [-3,-3]

    # Actualizar posicion de la bolita
    if esperando_saque == False:
        bolita.update()
    else:
        bolita.rect.midbottom = paleta.rect.midtop

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
        puntuacion += 10
    
    # Revisar si la bolita sale de la pantalla
    if bolita.rect.top > alto:
        vidas -= 1 # Decrementar vidas
        esperando_saque = True

    # Rellenar pantalla
    pantalla.fill(color_azul)

    # Mostrar puntuacion
    mostrar_puntuacion()

    # Mostrar vidas
    mostrar_vidas()

    # Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)

    # Dibujar paleta del jugador en pantalla
    pantalla.blit(paleta.image, paleta.rect)

    # Dibujar Ladrillos
    muro.draw(pantalla)

    # Actualizar los elementos en pantalla
    pygame.display.flip()

    if vidas <= 0:
        juego_terminado()  # El juego termina llamando una funcion
