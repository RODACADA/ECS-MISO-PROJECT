import random
import esper
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_fliying_enemies import CFlyingEnemies


def system_enemies_fly(world: esper.World, delta_time: float):
    _, flying_enemies = world.get_component(CFlyingEnemies)[0]

    flying_enemies.next_flying_time -= delta_time

    if flying_enemies.next_flying_time <= 0 and flying_enemies.flying_enemies_count < flying_enemies.max_flying_enemies:
        all_enemies = world.get_components(CTagEnemy)

        elegible_entities = []
        c_tag: CTagEnemy
        for enemy_entity, (c_tag,) in all_enemies:
            if not c_tag.is_flying:
                elegible_entities.append(enemy_entity)

        if len(elegible_entities) > 0:
            selected_enemy = random.choice(elegible_entities)

            enemy_tag: CTagEnemy = world.component_for_entity(
                selected_enemy, CTagEnemy)
            enemy_tag.is_flying = True
            flying_enemies.flying_enemies_count += 1
            flying_enemies.next_flying_time = random.randrange(
                flying_enemies.min_flying_time*100//1, flying_enemies.max_flying_time*100//1 + 1)/100
