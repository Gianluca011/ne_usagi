import pygame
import time
from typing import List

from state_machine import State
from pet import Tamagotchi
from particles import Particle
from ui import draw_bar, draw_warning, Button
from config import HEIGHT, WIDTH, KEY_FEED, KEY_SLEEP, KEY_PLAY, KEY_SHOP

class MainState(State):
    def __init__(self, pet: Tamagotchi, day_bg: pygame.Surface, night_bg: pygame.Surface, icons: dict, sprites: dict):
        super().__init__()
        self.pet = pet
        self.day_bg = day_bg
        self.night_bg = night_bg
        self.icons = icons
        self.sprites = sprites
        self.particles: List[Particle] = []
        self.last_bg_check = 0
        self.current_bg = self.day_bg
        self._update_bg()
        
        btn_y = HEIGHT - 40
        btn_w = 60
        btn_h = 30
        margin = 10
        start_x = (WIDTH - (btn_w * 4 + margin * 3)) // 2

        self.btn_feed = Button(start_x, btn_y, btn_w, btn_h, "Comer", (200, 255, 200), (150, 255, 150))
        self.btn_sleep = Button(start_x + btn_w + margin, btn_y, btn_w, btn_h, "Dormir", (200, 200, 255), (150, 150, 255))
        self.btn_play = Button(start_x + 2*(btn_w + margin), btn_y, btn_w, btn_h, "Jugar", (255, 255, 200), (255, 255, 150))
        self.btn_shop = Button(start_x + 3*(btn_w + margin), btn_y, btn_w, btn_h, "Tienda", (255, 200, 200), (255, 150, 150))
        
    def _update_bg(self) -> None:
        now = time.time()
        if now - self.last_bg_check >= 10:
            hour = time.localtime().tm_hour
            self.current_bg = self.day_bg if 7 <= hour < 19 else self.night_bg
            self.last_bg_check = now

    def add_particle(self, text: str, color: tuple[int, int, int], y_offset: int = 110) -> None:
        from config import WIDTH
        self.particles.append(Particle(WIDTH // 2, y_offset, text, color))

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and not self.pet.durmiendo:
                if event.key == KEY_FEED:
                    self.next_state = "INVENTORY"
                elif event.key == KEY_SLEEP:
                    self.pet.dormir()
                elif event.key == KEY_PLAY:
                    self.next_state = "MINIGAME"
                elif event.key == KEY_SHOP:
                    self.next_state = "SHOP"
                    
            if not self.pet.durmiendo:
                if self.btn_feed.handle_event(event):
                    self.next_state = "INVENTORY"
                elif self.btn_sleep.handle_event(event):
                    self.pet.dormir()
                elif self.btn_play.handle_event(event):
                    self.next_state = "MINIGAME"
                elif self.btn_shop.handle_event(event):
                    self.next_state = "SHOP"

    def update(self, dt: float) -> None:
        self._update_bg()
        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.current_bg, (0, 0))

        # Barras e íconos y globos de warning
        window.blit(self.icons['food'], (20, 18))
        draw_bar(window, 50, 20, 200, 20, self.pet.hambre, 100)
        if self.pet.is_critical("hambre"): 
            draw_warning(window, 260, 30)

        window.blit(self.icons['energy'], (20, 50))
        draw_bar(window, 50, 52, 200, 20, self.pet.energia, 100)
        if self.pet.is_critical("energia"): 
            draw_warning(window, 260, 62)

        window.blit(self.icons['fun'], (20, 82))
        draw_bar(window, 50, 84, 200, 20, self.pet.felicidad, 100)
        if self.pet.is_critical("felicidad"): 
            draw_warning(window, 260, 94)

        # Sprite de la mascota
        if self.pet.durmiendo:
            window.blit(self.sprites['sleep'], (90, 120))
        elif self.pet.is_critical("hambre"):
            window.blit(self.sprites['hungry'], (90, 120))
        elif self.pet.is_critical("felicidad"):
            window.blit(self.sprites['sad'], (90, 120))
        else:
            window.blit(self.sprites['idle'], (90, 120))
            
        # Renderizar cosmético placeholder
        if self.pet.active_cosmetic:
            c_color = (200, 0, 0)
            c_rect = (140, 120, 20, 10) # default sombrero_yankii en cabeza
            if self.pet.active_cosmetic == "lentes":
                c_color = (50, 50, 50)
                c_rect = (130, 145, 40, 10) # centrado ojeras
            elif self.pet.active_cosmetic == "kimono":
                c_color = (0, 0, 200)
                c_rect = (120, 170, 60, 40) # cuerpo

            pygame.draw.rect(window, c_color, c_rect)

        # Textos de controles y monedas
        font_info = pygame.font.SysFont(None, 16)
        txt_info_coins = font_info.render(f"Z. Doradas: {self.pet.golden_carrots}", True, (255, 255, 255))
        window.blit(txt_info_coins, (WIDTH - txt_info_coins.get_width() - 10, 10))
        
        # Botones
        self.btn_feed.draw(window)
        self.btn_sleep.draw(window)
        self.btn_play.draw(window)
        self.btn_shop.draw(window)
        
        # Dibujar partículas
        for p in self.particles:
            p.draw(window)
