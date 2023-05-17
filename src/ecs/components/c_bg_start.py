import pygame
import random


""" class CBGStar:
    def __init__(self, color: pygame.Color, velocity: float, position: pygame.Vector2, blink_time) -> None:
        self.color = color
        self.velocity = velocity
        self.position = position
        self.blink_time = blink_time

        self.elapsed_time = random.randrange(0, blink_time*100//1)/100
        self.blink = random.choice([True, False]) """

class CBGStar:
    def __init__(self, color: pygame.Color, velocity: float, position: pygame.Vector2, blink_time) -> None:
        self.color = color
        self.velocity = velocity
        self.position = position
        self.blink_time = blink_time

        self.elapsed_time = random.randrange(0, blink_time*100//1)/100
        self.blink = random.choice([True, False])
        
        # Crear la superficie y el rectángulo
        self.surface = pygame.Surface((1, 1))  # cambiar el tamaño si es necesario
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(topleft=self.position)
