import pygame
from typing import Optional, Dict

class State:
    """Clase base para todos los estados del juego."""
    def __init__(self):
        self.next_state: Optional[str] = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, window: pygame.Surface) -> None:
        pass

class StateMachine:
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        self.current_state_name: Optional[str] = None

    def add_state(self, name: str, state: State) -> None:
        self.states[name] = state

    def change_state(self, name: str) -> None:
        if name in self.states:
            self.current_state_name = name
            self.current_state = self.states[name]
            self.current_state.next_state = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        if self.current_state:
            self.current_state.handle_events(events)
            
            # Verificar si el estado actual solicitó una transición
            if self.current_state.next_state:
                self.change_state(self.current_state.next_state)

    def update(self, dt: float) -> None:
        if self.current_state:
            self.current_state.update(dt)

    def draw(self, window: pygame.Surface) -> None:
        if self.current_state:
            self.current_state.draw(window)
