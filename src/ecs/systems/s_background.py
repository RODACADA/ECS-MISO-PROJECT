import esper
import pygame

from src.create.prefab_creator import create_star

from src.ecs.components.c_bg_star_spawner import CBgStarSpawner
from src.ecs.components.c_bg_start import CBGStar
import random


def system_background(world: esper.World, delta_time: float, screen: pygame.Surface):
    _, spawner = world.get_component(CBgStarSpawner)[0]
    spawner.elapsed_time += delta_time

    if spawner.elapsed_time > spawner.spawn_time:
        create_star(world, spawner, screen)
        spawner.elapsed_time -= spawner.spawn_time
        spawner.spawn_time = random.randrange(
            spawner.min_spawn_time*100//1, spawner.max_spawn_time*100//1 + 1)/100

    star_components = world.get_component(CBGStar)

    for start_entity, star in star_components:
        star.elapsed_time += delta_time

        if star.elapsed_time > star.blink_time:
            star.blink = not star.blink
            star.elapsed_time -= star.blink_time

        star.position.y += star.velocity * delta_time

        if star.position.y > screen.get_height():
            world.delete_entity(start_entity)
        elif star.blink:
            surface = pygame.Surface(pygame.Vector2(1, 1))
            surface.fill(star.color)
            screen.blit(surface, star.position)
