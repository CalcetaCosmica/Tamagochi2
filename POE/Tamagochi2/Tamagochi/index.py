import pygame
import sys
import random
import subprocess

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
LIGHT_PINK = (255, 182, 193)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Función para dibujar texto en la pantalla con efecto de brillo
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))

    # Crear superficie para el brillo
    shine_surface = pygame.Surface(text_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shine_surface, LIGHT_PINK, text_rect)
    shine_surface.set_alpha(100 + int(155 * abs((pygame.time.get_ticks() % 1000) / 1000 - 0.5) * 2))
    surface.blit(shine_surface, text_rect.topleft)

    surface.blit(text_obj, text_rect)

# Función para dibujar botones redondeados con efecto de sombra
def draw_button(text, font, color, surface, x, y, width, height, hover=False):
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    border_radius = height // 2
    pygame.draw.rect(button_surface, color, (0, 0, width, height), border_radius=border_radius)

    # Dibujar sombra al colocar el mouse sobre el botón
    if hover:
        shadow_color = (0, 0, 0, 100)
        pygame.draw.rect(button_surface, shadow_color, (0, 0, width, height), border_radius=border_radius)

    # Dibujar borde
    pygame.draw.rect(button_surface, LIGHT_GRAY, (0, 0, width, height), 3, border_radius=border_radius)

    # Dibujar texto
    text_obj = font.render(text, True, BLACK)
    text_rect = text_obj.get_rect(center=(width / 2, height / 2))
    button_surface.blit(text_obj, text_rect)

    surface.blit(button_surface, (x, y))

# Función para la animación de transición
def transition_animation(surface):
    max_bits = 10000
    for _ in range(max_bits):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.circle(surface, color, (x, y), 2)
        pygame.display.update()

# Función principal del juego
def run_game(screen):
    # Cargar la imagen de fondo
    background_image = pygame.image.load(r'star.PNG').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Loop principal
    while True:
        # Dibujar elementos en la pantalla de inicio
        screen.blit(background_image, (0, 0))  # Dibujar fondo

        # Detectar la posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar botones con efecto de sombra al colocar el mouse sobre ellos
        draw_button("Jugar", button_font, WHITE, screen, SCREEN_WIDTH / 2 - 100, 380, 200, 50, hover=(200 <= mouse_pos[0] <= 600 and 380 <= mouse_pos[1] <= 430))
        draw_button("Opciones", button_font, WHITE, screen, SCREEN_WIDTH / 2 - 100, 450, 200, 50, hover=(200 <= mouse_pos[0] <= 600 and 450 <= mouse_pos[1] <= 500))
        draw_button("Salir", button_font, WHITE, screen, SCREEN_WIDTH / 2 - 100, 520, 200, 50, hover=(200 <= mouse_pos[0] <= 600 and 520 <= mouse_pos[1] <= 570))

        # Actualizar la pantalla
        pygame.display.update()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= mouse_pos[0] <= 600 and 380 <= mouse_pos[1] <= 430:
                    return "play"  # Si se presiona "Jugar"
                elif 200 <= mouse_pos[0] <= 600 and 450 <= mouse_pos[1] <= 500:
                    print("¡Haz clic en el botón de Opciones!")
                elif 200 <= mouse_pos[0] <= 600 and 520 <= mouse_pos[1] <= 570:
                    pygame.quit()
                    sys.exit()

# Función para ejecutar el código como una cabecera
def run_header():
    # Crear la pantalla
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pantalla de Inicio")

    # Fuentes
    title_font = pygame.font.Font(None, 80)
    global button_font
    button_font = pygame.font.Font(None, 50)

    while True:
        action = run_game(screen)
        if action == "play":
            transition_animation(screen)  # Ejecutar animación de transición
            pygame.display.update()
            # Ejecutar display.py
            subprocess.run(["python", "display.py"])
            pygame.quit()  # Cerrar el juego actual
            sys.exit()

if __name__ == "__main__":
    run_header()
