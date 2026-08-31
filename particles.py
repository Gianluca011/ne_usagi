import pygame

class Particle:
    def __init__(self, x: int, y: int, text: str, color: tuple[int, int, int]):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color
        self.life = 1.5
        self.max_life = 1.5
        try:
            self.font = pygame.font.SysFont("arial", 14, bold=True)
        except:
            self.font = pygame.font.Font(None, 14)
            
    def update(self, dt: float) -> None:
        self.y -= 30 * dt
        self.life -= dt
        
    def draw(self, window: pygame.Surface) -> None:
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            surf = self.font.render(self.text, True, self.color)
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(int(self.x), int(self.y)))
            window.blit(surf, rect)
