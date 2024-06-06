import pygame
import sys
import random
import os

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Dimensiones del área de visualización de la cuadrícula
GRID_VIEW_WIDTH = SCREEN_WIDTH
GRID_VIEW_HEIGHT = SCREEN_HEIGHT - 100  # Deja espacio para el desplazamiento

# Dimensiones de las imágenes y la cuadrícula
IMAGE_SIZE = 100
GRID_COLS = 5
GRID_ROWS = 5

# Colores
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
LIGHT_PINK = (255, 182, 193)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Función para cargar las imágenes desde una carpeta
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            img = pygame.transform.scale(img, (IMAGE_SIZE, IMAGE_SIZE))
            images.append(img)
    return images

# Cargar las imágenes de la carpeta indicada
image_folder = 'focas'  # Reemplaza con la ruta a tu carpeta de imágenes
images = load_images_from_folder(image_folder)

# Función para dibujar la cuadrícula de imágenes con desplazamiento y hover
def draw_image_grid(surface, images, offset, selected_index=None):
    if selected_index is not None:
        return  # No dibujar ninguna imagen si hay una seleccionada
    start_index = (offset // IMAGE_SIZE) * GRID_COLS
    start_y = 150  # Para ajustar la posición de las imágenes más abajo
    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            index = start_index + i * GRID_COLS + j
            if index >= len(images):
                return
            x = (SCREEN_WIDTH - (GRID_COLS * (IMAGE_SIZE + 10))) // 2 + j * (IMAGE_SIZE + 10)
            y = start_y + i * (IMAGE_SIZE + 10) - offset % IMAGE_SIZE
            surface.blit(images[index], (x, y))

# Función principal
def main():
    clock = pygame.time.Clock()
    offset = 0  # Desplazamiento inicial
    max_offset = (len(images) // GRID_COLS - GRID_ROWS + 1) * IMAGE_SIZE  # Desplazamiento máximo
    selected_index = None
    selected_image = None
    bar_width = SCREEN_WIDTH
    bar_height = 20
    bar_rect = pygame.Rect(0, 0, bar_width, bar_height)
    bar_decrease_speed = 1
    bar_decrease_counter = 0
    show_bar = False

    # Cargar la imagen de fondo
    background_image = pygame.image.load(r'select.PNG').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        screen.blit(background_image, (0, 0))  # Dibujar fondo

        # Dibujar la barra de alimentación si está visible
        if show_bar:
            pygame.draw.rect(screen, LIGHT_GRAY, bar_rect)

        # Reducir la barra de alimentación cada cierto tiempo
        bar_decrease_counter += 1
        if bar_decrease_counter >= 300:  # 60 FPS * 5 segundos
            bar_decrease_counter = 0
            bar_width -= bar_decrease_speed
            if bar_width <= 0:
                bar_width = 0
            bar_rect.width = bar_width

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                offset += event.y * IMAGE_SIZE
                offset = max(0, min(offset, max_offset))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = (mouse_pos[0] - (SCREEN_WIDTH - (GRID_COLS * (IMAGE_SIZE + 10))) // 2) // (IMAGE_SIZE + 10)
                grid_y = (mouse_pos[1] - 150 + offset) // (IMAGE_SIZE + 10)
                index = (grid_y * GRID_COLS) + grid_x
                if 0 <= grid_x < GRID_COLS and index < len(images):
                    print(f"Imagen {index} seleccionada")
                    selected_index = index
                    selected_image = images[selected_index]
                    bar_width = SCREEN_WIDTH
                    bar_rect.width = bar_width
                    show_bar = True

        # Dibujar la cuadrícula de imágenes
        draw_image_grid(screen, images, offset, selected_index)
        
        # Si hay una imagen seleccionada, hacerla más grande y mostrar los botones
        if selected_index is not None:
            selected_img = pygame.transform.scale(selected_image, (300, 300))
            selected_rect = selected_img.get_rect()
            selected_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)  # Mover hacia abajo
            screen.blit(selected_img, selected_rect)
            # Botones a la izquierda
            pygame.draw.rect(screen, PINK, (50, 50, 100, 50))  # Ejemplo de un botón
            pygame.draw.rect(screen, PINK, (50, 150, 100, 50))  # Ejemplo de un segundo botón

        # Actualizar la pantalla
        pygame.display.update()
        
        # Limitar a 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    main()
