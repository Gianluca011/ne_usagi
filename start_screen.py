import pygame
import os
from config import WIDTH, HEIGHT, ASSETS_DIR

from state_machine import State

class StartScreenState(State):
    def __init__(self):
        super().__init__()
        # Intentamos cargar la imagen de fondo y el logo
        self.bg_path = os.path.join(ASSETS_DIR, "start_bg.png")
        self.logo_path = os.path.join(ASSETS_DIR, "logo.png")
        
        if os.path.exists(self.bg_path):
            self.bg_img = pygame.image.load(self.bg_path).convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        else:
            self.bg_img = pygame.Surface((WIDTH, HEIGHT))
            self.bg_img.fill((255, 230, 240)) # Color rosa claro por defecto
            
        if os.path.exists(self.logo_path):
            self.logo_img = pygame.image.load(self.logo_path).convert_alpha()
            # Escalar el logo para que no ocupe toda la pantalla
            img_w, img_h = self.logo_img.get_size()
            max_w, max_h = 240, 120
            if img_w > max_w or img_h > max_h:
                scale = min(max_w / img_w, max_h / img_h)
                self.logo_img = pygame.transform.smoothscale(self.logo_img, (int(img_w * scale), int(img_h * scale)))
        else:
            # Placeholder text si no hay logo
            self.logo_img = None
            try:
                self.font_logo = pygame.font.SysFont("arial", 40, bold=True)
            except:
                self.font_logo = pygame.font.Font(None, 40)
            self.logo_text = self.font_logo.render("Ne Usagi", True, (255, 100, 150))
            
        try:
            self.font_text = pygame.font.SysFont("arial", 18, bold=True)
        except:
            self.font_text = pygame.font.Font(None, 18)
            
        # Para parpadeo del texto "Presione enter..."
        self.blink_timer = 0
        self.show_text = True
        
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_state = "MAIN"

    def update(self, dt: float) -> None:
        self.blink_timer += dt
        if self.blink_timer >= 0.5:
            self.show_text = not self.show_text
            self.blink_timer = 0
        
    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.bg_img, (0, 0))
        
        if self.logo_img:
            # Centramos la imagen original del logo en la parte superior
            rect = self.logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(self.logo_img, rect)
        else:
            rect = self.logo_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(self.logo_text, rect)
            
        if self.show_text:
            prompt = self.font_text.render("Presione ENTER para empezar", True, (50, 50, 50))
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            window.blit(prompt, prompt_rect)
