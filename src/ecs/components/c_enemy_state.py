from enum import Enum


class CEnemyState:
    def __init__(self):
        self.state = EnemyState.MOVE


class EnemyState(Enum):
    MOVE = 0
    FLYING_ATTACK = 1
    FLYING_RETURN = 2
