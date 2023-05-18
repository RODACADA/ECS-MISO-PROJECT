

from typing import List

import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion


def system_collision_player_enemy(world: esper.World, player_entity: int,
                                  level_cfg: dict, explosion_info: dict, is_player_dead: List[bool], player_death_time: List[int]):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    sb_comp = world.get_components(CTagBulletStatic, CSurface)

    pl_rect = pl_s.area.copy()
    pl_rect.topleft = pl_t.pos

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - \
                pl_s.area.w / 2
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - \
                pl_s.area.h / 2
            create_explosion(world, c_t.pos, explosion_info)
            is_player_dead[0] = True
            player_death_time[0] = pygame.time.get_ticks()
            pl_s.show = False
            for _, (sb_tag, sb_s) in sb_comp:
                sb_s.show = False
