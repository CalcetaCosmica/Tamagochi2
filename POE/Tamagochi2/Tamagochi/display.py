import pygame
import sys
import os
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visualización de Imágenes")

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
PASTEL_GREEN = (119, 221, 119)
DARK_RED = (139, 0, 0)
RED = (255, 0, 0)
DARK_PINK = (231, 84, 128)
BLUE = (0, 191, 255)
DARK_BLUE = (0, 0, 139)

# Umbral de la barra de alimentación para cambiar a rojo
BAR_THRESHOLD = 200

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

# Función para dibujar un botón con bordes redondeados
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Función para crear la animación de lluvia de comida
def create_food_rain(food_images, num_food):
    food_sprites = []
    for _ in range(num_food):
        img = random.choice(food_images)
        x = random.randint(0, SCREEN_WIDTH - img.get_width())
        y = random.randint(-300, -50)
        speed = random.randint(1, 5)
        food_sprites.append([img, x, y, speed])
    return food_sprites

# Función para actualizar la animación de lluvia de comida
def update_food_rain(food_sprites):
    for sprite in food_sprites:
        sprite[2] += sprite[3]
        if sprite[2] > SCREEN_HEIGHT:
            sprite[1] = random.randint(0, SCREEN_WIDTH - sprite[0].get_width())
            sprite[2] = random.randint(-300, -50)
            sprite[3] = random.randint(1, 5)

# Función para crear la animación de agua
def create_water_animation(num_drops):
    water_sprites = []
    for _ in range(num_drops):
        drop = pygame.Surface((10, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(drop, BLUE, (0, 0, 10, 30))
        x = random.randint(0, SCREEN_WIDTH - drop.get_width())
        y = random.randint(-300, -50)
        speed = random.randint(5, 10)
        water_sprites.append([drop, x, y, speed])
    return water_sprites

# Función para actualizar la animación de agua
def update_water_animation(water_sprites):
    for sprite in water_sprites:
        sprite[2] += sprite[3]
        if sprite[2] > SCREEN_HEIGHT:
            sprite[1] = random.randint(0, SCREEN_WIDTH - sprite[0].get_width())
            sprite[2] = random.randint(-300, -50)
            sprite[3] = random.randint(5, 10)

# Función para crear la animación de corazones
# Función para crear la animación de corazones utilizando la imagen "Corazon.png"
def create_heart_animation(num_hearts):
    heart_sprites = []
    heart_img = pygame.image.load("Corazon.png").convert_alpha()
    for _ in range(num_hearts):
        x = random.randint(0, SCREEN_WIDTH - heart_img.get_width())
        y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 300)
        speed = random.randint(1, 5)
        heart_sprites.append([heart_img, x, y, speed])
    return heart_sprites

# Función para actualizar la animación de corazones
def update_heart_animation(heart_sprites):
    for sprite in heart_sprites:
        sprite[2] -= sprite[3]
        if sprite[2] < -20:
            sprite[1] = random.randint(0, SCREEN_WIDTH - sprite[0].get_width())
            sprite[2] = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 300)
            sprite[3] = random.randint(1, 5)

# Función para mostrar un mensaje de Game Over
def show_game_over(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

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
    bar_decrease_speed = SCREEN_WIDTH / 60 / 2  # Decrease over 2 seconds at 60 FPS
    bar_decrease_counter = 0
    show_bar = False
    button_feed_rect = pygame.Rect(50, 430, 200, 50)  # Botón para rellenar la barra
    button_reset_rect = pygame.Rect(50, 360, 200, 50)  # Botón para volver a seleccionar la foca
    button_bath_rect = pygame.Rect(50, 290, 200, 50)  # Botón para bañar la foca
    button_love_rect = pygame.Rect(50, 220, 200, 50)  # Botón para apapachar la foca

    # Cargar la imagen de fondo
    background_image = pygame.image.load(r'select.PNG').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Cargar imágenes de comida para la animación de lluvia
    food_folder = 'comida'  # Reemplaza con la ruta a tu carpeta de imágenes de comida
    food_images = load_images_from_folder(food_folder)
    food_sprites = []
    food_rain_active = False
    food_rain_timer = 0
    food_rain_duration = 3 * 60  # 3 segundos a 60 FPS

    water_sprites = []
    water_animation_active = False
    water_animation_timer = 0
    water_animation_duration = 3 * 60  # 3 segundos a 60 FPS

    heart_sprites = []
    heart_animation_active = False
    heart_animation_timer = 0
    heart_animation_duration = 3 * 60  # 3 segundos a 60 FPS

    while True:
        screen.blit(background_image, (0, 0))  # Dibujar fondo

        # Dibujar la barra de alimentación si está visible
        if show_bar:
            bar_color = PASTEL_GREEN if bar_rect.width > BAR_THRESHOLD else DARK_RED
            pygame.draw.rect(screen, bar_color, bar_rect)

        # Reducir la barra de alimentación cada cierto tiempo
        bar_decrease_counter += 1
        if bar_decrease_counter >= 60:  # 60 FPS * 1 segundo
            bar_decrease_counter = 0
            bar_rect.width -= bar_decrease_speed
            if bar_rect.width <= 0:
                show_game_over(screen)

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
                if selected_index is None:
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
                elif button_feed_rect.collidepoint(mouse_pos):
                    bar_rect.width = SCREEN_WIDTH
                    bar_color = PASTEL_GREEN
                    food_rain_active = True
                    food_rain_timer = 0
                    food_sprites = create_food_rain(food_images, 20)
                elif button_reset_rect.collidepoint(mouse_pos):
                    selected_index = None
                    selected_image = None
                    show_bar = False
                elif button_bath_rect.collidepoint(mouse_pos):
                    water_animation_active = True
                    water_animation_timer = 0
                    water_sprites = create_water_animation(20)
                elif button_love_rect.collidepoint(mouse_pos):
                    heart_animation_active = True
                    heart_animation_timer = 0
                    heart_sprites = create_heart_animation(20)

        # Dibujar la cuadrícula de imágenes
        draw_image_grid(screen, images, offset, selected_index)

        # Si hay una imagen seleccionada, hacerla más grande y mostrar los botones
        if selected_index is not None:
            selected_img = pygame.transform.scale(selected_image, (300, 300))
            selected_rect = selected_img.get_rect()
            selected_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)  # Mover hacia abajo
            screen.blit(selected_img, selected_rect)
            # Botones
            draw_rounded_rect(screen, PINK, button_feed_rect, 20)
            draw_rounded_rect(screen, DARK_PINK, button_reset_rect, 20)
            draw_rounded_rect(screen, BLUE, button_bath_rect, 20)
            draw_rounded_rect(screen, DARK_BLUE, button_love_rect, 20)
            font = pygame.font.Font(None, 36)
            feed_text = font.render("Alimentar", True, WHITE)
            reset_text = font.render("Reiniciar", True, WHITE)
            bath_text = font.render("Bañar", True, WHITE)
            love_text = font.render("Apapachar", True, WHITE)
            screen.blit(feed_text, (button_feed_rect.x + 50, button_feed_rect.y + 10))
            screen.blit(reset_text, (button_reset_rect.x + 50, button_reset_rect.y + 10))
            screen.blit(bath_text, (button_bath_rect.x + 70, button_bath_rect.y + 10))
            screen.blit(love_text, (button_love_rect.x + 55, button_love_rect.y + 10))

        # Animación de lluvia de comida
        if food_rain_active:
            update_food_rain(food_sprites)
            for sprite in food_sprites:
                screen.blit(sprite[0], (sprite[1], sprite[2]))
            food_rain_timer += 1
            if food_rain_timer >= food_rain_duration:
                food_rain_active = False

        # Animación de agua
        if water_animation_active:
            update_water_animation(water_sprites)
            for sprite in water_sprites:
                screen.blit(sprite[0], (sprite[1], sprite[2]))
            water_animation_timer += 1
            if water_animation_timer >= water_animation_duration:
                water_animation_active = False

        # Animación de corazones
        if heart_animation_active:
            update_heart_animation(heart_sprites)
            for sprite in heart_sprites:
                screen.blit(sprite[0], (sprite[1], sprite[2]))
            heart_animation_timer += 1
            if heart_animation_timer >= heart_animation_duration:
                heart_animation_active = False

        # Actualizar la pantalla
        pygame.display.update()

        # Limitar a 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    main()
