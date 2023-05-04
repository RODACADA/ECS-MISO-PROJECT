
import pygame
import esper
from src.ecs.components.c_ability import CAbility
from src.ecs.components.c_power_def import CPowerDef
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator


def system_update_cd_text(world: esper.World, player_entity: int):
    components = world.get_components(CTagText, CSurface, CPowerDef)
    ability = world.component_for_entity(player_entity, CAbility)

    c_s: CSurface
    c_p: CPowerDef

    for _, (c_t, c_s, c_p) in components:
        transformed_cd = abs(
            (pygame.time.get_ticks() - ability.next_available_time) + ability.cd_ms)
        top = 100

        result = transformed_cd*top//ability.cd_ms
        result = min(result, 100)

        text_content = f"{result}%"

        font = ServiceLocator.fonts_service.get(c_p.font, c_p.size)
        text = font.render(text_content, True, c_p.color)
        c_s.surf = text
        c_s.area = text.get_rect()
