from enum import Enum
import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, txt: str, size: int,
                color: pygame.Color, pos: pygame.Vector2, alignment: TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get(
        "assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity


def update_text(world: esper.World, entity: int, text: str, size: int, color):
    font = ServiceLocator.fonts_service.get(
        "assets/fnt/PressStart2P.ttf", size)

    component = world.component_for_entity(entity, CSurface)
    component.surf = font.render(text, True, color)
    component.area = component.surf.get_rect()


def create_image(world: esper.World, img_path: str, pos: pygame.Vector2):
    image_entity = world.create_entity()

    # Carga la imagen desde el archivo
    image_surface = pygame.image.load(img_path)

    world.add_component(image_entity, CSurface.from_surface(image_surface))
    world.add_component(image_entity, CTransform(pos))

    return image_entity
