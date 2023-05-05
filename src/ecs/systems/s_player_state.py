import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_velocity import CVelocity


def system_enemy_state(world: esper.World):
    components = world.get_components(CEnemyState, CAnimation, CVelocity)
    for _, (c_st, c_a, c_v) in components:
        if c_st.state == EnemyState.MOVE:
            _do_enemy_move(c_st, c_a, c_v)
        elif c_st.state == EnemyState.FLYING_ATTACK:
            _do_enemy_flying_attack(c_st, c_a, c_v)
        elif c_st.state == EnemyState.FLYING_RETURN:
            _do_enemy_flying_return(c_st, c_a, c_v)


def _do_enemy_move(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "MOVE")
    # if c_v.vel.magnitude_squared() <= 0:
    #     c_st.state = EnemyState.FLYING_ATTACK


def _do_enemy_flying_attack(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "FLYING_ATTACK")
    if c_v.vel.magnitude_squared() > 0:
        c_st.state = EnemyState.FLYING_RETURN


def _do_enemy_flying_return(c_st: CEnemyState, c_a: CAnimation, c_v: CVelocity):
    set_animation(c_a, "FLYING_ATTACK")
    if c_v.vel.magnitude_squared() > 0:
        c_st.state = EnemyState.MOVE
