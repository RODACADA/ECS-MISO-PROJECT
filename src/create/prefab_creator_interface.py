from enum import Enum
import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_blink import CBlink


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


def create_menus(world:esper.World) -> dict:
    set_interface = ServiceLocator.setting_service.get("assets/cfg/interface.json")
    rojo = pygame.Color(set_interface["title_text_color"]["r"],
                                set_interface["title_text_color"]["g"],
                                set_interface["title_text_color"]["b"])
    blanco = pygame.Color(set_interface["normal_text_color"]["r"],
                                set_interface["normal_text_color"]["g"],
                                set_interface["normal_text_color"]["b"])
    azul = pygame.Color(set_interface["high_score_color"]["r"],
                                set_interface["high_score_color"]["g"],
                                set_interface["high_score_color"]["b"])
    record = str(set_interface["high_score_max_value"])
    
    screen_height = 256
    
    # Crea las entidades de texto y asigna a los atributos correspondientes
    up = create_text(world, "1UP", 8, rojo, pygame.Vector2(32, screen_height-10), TextAlignment.LEFT)
    high = create_text(world, "HI-SCORE", 8, rojo, pygame.Vector2(152, screen_height-10), TextAlignment.RIGHT)
    score = create_text(world, "00", 8, blanco, pygame.Vector2(70, screen_height), TextAlignment.RIGHT)
    record = create_text(world, record, 8, azul, pygame.Vector2(145, screen_height), TextAlignment.RIGHT)
    return {
        "up": up,
        "high": high,
        "score": score,
        "record": record,
    }

def create_logo(world:esper.World) -> int:
    set_interface = ServiceLocator.setting_service.get("assets/cfg/interface.json")
    screen = pygame.display.get_surface()  # superficie de la pantalla actual
    initial_y_pos = screen.get_height() + 50  # posición y inicial para el logo
    
    # imagen del logo desde la configuración
    image = str(set_interface["logo_title"]["image"])

    # Crea la entidad de logo y asigna a los atributos correspondientes
    logo = create_image(world, image, pygame.Vector2(55, initial_y_pos))
    
    return logo


def create_blinking_text(world:esper.World, text:str, alignment:TextAlignment, blink_interval: float) -> int:
    set_interface = ServiceLocator.setting_service.get("assets/cfg/interface.json")
    rojo = pygame.Color(set_interface["title_text_color"]["r"],
                                set_interface["title_text_color"]["g"],
                                set_interface["title_text_color"]["b"])
    screen_height = 256
    entity = create_text(world, text, 8, rojo, pygame.Vector2(128, screen_height+132), alignment)
    world.add_component(entity, CBlink(blink_interval))  # Agrega el componente CBlink a la entidad
    return entity


