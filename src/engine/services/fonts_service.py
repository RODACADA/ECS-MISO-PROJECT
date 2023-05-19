import pygame
from utils import resource_path


class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path: str, size: int) -> pygame.font.FontType:
        if path not in self._fonts:
            self._fonts[(path,size)] = pygame.font.Font(resource_path(path), size)
        return self._fonts[(path,size)]
    
    
