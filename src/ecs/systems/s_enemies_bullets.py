

import random
import esper
from src.create.prefab_creator import create_bullet_enemy
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_bullets(world: esper.World, lvl_config: dict, enemy_bullet_cfg: dict):
    prob_move = lvl_config["enemies_fire_prob_move"]
    prob_attacking = lvl_config["enemies_fire_prob_attacking"]

    enemies = world.get_components(
        CTagEnemy, CEnemyState, CSurface, CTransform)

    c_tag: CTagEnemy
    c_s: CEnemyState
    c_surf: CSurface
    c_t: CTransform
    for id, (c_tag, c_s, c_surf, c_t) in enemies:
        prob = prob_move if c_s.state == EnemyState.MOVE else prob_attacking

        if random.random() <= prob:
            create_bullet_enemy(
                world, c_t.pos, c_surf.area.size, enemy_bullet_cfg)
