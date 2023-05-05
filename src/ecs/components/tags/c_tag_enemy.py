class CTagEnemy:
    def __init__(self, enemy_type: str, vertical_velocity: int, chase_velocity: int) -> None:
        self.enemy_type = enemy_type
        self.is_flying = False
        self.vertical_velocity = vertical_velocity
        self.chase_velocity = chase_velocity
