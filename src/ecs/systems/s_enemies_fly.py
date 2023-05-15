import random
from typing import List
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemies_fly(world: esper.World, flying_enemies: List[int], max_flying_enemies: int):
    if flying_enemies[0] >= max_flying_enemies:
        return
    else:
        all_enemies = world.get_components(CTagEnemy)

        elegible_entities = []
        c_tag: CTagEnemy
        for enemy_entity, (c_tag,) in all_enemies:
            if not c_tag.is_flying:
                elegible_entities.append(enemy_entity)

        selected_enemy = random.choice(elegible_entities)

        enemy_tag: CTagEnemy = world.component_for_entity(
            selected_enemy, CTagEnemy)
        enemy_tag.is_flying = True

        flying_enemies[0] += 1
