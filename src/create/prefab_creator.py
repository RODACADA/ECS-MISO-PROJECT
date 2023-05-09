import random
import pygame
import esper
from src.ecs.components.c_ability import CAbility

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_power_def import CPowerDef
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.c_bg_star_spawner import CBgStarSpawner
from src.ecs.components.c_bg_start import CBGStar
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_sprite = ServiceLocator.images_service.get(enemy_info["image"])
    size = enemy_sprite.get_size()
    if "animations" in enemy_info:
        size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(pos.x - (size[0] / 2),
                         pos.y - (size[1] / 2))
    # vel_max = enemy_info["velocity_max"]
    # vel_min = enemy_info["velocity_min"]
    # vel_range = random.randrange(vel_min, vel_max)
    # velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
    #                           random.choice([-vel_range, vel_range]))

    # velocity = pygame.Vector2(0, 0)
    velocity = pygame.Vector2(enemy_info["velocity"], 0)

    enemy_entity = create_sprite(world, pos, velocity, enemy_sprite)

    world.add_component(enemy_entity, CTagEnemy(
        "Bouncer", enemy_info["vertical_velocity"], enemy_info["chase_velocity"]))
    if "animations" in enemy_info:
        world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CEnemyState())
    # ServiceLocator.sounds_service.play(enemy_info["sound"])


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])

    size = player_surface.get_size()
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_surface)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


# def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
#     enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
#     velocity = pygame.Vector2(0, 0)
#     enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
#     world.add_component(enemy_entity, CEnemyHunterState(pos))
#     world.add_component(enemy_entity,
#                         CAnimation(enemy_info["animations"]))
    # world.add_component(enemy_entity, CTagEnemy("Hunter"))


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_fire = world.create_entity()
    input_pause = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))
    world.add_component(input_pause, CInputCommand("PAUSE", pygame.K_p))


def create_bullet(world: esper.World,
                  mouse_pos: pygame.Vector2,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):

    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])

    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]
    ServiceLocator.sounds_service.play(bullet_info["sound"])

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(
        explosion_info["image"])

    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity


def create_texts(world: esper.World, text_def: dict):
    for text_item in text_def["texts"]:
        text_entity = world.create_entity()
        pos = pygame.Vector2(text_item["position"]
                             ["x"], text_item["position"]["y"])
        color = pygame.Color(text_item["color"]["r"],
                             text_item["color"]["g"], text_item["color"]["b"])

        font = ServiceLocator.fonts_service.get(
            text_item["fnt"], text_item["size"])
        text = font.render(text_item["text"], True, color)

        world.add_component(text_entity, CTransform(pos))
        world.add_component(text_entity, CSurface.from_text(text))

        type = "STATIC" if text_item["isStatic"] else text_item["id"]

        world.add_component(text_entity, CTagText(type))

        if type == "power":
            world.add_component(text_entity, CPowerDef(
                pos, text_item["size"], color, text_item["fnt"]))


def create_star(world: esper.World, spawner: CBgStarSpawner, screen: pygame.Surface, y=0):
    start_entity = world.create_entity()
    color = random.choice(spawner.colors)
    velocity = random.randrange(spawner.min_vel, spawner.max_vel+1)
    position = pygame.Vector2(random.randrange(0, screen.get_width()+1), y)
    blink_time = random.randrange(
        spawner.min_blink_time*100//1, spawner.max_blink_time*100//1 + 1)/100

    star_comp = CBGStar(color, velocity, position, blink_time)

    world.add_component(start_entity, star_comp)


def create_background(world: esper.World, bg_cfg: dict, screen: pygame.Surface):
    bg_entity = world.create_entity()
    spawner = CBgStarSpawner(bg_cfg)
    world.add_component(bg_entity, spawner)

    initial_count = int(screen.get_height() * 4 / (spawner.max_vel +
                        spawner.min_vel) / (spawner.min_spawn_time + spawner.max_spawn_time))

    for i in range(initial_count):
        y = random.randint(0, screen.get_height())
        create_star(world, spawner, screen, y)
