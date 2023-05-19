

import esper


from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_fliying_enemies import CFlyingEnemies
from src.create.prefab_creator import create_explosion


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict, increase_score):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    _, flying_enemies = world.get_component(CFlyingEnemies)[0]

    sb_components = world.get_components(CTagBulletStatic, CSurface)

    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                if c_ene.is_flying:
                    flying_enemies.flying_enemies_count -= 1
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)

                increase_score(c_ene.enemy_type, c_ene.is_flying)

                create_explosion(world, c_t.pos, explosion_info)
                for _, (s_tag, s_s) in sb_components:
                    s_s.show = True
