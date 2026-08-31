import pygame
from config import COLOR_BAR_BG, COLOR_BAR_BORDER, COLOR_HIGH, COLOR_MID, COLOR_LOW

pygame.font.init()
try:
    font = pygame.font.SysFont("arial", 14, bold=True)
except:
    font = pygame.font.Font(None, 14)

def get_bar_color(value: float) -> tuple[int, int, int]:
    if value >= 80:
        return COLOR_HIGH
    elif value >= 40:
        return COLOR_MID
    else:
        return COLOR_LOW

def draw_bar(surface: pygame.Surface, x: int, y: int, width: int, height: int, value: float, max_value: float) -> None:
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

def draw_warning(surface: pygame.Surface, x: int, y: int) -> None:
    """ Dibuja un ícono de advertencia (globo rojo) si la stat es crítica """
    pygame.draw.circle(surface, (255, 50, 50), (x, y), 10)
    pygame.draw.circle(surface, (255, 255, 255), (x, y), 10, 1)
    
    text = font.render("!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple[int, int, int], hover_color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        current_color = self.hover_color if self.is_hovered else self.color
        
        # Dibujar fondo y borde
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_BAR_BORDER, self.rect, 2, border_radius=5)

        # Dibujar texto
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Devuelve True si el botón fue clickeado"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
