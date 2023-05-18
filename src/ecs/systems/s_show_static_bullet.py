
from typing import List
import esper
from src.ecs.components.c_surface import CSurface


def system_show_static_bullet(world: esper.World, c_s: CSurface, is_player_dead: List[bool]):
    if is_player_dead[0]:
        c_s.show = False
