

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_static_bullet_movement(world: esper.World):
    player_components = world.get_components(CTransform, CTagPlayer, CSurface)
    s_bullet_components = world.get_components(CTransform, CTagBulletStatic)

    c_s: CSurface
    c_t: CTransform
    s_t: CTransform

    for _, (c_t, c_tag, c_s) in player_components:
        for _, (s_t, s_tag) in s_bullet_components:
            s_t.pos.x = c_t.pos.x + c_s.surf.get_rect().width//2
