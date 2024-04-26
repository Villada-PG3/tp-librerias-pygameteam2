import pygame
from pygame.locals import *
import random

pygame.init()

# crear la ventana
ancho = 500
alto = 500
tamaño_pantalla = (ancho, alto)
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption('Juego de Autos')

# colores
gris = (100, 100, 100)
verde = (76, 208, 56)
rojo = (200, 0, 0)
blanco = (255, 255, 255)
amarillo = (255, 232, 0)

# tamaños de la carretera y los marcadores
ancho_carretera = 300
ancho_marcador = 10
alto_marcador = 50

# coordenadas de los carriles
carril_izquierdo = 150
carril_central = 250
carril_derecho = 350
carriles = [carril_izquierdo, carril_central, carril_derecho]

# carretera y marcadores de borde
carretera = (100, 0, ancho_carretera, alto)
marcador_borde_izquierdo = (95, 0, ancho_marcador, alto)
marcador_borde_derecho = (395, 0, ancho_marcador, alto)

# para animar el movimiento de los marcadores de carril
movimiento_marcador_carril_y = 0

# coordenadas iniciales del jugador
jugador_x = 250
jugador_y = 400

# configuraciones de fotogramas
reloj = pygame.time.Clock()
fps = 120

# configuraciones del juego
fin_del_juego = False
velocidad = 2
puntaje = 0

class Vehiculo(pygame.sprite.Sprite):
    
    def __init__(self, imagen, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # escalar la imagen para que no sea más ancha que el carril
        escala_imagen = 55 / imagen.get_rect().width
        nuevo_ancho = imagen.get_rect().width * escala_imagen
        nuevo_alto = imagen.get_rect().height * escala_imagen
        self.image = pygame.transform.scale(imagen, (int(nuevo_ancho), int(nuevo_alto)))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class VehiculoJugador(Vehiculo):
    
    def __init__(self, x, y):
        imagen = pygame.image.load('./images/car.png')
        super().__init__(imagen, x, y)
        
        
class Motocicleta(Vehiculo):
    def __init__(self, x, y, imagen):
        super().__init__(imagen, x, y)

# grupos de sprites
grupo_jugador = pygame.sprite.Group()
grupo_vehiculos = pygame.sprite.Group()

# crear el auto del jugador
jugador = VehiculoJugador(jugador_x, jugador_y)
grupo_jugador.add(jugador)

# cargar las imágenes de los vehículos
nombres_archivos_imagen = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
imagenes_vehiculos = []
for nombre_archivo_imagen in nombres_archivos_imagen:
    imagen = pygame.image.load('./images/' + nombre_archivo_imagen)
    imagenes_vehiculos.append(imagen)
    
# cargar la imagen de choque
choque = pygame.image.load('./images/crash.png')
rect_choque = choque.get_rect()
tasa_aumento_velocidad = 0.0015
velocidad_cambio_carril = 2
puntaje_para_cambiar_vehiculo = 20

# bucle del juego

teclas_izquierda_presionadas = set()
teclas_derecha_presionadas = set()

corriendo = True
while corriendo:
    aumento_velocidad = velocidad * tasa_aumento_velocidad

    reloj.tick(fps)

    # Dentro del bucle principal, en la sección de eventos:
    for event in pygame.event.get():
        if event.type == QUIT:
            corriendo = False

        # Manejar teclas presionadas
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                teclas_izquierda_presionadas.add(event.key)
            elif event.key == K_RIGHT:
                teclas_derecha_presionadas.add(event.key)
        # Manejar teclas liberadas
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                teclas_izquierda_presionadas.discard(event.key)
            elif event.key == K_RIGHT:
                teclas_derecha_presionadas.discard(event.key)

    # Mover el vehículo basado en las teclas presionadas
    if K_LEFT in teclas_izquierda_presionadas and jugador.rect.center[0] > carril_izquierdo:
        jugador.rect.x -= velocidad_cambio_carril * velocidad
    elif K_RIGHT in teclas_derecha_presionadas and jugador.rect.center[0] < carril_derecho:
        jugador.rect.x += velocidad_cambio_carril * velocidad

    # Verificar colisión después de cambiar de carril
    for vehiculo in grupo_vehiculos:
        if pygame.sprite.collide_rect(jugador, vehiculo):
            fin_del_juego = True
            if K_LEFT in teclas_izquierda_presionadas:
                jugador.rect.left = vehiculo.rect.right
                rect_choque.center = [jugador.rect.left, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]
            elif K_RIGHT in teclas_derecha_presionadas:
                jugador.rect.right = vehiculo.rect.left
                rect_choque.center = [jugador.rect.right, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]
                    # colocar el auto del jugador junto a otro vehículo
                    # y determinar dónde colocar la imagen de choque
            if event.key == K_LEFT:
                jugador.rect.left = vehiculo.rect.right
                rect_choque.center = [jugador.rect.left, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]
            elif event.key == K_RIGHT:
                jugador.rect.right = vehiculo.rect.left
                rect_choque.center = [jugador.rect.right, (jugador.rect.center[1] + vehiculo.rect.center[1]) / 2]
    if puntaje >= puntaje_para_cambiar_vehiculo and not isinstance(jugador, Motocicleta):
    # Cambiar el vehículo a una moto
        imagen_motocicleta = pygame.image.load('./images/moto.png')
        jugador = Motocicleta(jugador.rect.center[0],  jugador.rect.center[1], imagen_motocicleta)
        grupo_jugador.empty()
        grupo_jugador.add(jugador)
        # Ajustar la tasa de aumento
        tasa_aumento_velocidad = 0.0007  # 0.07% de aumento por segundo
        aumento_velocidad = velocidad * tasa_aumento_velocidad

            
    # dibujar el pasto
    pantalla.fill(verde)
    
    # dibujar la carretera
    pygame.draw.rect(pantalla, gris, carretera)
    
    # dibujar los marcadores de borde
    pygame.draw.rect(pantalla, amarillo, marcador_borde_izquierdo)
    pygame.draw.rect(pantalla, amarillo, marcador_borde_derecho)
    
    # dibujar los marcadores de carril
    movimiento_marcador_carril_y += velocidad * 2
    if movimiento_marcador_carril_y >= alto_marcador * 2:
        movimiento_marcador_carril_y = 0
    for y in range(alto_marcador * -2, alto, alto_marcador * 2):
        pygame.draw.rect(pantalla, blanco, (carril_izquierdo + 45, y + movimiento_marcador_carril_y, ancho_marcador, alto_marcador))
        pygame.draw.rect(pantalla, blanco, (carril_central + 45, y + movimiento_marcador_carril_y, ancho_marcador, alto_marcador))
        
    # dibujar el auto del jugador
    grupo_jugador.draw(pantalla)
    
    # agregar un vehículo
    if len(grupo_vehiculos) < 2:
        
        # asegurar que haya suficiente espacio entre los vehículos
        agregar_vehiculo = True
        for vehiculo in grupo_vehiculos:
            if vehiculo.rect.top < vehiculo.rect.height * 1.5:
                agregar_vehiculo = False
                
        if agregar_vehiculo:
            
            # seleccionar un carril al azar
            carril = random.choice(carriles)
            
            # seleccionar una imagen de vehículo al azar
            imagen = random.choice(imagenes_vehiculos)
            vehiculo = Vehiculo(imagen, carril, alto / -2)
            grupo_vehiculos.add(vehiculo)
    
    # hacer que los vehículos se muevan
    for vehiculo in grupo_vehiculos:
        vehiculo.rect.y += velocidad
        
        # eliminar el vehículo una vez que salga de la pantalla
        if vehiculo.rect.top >= alto:
            vehiculo.kill()
            
            # sumar al puntaje
            puntaje += 1
            
            # acelerar el juego después de pasar 5 vehículos
            if puntaje > 0 and puntaje % 5 == 0:
                velocidad += 1
    
    # dibujar los vehículos
    grupo_vehiculos.draw(pantalla)
    
    # mostrar el puntaje
    fuente = pygame.font.Font(pygame.font.get_default_font(), 16)
    texto = fuente.render('Puntaje: ' + str(puntaje), True, blanco)
    rect_texto = texto.get_rect()
    rect_texto.center = (50, 400)
    pantalla.blit(texto, rect_texto)
    
    # verificar si hay una colisión frontal
    if pygame.sprite.spritecollide(jugador, grupo_vehiculos, True):
        fin_del_juego = True
        rect_choque.center = [jugador.rect.center[0], jugador.rect.top]
            
    # mostrar fin del juego
    if fin_del_juego:
        pantalla.blit(choque, rect_choque)
        
        pygame.draw.rect(pantalla, rojo, (0, 50, ancho, 100))
        
        fuente = pygame.font.Font(pygame.font.get_default_font(), 16)
        texto = fuente.render('Fin del juego. ¿Jugar de nuevo? (Presiona Y o N)', True, blanco)
        rect_texto = texto.get_rect()
        rect_texto.center = (ancho / 2, 100)
        pantalla.blit(texto, rect_texto)
            
    pygame.display.update()

    # esperar la entrada del usuario para jugar de nuevo o salir
    while fin_del_juego:
        
        reloj.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                fin_del_juego = False
                corriendo = False
                
            # obtener la entrada del usuario (y o n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reiniciar el juego
                    fin_del_juego = False
                    velocidad = 2
                    puntaje = 0
                    grupo_vehiculos.empty()
                    jugador.rect.center = [jugador_x, jugador_y]
                elif event.key == K_n:
                    # salir de los bucles
                    fin_del_juego = False
                    corriendo = False

pygame.quit()
