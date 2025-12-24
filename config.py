# config.py

import pygame

# --- Dimensiones y Configuración de Pantalla ---
WIDTH, HEIGHT = 300, 300
CAPTION = "Mi Tamagotchi 🐰"
FPS = 30

# --- Rutas y Guardado ---
SAVE_PATH = "data/save.json"
ASSETS_DIR = "assets/"

# --- Configuración de la Mascota ---
PET_SIZE = (120, 120)
DURACION_SUENO = 5  # Segundos que dura el sueño

# --- Teclas de Interacción ---
KEY_FEED = pygame.K_SPACE  # Espacio para alimentar
KEY_SLEEP = pygame.K_e  # E para dormir
KEY_PLAY = pygame.K_j  # J para jugar

# --- Colores de las Barras (Basados en get_bar_color) ---
COLOR_HIGH = (100, 220, 100)  # > 80%
COLOR_MID = (255, 210, 80)  # >= 40%
COLOR_LOW = (255, 100, 100)  # < 40%
COLOR_BAR_BG = (200, 200, 200)
COLOR_BAR_BORDER = (50, 50, 50)
