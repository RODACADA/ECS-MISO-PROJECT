

import random
import esper
from src.create.prefab_creator import create_bullet_enemy, create_bullet_enemy_directed
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_bullets(world: esper.World, lvl_config: dict, enemy_bullet_cfg: dict, p_t: CTransform):
    prob_move = lvl_config["enemies_fire_prob_move"]
    prob_attacking = lvl_config["enemies_fire_prob_attacking"]

    enemies = world.get_components(
        CTagEnemy, CEnemyState, CSurface, CTransform)

    c_tag: CTagEnemy
    c_s: CEnemyState
    c_surf: CSurface
    c_t: CTransform
    for _, (c_tag, c_s, c_surf, c_t) in enemies:
        prob = prob_move if c_s.state == EnemyState.MOVE else prob_attacking
        should_fire = random.random() <= prob

        if should_fire and c_s.state == EnemyState.MOVE:
            create_bullet_enemy(
                world, c_t.pos, c_surf.area.size, enemy_bullet_cfg)

        if should_fire and c_s.state == EnemyState.FLYING_ATTACK:
            y_diff = p_t.pos.y - c_t.pos.y
            if y_diff > 10:
                create_bullet_enemy_directed(
                    world, c_t.pos, c_surf.area.size, enemy_bullet_cfg, p_t.pos)
