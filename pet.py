import json
import os
import time
from config import SAVE_PATH, DURACION_SUENO


class Tamagotchi:
    def __init__(self):
        self.hambre = 100
        self.energia = 100
        self.felicidad = 100
        self.golden_carrots = 0
        self.inventory = []
        self.consumables = {"agua": 0, "zanahoria": 0, "pastel": 0}
        self.active_cosmetic = None
        self.ultimo_tiempo = time.time()
        self.durmiendo = False
        self.inicio_sueno = 0
        self.load_data()

    def load_data(self) -> None:
        default_data = {
            "hambre": 100,
            "energia": 100,
            "felicidad": 100,
            "golden_carrots": 0,
            "inventory": [],
            "consumables": {"agua": 0, "zanahoria": 0, "pastel": 0},
            "active_cosmetic": None,
            "ultimo_tiempo": time.time(),
        }
        if os.path.exists(SAVE_PATH):
            try:
                with open(SAVE_PATH, "r") as f:
                    data = json.load(f)
                for key, value in default_data.items():
                    if key not in data:
                        data[key] = value
            except Exception:
                data = default_data
        else:
            data = default_data

        self.hambre = data["hambre"]
        self.energia = data["energia"]
        self.felicidad = data["felicidad"]
        self.golden_carrots = data.get("golden_carrots", 0)
        self.inventory = data.get("inventory", [])
        self.consumables = data.get("consumables", {"agua": 0, "zanahoria": 0, "pastel": 0})
        self.active_cosmetic = data.get("active_cosmetic", None)
        self.ultimo_tiempo = data["ultimo_tiempo"]

    def save_data(self) -> None:
        data = {
            "hambre": self.hambre,
            "energia": self.energia,
            "felicidad": self.felicidad,
            "golden_carrots": self.golden_carrots,
            "inventory": self.inventory,
            "consumables": self.consumables,
            "active_cosmetic": self.active_cosmetic,
            "ultimo_tiempo": self.ultimo_tiempo,
        }
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f)

    def alimentar(self) -> None:
        self.hambre = min(100, self.hambre + 20)

    def alimentar_item(self, item_id: str, stats: dict) -> bool:
        if self.consumables.get(item_id, 0) > 0:
            self.consumables[item_id] -= 1
            if "hambre" in stats:
                self.hambre = min(100, self.hambre + stats["hambre"])
            if "energia" in stats:
                self.energia = min(100, self.energia + stats["energia"])
            if "felicidad" in stats:
                self.felicidad = min(100, self.felicidad + stats["felicidad"])
            return True
        return False

    def dormir(self) -> None:
        if not self.durmiendo:
            self.durmiendo = True
            self.inicio_sueno = time.time()

    def jugar(self, score: int) -> None:
        if score > 0:
            aumento = min(100, score * 2)
            self.felicidad = min(100, self.felicidad + aumento)
            self.golden_carrots += score

    def update(self) -> None:
        now = time.time()
        if self.durmiendo:
            if now - self.inicio_sueno >= DURACION_SUENO:
                self.durmiendo = False
                self.energia = min(100, self.energia + 25)
        else:
            if self.energia <= 0:
                self.dormir()
            else:
                elapsed = now - self.ultimo_tiempo
                if elapsed > 10:
                    self.hambre = max(0, self.hambre - 5)
                    self.energia = max(0, self.energia - 3)
                    self.felicidad = max(0, self.felicidad - 2)
                    self.ultimo_tiempo = now

    def is_critical(self, stat: str) -> bool:
        if stat == "hambre":
            return self.hambre < 40
        if stat == "energia":
            return self.energia < 40
        if stat == "felicidad":
            return self.felicidad < 30
        return False
