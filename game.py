import pygame
import time

# Importamos lógica y configuración
from pet import load_data, save_data, minijuego, draw_bar
from config import (
    WIDTH,
    HEIGHT,
    CAPTION,
    PET_SIZE,
    DURACION_SUENO,
    FPS,
    ASSETS_DIR,
    KEY_FEED,
    KEY_SLEEP,
    KEY_PLAY,
)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

# --- Estado de la mascota ---
pet = load_data()
durmiendo = False
inicio_sueno = 0

# --- Carga de Assets ---

# Sprites
idle_img = pygame.image.load(ASSETS_DIR + "pet_idle.png").convert_alpha()
idle_img = pygame.transform.scale(idle_img, PET_SIZE)

hungry_img = pygame.image.load(ASSETS_DIR + "pet_hungry.png").convert_alpha()
hungry_img = pygame.transform.scale(hungry_img, PET_SIZE)

sleep_img = pygame.image.load(ASSETS_DIR + "pet_sleep.png").convert_alpha()
sleep_img = pygame.transform.scale(sleep_img, PET_SIZE)

sad_img = pygame.image.load(ASSETS_DIR + "pet_sad.png").convert_alpha()
sad_img = pygame.transform.scale(sad_img, PET_SIZE)

# Íconos
icon_size = (24, 24)
food_icon = pygame.image.load(ASSETS_DIR + "food_icon.png").convert_alpha()
food_icon = pygame.transform.scale(food_icon, icon_size)

energy_icon = pygame.image.load(ASSETS_DIR + "energy_icon.png").convert_alpha()
energy_icon = pygame.transform.scale(energy_icon, icon_size)

fun_icon = pygame.image.load(ASSETS_DIR + "fun_icon.png").convert_alpha()
fun_icon = pygame.transform.scale(fun_icon, icon_size)

# Fondo dinámico día/noche
day_bg = pygame.image.load(ASSETS_DIR + "day_bg.png").convert()
day_bg = pygame.transform.scale(day_bg, (WIDTH, HEIGHT))
night_bg = pygame.image.load(ASSETS_DIR + "night_bg.png").convert()
night_bg = pygame.transform.scale(night_bg, (WIDTH, HEIGHT))


# --- Bucle principal ---
clock = pygame.time.Clock()
running = True

while running:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data(pet)
            running = False
        elif event.type == pygame.KEYDOWN and not durmiendo:
            if event.key == KEY_FEED:
                pet["hambre"] = min(100, pet["hambre"] + 20)
            elif event.key == KEY_SLEEP:
                durmiendo = True
                inicio_sueno = now
            elif event.key == KEY_PLAY:
                puntos = minijuego()
                if puntos > 0:
                    aumento = min(100, puntos * 2)
                    pet["felicidad"] = min(100, pet["felicidad"] + aumento)

    # Sueño automático
    if not durmiendo and pet["energia"] <= 0:
        durmiendo = True
        inicio_sueno = now

    if durmiendo:
        if now - inicio_sueno >= DURACION_SUENO:
            durmiendo = False
            pet["energia"] = min(100, pet["energia"] + 25)
    else:
        elapsed = now - pet["ultimo_tiempo"]
        if elapsed > 10:
            pet["hambre"] = max(0, pet["hambre"] - 5)
            pet["energia"] = max(0, pet["energia"] - 3)
            pet["felicidad"] = max(0, pet["felicidad"] - 2)
            pet["ultimo_tiempo"] = now

    # Fondo día/noche
    hour = time.localtime().tm_hour
    bg = day_bg if 7 <= hour < 19 else night_bg
    window.blit(bg, (0, 0))

    # Dibujar barras (usando la función importada)
    window.blit(food_icon, (20, 18))
    draw_bar(window, 50, 20, 200, 20, pet["hambre"], 100)

    window.blit(energy_icon, (20, 50))
    draw_bar(window, 50, 52, 200, 20, pet["energia"], 100)

    window.blit(fun_icon, (20, 82))
    draw_bar(window, 50, 84, 200, 20, pet["felicidad"], 100)

    # Sprite de la mascota
    if durmiendo:
        window.blit(sleep_img, (90, 120))
    elif pet["hambre"] < 40:
        window.blit(hungry_img, (90, 120))
    elif pet["felicidad"] < 30:
        window.blit(sad_img, (90, 120))
    else:
        window.blit(idle_img, (90, 120))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
