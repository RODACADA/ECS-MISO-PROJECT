import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface

def system_blinking(world:esper.World, dt:float):
    for ent, (blink, surf) in world.get_components(CBlink, CSurface):
        blink.time_since_last_blink += dt
        if blink.time_since_last_blink > blink.blink_interval:
            surf.show = not surf.show  # Cambia el estado de visibilidad
            #print(f"Entity {ent} visibility: {surf.show}")  # Imprime el estado de visibilidad
            blink.time_since_last_blink = 0