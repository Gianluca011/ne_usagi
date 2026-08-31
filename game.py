import pygame
import time
import os

from pet import Tamagotchi
from minigames import MinigameState, play_sfx
from shop import ShopState
from start_screen import StartScreenState
from inventory_screen import InventoryState
from main_state import MainState
from state_machine import StateMachine

from config import (
    WIDTH,
    HEIGHT,
    CAPTION,
    PET_SIZE,
    FPS,
    ASSETS_DIR,
    KEY_FEED,
    KEY_SLEEP,
    KEY_PLAY,
    KEY_SHOP,
)

pygame.init()
if pygame.mixer.get_init() is None:
    pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

# Instanciamos la mascota principal (clase)
pet = Tamagotchi()

# --- Carga de Assets ---
def load_img_or_dummy(name, size, dummy_color=(255, 255, 255)):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            pass
    s = pygame.Surface(size)
    s.fill(dummy_color)
    return s

idle_img = load_img_or_dummy("pet_idle.png", PET_SIZE)
hungry_img = load_img_or_dummy("pet_hungry.png", PET_SIZE, (255, 200, 200))
sleep_img = load_img_or_dummy("pet_sleep.png", PET_SIZE, (200, 200, 255))
sad_img = load_img_or_dummy("pet_sad.png", PET_SIZE, (100, 100, 200))

icon_size = (24, 24)
food_icon = load_img_or_dummy("food_icon.png", icon_size, (255, 100, 100))
energy_icon = load_img_or_dummy("energy_icon.png", icon_size, (100, 255, 100))
fun_icon = load_img_or_dummy("fun_icon.png", icon_size, (100, 100, 255))

day_bg = load_img_or_dummy("day_bg.png", (WIDTH, HEIGHT), (135, 206, 235))
night_bg = load_img_or_dummy("night_bg.png", (WIDTH, HEIGHT), (25, 25, 112))

# --- Música Lo-Fi ---
music_path = os.path.join(ASSETS_DIR, "lofi.mp3")
if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # Loop infinito
    except:
        pass

# Partículas están ahora manejadas por MainState y la nueva clase Particle

# --- Inicialización de la Máquina de Estados ---
sm = StateMachine()

icons = {
    'food': food_icon,
    'energy': energy_icon,
    'fun': fun_icon
}
sprites = {
    'idle': idle_img,
    'hungry': hungry_img,
    'sleep': sleep_img,
    'sad': sad_img
}

main_state = MainState(pet, day_bg, night_bg, icons, sprites)
sm.add_state("START_SCREEN", StartScreenState())
sm.add_state("MAIN", main_state)
sm.add_state("INVENTORY", InventoryState(pet))
sm.add_state("SHOP", ShopState(pet))
sm.add_state("MINIGAME", MinigameState(pet))

sm.change_state("START_SCREEN")

# --- Bucle Principal ---
clock = pygame.time.Clock()
running = True

last_bg_check = 0
current_bg = day_bg

current_state = "START_SCREEN"
shop_state = None
minigame_state = None
inventory_state = None
start_screen_state = StartScreenState()
particles = []

while running:
    dt = clock.tick(FPS) / 1000.0
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pet.save_data()
            running = False

    if not running:
        break

    # Actualizar IA (caída de stats, etc.)
    # Se llama independientemente del estado para que el tiempo siga corriendo
    pet.update()

    # Si hay que agregar partículas cuando vuelve del inventario o minijuego, lo manejamos.
    # En la implementación actual de MinigameState/InventoryState no están pasando partículas, 
    # pero podemos recuperarlas si fuera necesario más adelante conectando estados o 
    # dejando que cada estado genere sus partículas temporalmente.
    
    sm.handle_events(events)
    sm.update(dt)
    sm.draw(window)

    pygame.display.flip()

pygame.quit()
