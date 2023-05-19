

from typing import List

import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.create.prefab_creator import create_explosion


def system_collision_player_bullet(world: esper.World, explosion_info: dict, is_player_dead: List[bool], player_death_time: List[int]):
    components_player = world.get_components(CSurface, CTransform, CTagPlayer)
    components_bullet = world.get_components(
        CSurface, CTransform, CTagBulletEnemy)

    sb_comp = world.get_components(CTagBulletStatic, CSurface)

    for player_entity, (c_s, c_t, c_tag) in components_player:
        player_rect = c_s.area.copy()
        player_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if player_rect.colliderect(bull_rect):
                c_s.show = False
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, explosion_info)
                is_player_dead[0] = True
                for _, (sb_tag, sb_s) in sb_comp:
                    sb_s.show = False
                player_death_time[0] = pygame.time.get_ticks()
