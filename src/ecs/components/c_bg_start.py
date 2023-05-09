import pygame
import random


class CBGStar:
    def __init__(self, color: pygame.Color, velocity: float, position: pygame.Vector2, blink_time) -> None:
        self.color = color
        self.velocity = velocity
        self.position = position
        self.blink_time = blink_time

        self.elapsed_time = random.randrange(0, blink_time*100//1)/100
        self.blink = random.choice([True, False])
