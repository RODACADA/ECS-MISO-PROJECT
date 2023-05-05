import pygame
import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_state(world: esper.World, player_position: CTransform):
    components = world.get_components(
        CEnemyState, CAnimation, CVelocity, CTagEnemy, CTransform)
    for _, (c_st, c_a, c_v, c_tag, c_t) in components:
        if c_st.state == EnemyState.MOVE:
            _do_enemy_move(c_st, c_a, c_tag)
        elif c_st.state == EnemyState.FLYING_ATTACK:
            _do_enemy_flying_attack(
                c_st, c_a, c_v, player_position, c_t, c_tag)
        elif c_st.state == EnemyState.FLYING_RETURN:
            _do_enemy_flying_return(c_st, c_a, c_v)


def _do_enemy_move(c_st: CEnemyState, c_a: CAnimation, c_tag: CTagEnemy):
    set_animation(c_a, "MOVE")
    if c_tag.is_flying:
        c_st.state = EnemyState.FLYING_ATTACK


def _do_enemy_flying_attack(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity, p_t: CTransform, c_t: CTransform, c_tag: CTagEnemy):
    set_animation(c_a, "FLYING_ATTACK")

    c_v.vel = pygame.Vector2(
        ((p_t.pos - c_t.pos).normalize()*c_tag.chase_velocity).x, c_tag.vertical_velocity)

    if c_v.vel.magnitude_squared() > 0:
        c_st.state = EnemyState.FLYING_RETURN


def _do_enemy_flying_return(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "FLYING_ATTACK")
    if c_v.vel.magnitude_squared() > 0:
        c_st.state = EnemyState.MOVE
