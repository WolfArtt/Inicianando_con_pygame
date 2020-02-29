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


#Clase escena definimos la estructura basica de nuestras escenas
class Escena:
    def __init__(self): # Constructor
        "Inicializacion"
        self.proxima_escena = False
        self.jugando = True
        #pass           Para indicar que posteriores clases implementaran el metodo
    
    def leer_eventos(self, eventos):
        "Lee la lista de todos los eventos"
        pass
    
    def actualizar(self):
        "Calculos y logica"
        pass

    def dibujar(self, pantalla):
        "Dibuja los objetos en pantalla"
        pass

    def cambiar_escena(self, escena):
        "Selecciona la nueva escena a ser desplegada"
        self.proxima_escena = escena

# Clase Director para controlar nuestras escenas
class Director:
    def __init__(self, titulo = "", res = (ancho,alto)):    # Mandar titulo y la referencia de la pantalla
        pygame.init()
        # Inicializando pantalla
        self.pantalla = pygame.display.set_mode(res)
        # Configurar titulo de pantalla
        pygame.display.set_caption(titulo)
        # Crear el reloj
        self.reloj = pygame.time.Clock()
        self.escena = None  # Variable para guardar la escena actual para ser desplegada
        self.escenas = {}   # Diccionario para guardar escenas del juego

    def ejecutar(self, escena_inicial, fps = 60):
        self.escena = self.escenas[escena_inicial]
        jugando = True
        while jugando:
            self.reloj.tick(fps)
            eventos = pygame.event.get()
            # Revisar todos los eventos
            for evento in eventos:
                # Si se presiona la tachita de la barra de titulo
                if evento.type == pygame.QUIT:
                    # cerrar el videojuego.
                    jugando = False

            self.escena.leer_eventos(eventos)
            self.escena.actualizar()
            self.escena.dibujar(self.pantalla)

            self.elegirEscena(self.escena.proxima_escena)

            if jugando:
                jugando = self.escena.jugando

            pygame.display.flip()

        time.sleep(3)

    def elegirEscena(self, proxima_escena):
        if proxima_escena:
            if proxima_escena not in self.escenas:
                self.agregarEscena(proxima_escena)
            self.escena = self.escenas[proxima_escena]

    def agregarEscena(self, escena):
        escenaClase = 'Escena'+escena
        escenaObj = globals()[escenaClase]
        self.escenas[escena] = escenaObj();


class EscenaNivel1(Escena):
    def __init__(self):
        Escena.__init__(self)
        # Llamamos a nuestros constructores de las clases
        self.bolita = Bolita()
        self.paleta = Paleta()
        self.muro = Muro(100)

        self.puntuacion = 0
        self.vidas = 3
        self.esperando_saque = True
        # Ajustar repeticion de evento de la tecla precionada
        pygame.key.set_repeat(30)

    def leer_eventos(self, eventos):
        for evento in eventos:
            # Buscar eventos por teclado
            if evento.type == pygame.KEYDOWN:
                self.paleta.update(evento)

                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.bolita.rect.centerx < ancho/2:
                        self.bolita.speed = [3,-3]
                    else:
                        self.bolita.speed = [-3,-3]

    def actualizar(self):    
        # Actualizar posicion de la bolita
        if self.esperando_saque == False:
            self.bolita.update()
        else:
            self.bolita.rect.midbottom = self.paleta.rect.midtop

        # Colision entre bolita y jugador
        if pygame.sprite.collide_rect(self.bolita, self.paleta):
            self.bolita.speed[1] = -self.bolita.speed[1]

        # Colision bolita con el Muro
        lista = pygame.sprite.spritecollide(self.bolita,self.muro, False)
        if lista:
            ladrillo = lista[0]
            cx = self.bolita.rect.centerx
            if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
                self.bolita.speed[0] = -self.bolita.speed[0]
            else:
                self.bolita.speed[1] = -self.bolita.speed[1]
            self.muro.remove(ladrillo)
            self.puntuacion += 10
        
        # Revisar si la bolita sale de la pantalla
        if self.bolita.rect.top > alto:
            self.vidas -= 1 # Decrementar vidas
            self.esperando_saque = True

        if self.vidas <= 0:
            #self.jugando = False  # El juego termina llamando una funcion
            self.jugandocambiar_escena('JuegoTerminado')

    def dibujar(self, pantalla):

        # Rellenar pantalla
        pantalla.fill(color_azul)

        # Mostrar puntuacion
        self.mostrar_puntuacion(pantalla)

        # Mostrar vidas
        self.mostrar_vidas(pantalla)

        # Dibujar bolita en pantalla
        pantalla.blit(self.bolita.image, self.bolita.rect)

        # Dibujar paleta del jugador en pantalla
        pantalla.blit(self.paleta.image, self.paleta.rect)

        # Dibujar Ladrillos
        self.muro.draw(pantalla)

    def mostrar_puntuacion(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        texto = fuente.render(str(self.puntuacion).zfill(5), True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0,0]
        pantalla.blit(texto, texto_rect)

    def mostrar_vidas(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        cadena = "Vidas: " + str(self.vidas).zfill(2)
        texto = fuente.render(cadena, True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.topright = [ancho,0]
        pantalla.blit(texto, texto_rect)  

class EscenaJuegoTerminado(Escena):
    def actualizar(self):
        self.jugando = False

    def dibujar(self, pantalla):
        fuente = pygame.font.SysFont('Arial', 42)
        texto = fuente.render('Juego Terminado Perdedor', True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.center = [ancho/2 , alto/2]
        pantalla.blit(texto, texto_rect)

#Clases para cada uno de nuestros dibujos
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

director = Director('Juego de Ladrillos', (ancho, alto))
director.agregarEscena('Nivel1')
director.ejecutar('Nivel1')

"""
# Iniciando pantalla
pantalla = pygame.display.set_mode((ancho,alto))

# Cambiaremos titulo de pantalla
pygame.display.set_caption('Juego de ladrillos')

# Crear objeto reloj
reloj = pygame.time.Clock()
# Ajustar repeticion de evento de la tecla precionada
pygame.key.set_repeat(30)
"""