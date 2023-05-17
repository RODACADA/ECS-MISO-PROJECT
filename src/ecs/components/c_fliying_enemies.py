import random


class CFlyingEnemies:
    def __init__(self, max_flying_enemies: int, min_flying_time: int, max_flying_time: int) -> None:
        self.flying_enemies_count = 0
        self.max_flying_enemies = max_flying_enemies
        self.min_flying_time = min_flying_time
        self.max_flying_time = max_flying_time
        self.next_flying_time = random.randrange(
            min_flying_time*100//1, max_flying_time*100//1 + 1)/100
