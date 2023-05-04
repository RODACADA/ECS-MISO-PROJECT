import esper
from src.ecs.components.c_surface import CSurface

from src.ecs.components.tags.c_tag_text import CTagText


def system_update_pause_texts(world: esper.World, is_paused: bool):
    components = world.get_components(CSurface,
                                      CTagText)
    c_s: CSurface
    c_t: CTagText
    for _, (c_s, c_t) in components:
        if c_t.type == "pause":
            if is_paused:
                c_s.surf.set_alpha(255)
            else:
                c_s.surf.set_alpha(0)
