import pygame
import esper


from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_fliying_enemies import CFlyingEnemies
from src.engine.service_locator import ServiceLocator


def system_enemy_state(world: esper.World, player_position: CTransform, enemy_cfg: dict,
                       screen: pygame.Surface):
    _, flying_enemies = world.get_component(CFlyingEnemies)[0]
    components = world.get_components(
        CEnemyState, CAnimation, CVelocity, CTagEnemy, CTransform)
    for id, (c_st, c_a, c_v, c_tag, c_t) in components:
        if c_st.state == EnemyState.MOVE:
            _do_enemy_move(c_st, c_a, c_tag, enemy_cfg)
        elif c_st.state == EnemyState.FLYING_ATTACK:
            _do_enemy_flying_attack(
                c_st, c_a, c_v, player_position, c_t, c_tag, screen)
        elif c_st.state == EnemyState.FLYING_RETURN:
            _do_enemy_flying_return(
                c_st, c_a, c_v, c_t, c_tag, components, flying_enemies)


def _do_enemy_move(c_st: CEnemyState, c_a: CAnimation, c_tag: CTagEnemy, enemy_cfg: dict):
    set_animation(c_a, "MOVE")
    if c_tag.is_flying:
        c_st.state = EnemyState.FLYING_ATTACK
        ServiceLocator.sounds_service.play(enemy_cfg["attack_sound"])


def _do_enemy_flying_attack(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity, p_t: CTransform,
                            c_t: CTransform, c_tag: CTagEnemy, screen: pygame.Surface):
    set_animation(c_a, "FLYING_ATTACK")
    c_v.vel = pygame.Vector2(
        ((p_t.pos - c_t.pos).normalize()*c_tag.chase_velocity).x, c_tag.vertical_velocity)

    if c_t.pos.y > screen.get_height():
        c_t.pos.y = 0
        c_st.state = EnemyState.FLYING_RETURN


def _do_enemy_flying_return(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity,
                            c_t: CTransform, c_tag: CTagEnemy, components, flying_enemies: CFlyingEnemies):
    set_animation(c_a, "FLYING_ATTACK")

    other = False
    for id, (ec_st, ec_a, ec_v, ec_tag, ec_t) in components:
        if ec_t.pos_0 != c_t.pos_0 and not ec_tag.is_flying:
            o_t = ec_t
            o_v = ec_v
            o_a = ec_a
            other = True
            break

    if other:
        new_pos = c_t.pos_0 - o_t.pos_0 + o_t.pos
    else:
        new_pos = c_t.pos_0

    pos_diff = new_pos - c_t.pos

    if pos_diff.magnitude_squared() < 1:
        c_t.pos = new_pos
        if other:
            c_v.vel = o_v.vel.copy()
            c_a.curr_anim = o_a.curr_anim
            c_a.curr_anim_time = o_a.curr_anim_time
            c_a.curr_frame = o_a.curr_frame
        else:
            c_v.vel = pygame.Vector2(8, 0)
        c_st.state = EnemyState.MOVE
        c_tag.is_flying = False
        flying_enemies.flying_enemies_count -= 1
    else:
        c_v.vel = pygame.Vector2(pos_diff.normalize()*c_tag.vertical_velocity)
