import pygame
from config import WIDTH, HEIGHT

from state_machine import State
from pet import Tamagotchi
from ui import Button

class ShopState(State):
    def __init__(self, pet: Tamagotchi):
        super().__init__()
        self.pet = pet
        self.items = [
            {"id": "agua", "name": "Agua Fresca", "price": 2, "color": (100, 150, 255), "type": "consumable"},
            {"id": "zanahoria", "name": "Zanahoria Rica", "price": 5, "color": (255, 150, 0), "type": "consumable"},
            {"id": "pastel", "name": "Pastel de Fresa", "price": 15, "color": (255, 100, 200), "type": "consumable"},
            {"id": "sombrero_yankii", "name": "Gorro Yankii", "price": 10, "color": (200, 0, 0), "type": "cosmetic"},
            {"id": "lentes", "name": "Lentes Cool", "price": 15, "color": (50, 50, 50), "type": "cosmetic"},
            {"id": "kimono", "name": "Kimono Clásico", "price": 30, "color": (0, 0, 200), "type": "cosmetic"},
        ]
        self.selected_index = 0

        try:
            self.font_title = pygame.font.SysFont("arial", 22, bold=True)
            self.font_item = pygame.font.SysFont("arial", 16)
            self.font_info = pygame.font.SysFont("arial", 12)
        except:
            self.font_title = pygame.font.Font(None, 24)
            self.font_item = pygame.font.Font(None, 18)
            self.font_info = pygame.font.Font(None, 14)
            
        self.btn_exit = Button(WIDTH//2 - 40, HEIGHT - 30, 80, 25, "Salir", (200, 100, 100), (255, 100, 100))

    def _buy_item(self) -> None:
        item = self.items[self.selected_index]
        if item.get("type", "cosmetic") == "cosmetic":
            if item["id"] in self.pet.inventory:
                if self.pet.active_cosmetic == item["id"]:
                    self.pet.active_cosmetic = None # Desequipar
                else:
                    self.pet.active_cosmetic = item["id"]
            else:
                if self.pet.golden_carrots >= item["price"]:
                    self.pet.golden_carrots -= item["price"]
                    self.pet.inventory.append(item["id"])
                    self.pet.active_cosmetic = item["id"]
        else: # Consumable
            if self.pet.golden_carrots >= item["price"]:
                self.pet.golden_carrots -= item["price"]
                self.pet.consumables[item["id"]] = self.pet.consumables.get(item["id"], 0) + 1
    
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                    self.next_state = "MAIN"
                    return
                elif event.key == pygame.K_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    self._buy_item()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_exit.handle_event(event):
                    self.next_state = "MAIN"
                    return
                
                mouse_y = event.pos[1]
                if 70 <= mouse_y < 70 + len(self.items) * 25:
                    self.selected_index = (mouse_y - 70) // 25
                    self._buy_item()

    def draw(self, window: pygame.Surface) -> None:
        window.fill((240, 230, 210)) # Fondo color pergamino claro

        title = self.font_title.render("Tienda Yankii ⛩️", True, (0, 0, 0))
        window.blit(title, (WIDTH//2 - title.get_width()//2, 10))

        money = self.font_item.render(f"Zanahorias Doradas: {self.pet.golden_carrots}", True, (200, 100, 0))
        window.blit(money, (20, 40))

        y_offset = 70
        for i, item in enumerate(self.items):
            color = (0, 0, 0)
            if i == self.selected_index:
                color = (0, 150, 50) # Resaltado verde
            
            if item.get("type", "cosmetic") == "cosmetic":
                if self.pet.active_cosmetic == item["id"]:
                    status = "[EQUIPADO]"
                elif item["id"] in self.pet.inventory:
                    status = "[COMPRADO]"
                else:
                    status = f"[{item['price']} ZD]"
            else:
                qty = self.pet.consumables.get(item["id"], 0)
                status = f"[{item['price']} ZD] (Tienes: {qty})"
            
            text = self.font_item.render(f"{item['name']} {status}", True, color)
            window.blit(text, (35, y_offset))
            # Placeholder visual del cosmético/consumible (cuadrado)
            pygame.draw.rect(window, item["color"], (10, y_offset+2, 14, 14))
            
            # Mouse hover highlight effect
            mouse_pos = pygame.mouse.get_pos()
            if 70 <= mouse_pos[1] < 70 + len(self.items) * 25:
                hover_idx = (mouse_pos[1] - 70) // 25
                if hover_idx == i:
                    pygame.draw.rect(window, (255, 255, 255), (5, y_offset, WIDTH-10, 23), 1)

            y_offset += 25

        self.btn_exit.draw(window)
