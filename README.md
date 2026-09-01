# 🐰 Ne Usagi (ねウサギ) — Virtual Pet Tamagotchi

[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Fase%202%20(Refactored)-orange?style=for-the-badge)]()

**Ne Usagi** es una mascota virtual estilo retro y *pixel-art* desarrollada en **Python** con **Pygame**. Inspirada en los clásicos Tamagotchis y en la estética *kawaii* japonesa, permite cuidar, alimentar, personalizar y jugar con un tierno conejito que reacciona en tiempo real a tus cuidados y a la hora del día.

---

## 🌟 Características Principales

- 🐾 **Simulación de Mascota en Tiempo Real:**
  - Sistema de 3 estadísticas vitales: **Hambre**, **Energía** y **Felicidad** (0 - 100%).
  - Decaimiento dinámico con alertas visuales de estado crítico (`!`).
  - Expresiones y sprites contextuales: *Idle* (normal/feliz), *Hungry* (hambriento), *Sad* (triste) y *Sleep* (durmiendo).
- ☀️🌙 **Ciclo Día / Noche Dinámico:**
  - El entorno cambia automáticamente entre día y noche evaluando la hora real del sistema operativo.
- 🎮 **Minijuego Integrado ("Atrapa las Zanahorias"):**
  - Esquiva y atrapa zanahorias que caen para subir la felicidad de tu mascota y ganar dinero.
- 🪙 **Economía & Tienda ("Tienda Yankii ⛩️"):**
  - Obtén **Zanahorias Doradas (ZD)** superando el minijuego.
  - Compra consumibles (*Agua Fresca*, *Zanahoria Rica*, *Pastel de Fresa*).
  - Compra y equipa cosméticos inspirados en la cultura japonesa (*Gorro Yankii*, *Lentes Cool*, *Kimono Clásico*).
- 🎒 **Mochila e Inventario:**
  - Menú interactivo para gestionar y usar alimentos cuando tu mascota lo necesite.
- 💾 **Persistencia Automática:**
  - Guarda automáticamente el estado, monedas, consumibles y cosméticos en `data/save.json`.
- 🏗️ **Arquitectura Modular (State Machine + POO):**
  - Máquina de estados desacoplada (`START_SCREEN`, `MAIN`, `INVENTORY`, `SHOP`, `MINIGAME`).
  - Soporte híbrido para interactuar mediante **teclado y mouse** (con botones UI y efectos *hover*).
  - Sistema de partículas flotantes para retroalimentación visual al alimentar.
