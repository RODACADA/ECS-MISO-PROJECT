import pygame


class CPowerDef:
    def __init__(self, position: pygame.Vector2, size: int, color: pygame.Color, font: str) -> None:
        self.pos = position
        self.size = size
        self.color = color
        self.font = font
