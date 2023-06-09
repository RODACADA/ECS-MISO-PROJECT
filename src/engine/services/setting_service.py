import pygame
import json

class SettingService:
    def __init__(self):
        self._configs = {}

    def get(self, path:str) -> dict:
        if path not in self._configs:
            with open(path, encoding="utf-8") as file:
                self._configs[path] = json.load(file)
        return self._configs[path]