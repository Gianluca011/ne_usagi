import json
import os
import time
import random
import pygame

# Importamos configuraciones de otro módulo
from config import SAVE_PATH, WIDTH, HEIGHT, ASSETS_DIR

pygame.font.init()
font = pygame.font.SysFont("arial", 14, bold=True)


# --- Rutas y guardado ---
def load_data():
    default_data = {
        "hambre": 100,
        "energia": 100,
        "felicidad": 100,
        "ultimo_tiempo": time.time(),
    }
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r") as f:
            data = json.load(f)
        for key, value in default_data.items():
            if key not in data:
                data[key] = value
        return data
    return default_data


def save_data(data):
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f)


# --- Funciones auxiliares UI (Mantendremos estas aquí por ahora) ---
def get_bar_color(value):
    from config import COLOR_HIGH, COLOR_MID, COLOR_LOW

    if value >= 80:
        return COLOR_HIGH
    elif value >= 40:
        return COLOR_MID
    else:
        return COLOR_LOW


def draw_bar(surface, x, y, width, height, value, max_value):
    from config import COLOR_BAR_BG, COLOR_BAR_BORDER

    color = get_bar_color(value)

    # Fondo de la barra
    pygame.draw.rect(surface, COLOR_BAR_BG, (x, y, width, height))

    # Relleno
    fill_width = int((value / max_value) * width)
    pygame.draw.rect(surface, color, (x, y, fill_width, height))

    # Borde
    pygame.draw.rect(surface, COLOR_BAR_BORDER, (x, y, width, height), 2)

    # Texto de porcentaje
    percent_text = font.render(f"{int(value)}%", True, (0, 0, 0))
    text_rect = percent_text.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(percent_text, text_rect)


# --- Mini juego felicidad ---
def minijuego():
    # El minijuego se queda en pet.py por ahora, pero usaremos las dimensiones del config
    WIDTH_MJ, HEIGHT_MJ = WIDTH, HEIGHT
    window_mj = pygame.display.set_mode((WIDTH_MJ, HEIGHT_MJ))
    pygame.display.set_caption("Mini-juego: ¡Atrapá las zanahorias!")
    clock_mj = pygame.time.Clock()

    # Cargar imágenes
    # Tenga en cuenta: Estamos asumiendo que las rutas de imagen son correctas.
    fondo = pygame.image.load(ASSETS_DIR + "day_bg.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH_MJ, HEIGHT_MJ))
    conejo_img = pygame.image.load(ASSETS_DIR + "pet_idle.png").convert_alpha()
    conejo_img = pygame.transform.scale(conejo_img, (60, 60))
    zanahoria_img = pygame.image.load(ASSETS_DIR + "food_icon.png").convert_alpha()
    zanahoria_img = pygame.transform.scale(zanahoria_img, (30, 30))

    conejo = pygame.Rect(WIDTH_MJ // 2 - 30, HEIGHT_MJ - 60, 60, 60)
    zanahorias = []
    velocidad_zanahoria = 4
    velocidad_conejo = 6
    score = 0
    font_mj = pygame.font.SysFont("arial", 18, bold=True)

    # --- Pantalla de inicio ---
    mostrando_inicio = True
    while mostrando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                mostrando_inicio = False  # Empezar juego

        window_mj.blit(fondo, (0, 0))
        window_mj.blit(conejo_img, (conejo.x, conejo.y))
        titulo = font_mj.render("¡Atrapá las zanahorias!", True, (0, 0, 0))
        window_mj.blit(titulo, (60, 80))
        texto = font_mj.render("Presioná ENTER para empezar", True, (0, 0, 0))
        window_mj.blit(texto, (40, 120))
        pygame.display.flip()
        clock_mj.tick(30)

    # --- Bucle del minijuego ---
    tiempo_inicio = time.time()
    DURACION_JUEGO = 15
    running_mj = True

    while running_mj:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and conejo.x > 0:
            conejo.x -= velocidad_conejo
        if keys[pygame.K_RIGHT] and conejo.x < WIDTH_MJ - conejo.width:
            conejo.x += velocidad_conejo

        # Spawnear zanahorias
        if len(zanahorias) < 6 and random.random() < 0.03:
            zanahorias.append(pygame.Rect(random.randint(0, WIDTH_MJ - 20), 0, 20, 30))

        # Mover y detectar colisiones
        for z in zanahorias[:]:
            z.y += velocidad_zanahoria
            if z.colliderect(conejo):
                zanahorias.remove(z)
                score += 1
            elif z.y > HEIGHT_MJ:
                zanahorias.remove(z)

        # Dibujar fondo y objetos
        window_mj.blit(fondo, (0, 0))
        window_mj.blit(conejo_img, (conejo.x, conejo.y))
        for z in zanahorias:
            window_mj.blit(zanahoria_img, (z.x, z.y))

        # Texto de UI
        text = font_mj.render(f"Puntos: {score}", True, (0, 0, 0))
        window_mj.blit(text, (10, 10))
        restante = max(0, int(DURACION_JUEGO - (time.time() - tiempo_inicio)))
        timer_text = font_mj.render(f"Tiempo: {restante}", True, (0, 0, 0))
        window_mj.blit(timer_text, (WIDTH_MJ - 120, 10))

        pygame.display.flip()
        clock_mj.tick(30)

        if restante <= 0:
            running_mj = False

    # --- Pantalla final ---
    fin = True
    while fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = False
            if event.type == pygame.KEYDOWN:
                fin = False
        window_mj.blit(fondo, (0, 0))
        resultado = font_mj.render(f"¡Ganaste {score} puntos!", True, (0, 0, 0))
        window_mj.blit(resultado, (70, 130))
        volver = font_mj.render("Presioná cualquier tecla para volver", True, (0, 0, 0))
        window_mj.blit(volver, (25, 160))
        pygame.display.flip()
        clock_mj.tick(30)

    # Restaurar la pantalla principal después del minijuego
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mi Tamagotchi 🐰")

    return score
