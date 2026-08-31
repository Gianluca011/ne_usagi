import time
import random
import os
import pygame

from config import WIDTH, HEIGHT, ASSETS_DIR

def load_img_or_dummy(name, size, dummy_color=(255,255,255)):
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

def play_sfx(name):
    # Función dummy / soporte temporal para reproducir sonidos
    path = os.path.join(ASSETS_DIR, name)
    if pygame.mixer.get_init() and os.path.exists(path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.play()
        except:
            pass

from state_machine import State
from pet import Tamagotchi

class MinigameState(State):
    def __init__(self, pet: Tamagotchi):
        super().__init__()
        self.pet = pet
        self.state = "START" # START, PLAY, END
        self.score = 0
        
        path_bg = os.path.join(ASSETS_DIR, "day_bg.png")
        if os.path.exists(path_bg):
            self.fondo = pygame.image.load(path_bg).convert()
            self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))
        else:
            self.fondo = pygame.Surface((WIDTH, HEIGHT))
            self.fondo.fill((135, 206, 235))

        self.conejo_img = load_img_or_dummy("pet_idle.png", (60, 60), (255, 255, 255))
        self.zanahoria_img = load_img_or_dummy("food_icon.png", (30, 30), (255, 165, 0))

        self.conejo = pygame.Rect(WIDTH // 2 - 30, HEIGHT - 60, 60, 60)
        self.zanahorias = []
        self.velocidad_zanahoria = 150 # px/s
        self.velocidad_conejo = 250 # px/s
        
        self.font_mj = pygame.font.SysFont("arial", 18, bold=True)
        self.tiempo_inicio = 0
        self.duracion_juego = 15
        
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        if self.state == "START":
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = "PLAY"
                    self.tiempo_inicio = time.time()
        elif self.state == "END":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.pet.jugar(self.score)
                    self.next_state = "MAIN"

    def update(self, dt: float) -> None:
        if self.state == "PLAY":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.conejo.x > 0:
                self.conejo.x -= self.velocidad_conejo * dt
            if keys[pygame.K_RIGHT] and self.conejo.x < WIDTH - self.conejo.width:
                self.conejo.x += self.velocidad_conejo * dt

            # Spawn probability per second
            if len(self.zanahorias) < 6 and random.random() < (1.5 * dt):
                self.zanahorias.append(pygame.Rect(random.randint(0, WIDTH - 20), 0, 20, 30))

            for z in self.zanahorias[:]:
                z.y += self.velocidad_zanahoria * dt
                if z.colliderect(self.conejo):
                    self.zanahorias.remove(z)
                    self.score += 1
                    play_sfx("catch_sfx.wav")
                elif z.y > HEIGHT:
                    self.zanahorias.remove(z)

            restante = max(0, int(self.duracion_juego - (time.time() - self.tiempo_inicio)))
            if restante <= 0:
                self.state = "END"

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.fondo, (0, 0))
        
        if self.state == "START":
            window.blit(self.conejo_img, (self.conejo.x, self.conejo.y))
            titulo = self.font_mj.render("¡Atrapá las zanahorias!", True, (0, 0, 0))
            window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 80))
            texto = self.font_mj.render("Presioná ENTER para empezar", True, (0, 0, 0))
            window.blit(texto, (WIDTH // 2 - texto.get_width() // 2, 120))
            
        elif self.state == "PLAY":
            window.blit(self.conejo_img, (self.conejo.x, self.conejo.y))
            for z in self.zanahorias:
                window.blit(self.zanahoria_img, (z.x, z.y))

            text = self.font_mj.render(f"Puntos: {self.score}", True, (0, 0, 0))
            window.blit(text, (10, 10))
            restante = max(0, int(self.duracion_juego - (time.time() - self.tiempo_inicio)))
            timer_text = self.font_mj.render(f"Tiempo: {restante}", True, (0, 0, 0))
            window.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))
            
        elif self.state == "END":
            resultado = self.font_mj.render(f"¡Atrapaste {self.score}! (+ {self.score} ZD)", True, (0, 0, 0))
            window.blit(resultado, (WIDTH // 2 - resultado.get_width() // 2, 130))
            volver = self.font_mj.render("Presioná una tecla para volver", True, (0, 0, 0))
            window.blit(volver, (WIDTH // 2 - volver.get_width() // 2, 160))
