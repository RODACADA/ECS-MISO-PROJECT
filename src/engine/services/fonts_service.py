import pygame


class FontsService:
    def __init__(self):
        self._fonts = {}

    def get(self, path: str, size: int) -> pygame.font.FontType:
        if path not in self._fonts:
            self._fonts[path] = pygame.font.Font(path, size)
        return self._fonts[path]
