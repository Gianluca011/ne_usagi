import pygame
from config import WIDTH, HEIGHT

from state_machine import State
from pet import Tamagotchi
from ui import Button

class InventoryState(State):
    def __init__(self, pet: Tamagotchi):
        super().__init__()
        self.pet = pet
        self.consumables_info = {
            "agua": {"name": "Agua Fresca", "color": (100, 150, 255), "stats": {"hambre": 10}},
            "zanahoria": {"name": "Zanahoria Rica", "color": (255, 150, 0), "stats": {"hambre": 20}},
            "pastel": {"name": "Pastel de Fresa", "color": (255, 100, 200), "stats": {"hambre": 40, "felicidad": 10}},
        }
        
        self.items_list = []
        self._refresh_list()
                
        self.selected_index = 0

        try:
            self.font_title = pygame.font.SysFont("arial", 22, bold=True)
            self.font_item = pygame.font.SysFont("arial", 16)
            self.font_info = pygame.font.SysFont("arial", 12)
        except:
            self.font_title = pygame.font.Font(None, 24)
            self.font_item = pygame.font.Font(None, 18)
            self.font_info = pygame.font.Font(None, 14)
            
        self.particles_to_spawn = []
        self.btn_exit = Button(WIDTH//2 - 40, HEIGHT - 35, 80, 25, "Salir", (200, 100, 100), (255, 100, 100))
        
    def _refresh_list(self):
        self.items_list = []
        for c_id, qty in self.pet.consumables.items():
            if qty > 0 and c_id in self.consumables_info:
                item_data = self.consumables_info[c_id].copy()
                item_data["id"] = c_id
                self.items_list.append(item_data)
    
    def _use_item(self) -> None:
        if len(self.items_list) == 0: return
        item = self.items_list[self.selected_index]
        c_id = item["id"]
        
        if self.pet.alimentar_item(c_id, item["stats"]):
            # Agregar partículas a generar
            for stat, val in item["stats"].items():
                color = (0, 255, 0) if stat == "hambre" else (0, 0, 255)
                self.particles_to_spawn.append({"text": f"+{val} {stat.capitalize()}", "color": color})
                
            # Salir automáticamente del menú al comer
            self.next_state = "MAIN"

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.particles_to_spawn = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.next_state = "MAIN"
                    return
                elif len(self.items_list) > 0:
                    if event.key == pygame.K_UP:
                        self.selected_index = max(0, self.selected_index - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = min(len(self.items_list) - 1, self.selected_index + 1)
                    elif event.key == pygame.K_RETURN:
                        self._use_item()
                        return
                        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_exit.handle_event(event):
                    self.next_state = "MAIN"
                    return
                elif len(self.items_list) > 0:
                    mouse_y = event.pos[1]
                    if 50 <= mouse_y < 50 + len(self.items_list) * 30:
                        index = (mouse_y - 50) // 30
                        self.selected_index = index
                        self._use_item()
                        return

    def draw(self, window: pygame.Surface) -> None:
        window.fill((210, 240, 210)) # Fondo verde claro

        title = self.font_title.render("Mochila 🎒", True, (0, 0, 0))
        window.blit(title, (WIDTH//2 - title.get_width()//2, 10))

        if len(self.items_list) == 0:
            empty = self.font_item.render("Mochila vacía. ¡Compra comida!", True, (100, 100, 100))
            window.blit(empty, (WIDTH//2 - empty.get_width()//2, HEIGHT//2))
        else:
            y_offset = 50
            for i, item in enumerate(self.items_list):
                color = (0, 0, 0)
                if i == self.selected_index:
                    color = (0, 150, 50)
                
                qty = self.pet.consumables.get(item["id"], 0)
                text = self.font_item.render(f"{item['name']} (x{qty})", True, color)
                window.blit(text, (35, y_offset))
                pygame.draw.rect(window, item["color"], (10, y_offset+2, 14, 14))
                
                # Mouse hover highlight effect
                mouse_pos = pygame.mouse.get_pos()
                if 50 <= mouse_pos[1] < 50 + len(self.items_list) * 30:
                    hover_idx = (mouse_pos[1] - 50) // 30
                    if hover_idx == i:
                        pygame.draw.rect(window, (255, 255, 255), (5, y_offset, WIDTH-10, 28), 1)

                y_offset += 30

        self.btn_exit.draw(window)
