# 🐰 Ne Usagi (ねウサギ) — Virtual Pet Tamagotchi

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Fase%202%20(Refactor)-orange?style=for-the-badge)](#-roadmap--fase-2)

**Ne Usagi** es una mascota virtual estilo retro y *pixel-art* desarrollada en **Python** con **Pygame**. Inspirada en los clásicos Tamagotchis y en la estética *kawaii* japonesa, permite cuidar, alimentar, personalizar y jugar con un tierno conejito que reacciona en tiempo real a tus cuidados y a la hora del día.

---

## 🌟 Características principales

- 🐾 **Simulación de mascota en tiempo real**
  - Sistema de 3 estadísticas vitales: **Hambre**, **Energía** y **Felicidad** (0–100 %).
  - Decaimiento dinámico con alertas visuales de estado crítico (`!`).
  - Expresiones y sprites contextuales: *Idle* (normal/feliz), *Hungry* (hambriento), *Sad* (triste) y *Sleep* (durmiendo).
- ☀️🌙 **Ciclo día / noche dinámico**
  - El entorno cambia automáticamente entre día y noche evaluando la hora real del sistema operativo.
- 🎮 **Minijuego integrado ("Atrapa las Zanahorias")**
  - Esquiva y atrapa zanahorias que caen para subir la felicidad de tu mascota y ganar dinero.
- 🪙 **Economía y tienda ("Tienda Yankii ⛩️")**
  - Obtén **Zanahorias Doradas (ZD)** superando el minijuego.
  - Compra consumibles (*Agua Fresca*, *Zanahoria Rica*, *Pastel de Fresa*).
  - Compra y equipa cosméticos inspirados en la cultura japonesa (*Gorro Yankii*, *Lentes Cool*, *Kimono Clásico*).
- 🎒 **Mochila e inventario**
  - Menú interactivo para gestionar y usar alimentos cuando tu mascota lo necesite.
- 💾 **Persistencia automática**
  - Guarda automáticamente el estado, monedas, consumibles y cosméticos en `data/save.json`.
- 🏗️ **Arquitectura modular (State Machine + POO)**
  - Máquina de estados desacoplada (`START_SCREEN`, `MAIN`, `INVENTORY`, `SHOP`, `MINIGAME`).
  - Soporte híbrido para interactuar mediante **teclado y mouse** (con botones UI y efectos *hover*).
  - Sistema de partículas flotantes para retroalimentación visual al alimentar.

---

## 🚀 Instalación

### Requisitos previos

- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Pasos

```bash
# 1. Cloná el repositorio
git clone https://github.com/Gianluca011/ne_usagi.git
cd ne_usagi

# 2. (Opcional pero recomendado) Creá un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalá las dependencias
pip install pygame

# 4. Ejecutá el juego
python game.py
```

---

## 🎮 Controles

| Tecla | Acción |
| :---: | --- |
| `Espacio` | Alimentar a la mascota |
| `E` | Dormir |
| `J` | Jugar al minijuego (Atrapa las Zanahorias) |
| `S` | Abrir la tienda |
| `Mouse` | Navegar menús, inventario y tienda mediante botones interactivos |

---

## 📁 Estructura del proyecto

```
ne_usagi/
├── assets/                 # Sprites, íconos y recursos gráficos
├── config.py                # Configuración global (pantalla, rutas, teclas, colores)
├── game.py                  # Punto de entrada y bucle principal del juego
├── state_machine.py         # Máquina de estados (START_SCREEN, MAIN, SHOP, etc.)
├── main_state.py            # Lógica del estado principal (mascota + estadísticas)
├── pet.py                   # Lógica y comportamiento de la mascota
├── minigames.py              # Minijuego "Atrapa las Zanahorias"
├── shop.py                   # Sistema de tienda y compras
├── inventory_screen.py       # Pantalla de mochila / inventario
├── start_screen.py           # Pantalla de inicio
├── particles.py               # Sistema de partículas visuales
├── ui.py                      # Componentes reutilizables de interfaz
└── PRD_ Ne Usagi - Fase 2.md  # Documento de requisitos del proyecto
```

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia **MIT**. Consultá el archivo `LICENSE` para más detalles.

---

Si te gustó el proyecto, ¡dejá una ⭐ en el repositorio!
