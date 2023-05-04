class CAbility:
    def __init__(self, next_available_time: int, cd_seconds: int) -> None:
        self.next_available_time = next_available_time
        self.cd_ms = cd_seconds*1000
