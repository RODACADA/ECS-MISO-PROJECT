class CBlink:
    def __init__(self, blink_interval=1.0):
        self.blink_interval = blink_interval  # Cuánto tiempo (en segundos) esperar antes de cambiar el estado de visibilidad
        self.time_since_last_blink = 0.0  # Cuánto tiempo ha pasado desde la última vez que cambió el estado de visibilidad