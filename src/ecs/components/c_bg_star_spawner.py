import pygame
import random


class CBgStarSpawner:
    def __init__(self, bg_cfg: dict) -> None:
        self.min_spawn_time = bg_cfg["min_spawn_time"]
        self.max_spawn_time = bg_cfg["max_spawn_time"]
        self.min_blink_time = bg_cfg["min_blink_time"]
        self.max_blink_time = bg_cfg["max_blink_time"]
        self.min_vel = bg_cfg["min_velocity"]
        self.max_vel = bg_cfg["max_velocity"]
        self.colors = list()

        for color in bg_cfg["colors"]:
            self.colors.append(pygame.Color(
                color["r"], color["g"], color["b"]))

        self.elapsed_time = 0
        self.spawn_time = random.randrange(
            self.min_spawn_time*100//1, self.max_spawn_time*100//1 + 1)/100
