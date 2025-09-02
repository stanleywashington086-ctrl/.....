import pygame
import random
import sys
import os
from pygame import mixer

# Inicializar pygame
pygame.init()
mixer.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carta Romántica")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)

# Fuente
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 40, bold=True)

# Función para cargar recursos con manejo de rutas para el ejecutable
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar música (compatible con el ejecutable)
try:
    music_path = resource_path('romantic_music.mp3')
    mixer.music.load(music_path)
    mixer.music.play(-1)  # -1 para reproducir en bucle
except Exception as e:
    print(f"No se pudo cargar la música: {e}")

# Clase para los corazones
class Heart:
    def __init__(self):
        self.size = random.randint(10, 30)
        self.x = random.choice([
            random.randint(0, WIDTH),  # Bordes izquierdo/derecho
            random.randint(0, WIDTH)   # O cualquier posición para bordes superior/inferior
        ])
        
        # Determinar si el corazón va a subir por el borde izquierdo o derecho
        if self.x < WIDTH // 2:
            self.side = "left"
            self.x = 0
        else:
            self.side = "right"
            self.x = WIDTH
        
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.color = (random.randint(200, 255), random.randint(0, 100), random.randint(100, 150))
    
    def move(self):
        self.y -= self.speed
        # Mover ligeramente hacia el centro
        if self.side == "left":
            self.x += 0.5
        else:
            self.x -= 0.5
            
        # Si el corazón sale de la pantalla, reiniciarlo
        if self.y < -self.size:
            self.__init__()
    
    def draw(self):
        # Dibujar un corazón simple
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size/2)
        pygame.draw.circle(screen, self.color, (self.x + self.size/2, self.y), self.size/2)
        pygame.draw.polygon(screen, self.color, [
            (self.x - self.size/2, self.y),
            (self.x + self.size, self.y),
            (self.x + self.size/4, self.y + self.size/2)
        ])

# Crear corazones
hearts = [Heart() for _ in range(20)]

# Texto de la carta
message = """
Querido Cristian,

Hoy quiero decirte que eres lo más 
importante en mi vida. Cada momento 
a tu lado es un regalo que atesoro 
en lo más profundo de mi corazón.

Tu sonrisa ilumina mis días y tu 
amor da sentido a mi existencia.

Con todo mi amor,
Kimberly
"""

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Control de música
            elif event.key == pygame.K_p:
                if mixer.music.get_busy():
                    mixer.music.pause()
                else:
                    mixer.music.unpause()
            elif event.key == pygame.K_s:
                mixer.music.stop()
            elif event.key == pygame.K_r:
                mixer.music.play()
    
    # Fondo
    screen.fill(WHITE)
    
    # Dibujar corazones
    for heart in hearts:
        heart.move()
        heart.draw()
    
    # Dibujar carta
    pygame.draw.rect(screen, PINK, (50, 50, WIDTH-100, HEIGHT-100), border_radius=20)
    pygame.draw.rect(screen, BLACK, (50, 50, WIDTH-100, HEIGHT-100), 2, border_radius=20)
    
    # Título
    title = title_font.render("Para Ti", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
    
    # Mensaje
    y_offset = 150
    for line in message.split('\n'):
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
        y_offset += 30 
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()