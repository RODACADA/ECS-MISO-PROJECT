

import pygame
import esper
from src.ecs.components.c_surface import CSurface


def system_delete_start_text(world: esper.World, start_time: int, entity_id: int):
    surface = world.component_for_entity(entity_id, CSurface)
    if pygame.time.get_ticks() >= start_time + 2000:
        surface.show = False
