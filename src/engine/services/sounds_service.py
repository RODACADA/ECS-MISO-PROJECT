import pygame
from utils import resource_path


class SoundsService:
    def __init__(self) -> None:
        self._sounds = {}

    def play(self, path: str) -> None:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(resource_path(path))

        self._sounds[path].play()
