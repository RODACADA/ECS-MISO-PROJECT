import json
import pygame
import esper

from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_player_square, \
    create_bullet, create_texts, create_background, create_flying_enemies
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_ability import CAbility
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic

from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_player_bullet import system_collision_player_bullet
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_enemies_bullets import system_enemies_bullets
from src.ecs.systems.s_enemies_fly import system_enemies_fly
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_enemy_hunter_state import system_enemy_hunter_state
from src.ecs.systems.s_static_bullet_movement import system_static_bullet_movement
from src.ecs.systems.s_update_cd_text import system_update_cd_text
from src.ecs.systems.s_update_pause_texts import system_update_pause_texts
import src.engine.game_engine


class PlayScene(Scene):
    def __init__(self, level_path: str, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open(level_path) as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        # with open("assets/cfg/explosion.json") as explosion_file:
        #     self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/interface.json") as interface_file:
            self.interface_cfg = json.load(interface_file)
        with open("assets/cfg/background.json") as bg_file:
            self.bg_cfg = json.load(bg_file)
        with open("assets/cfg/enemy_bullet.json") as enemy_bullet_file:
            self.enemy_bullet_cfg = json.load(enemy_bullet_file)
        with open("assets/cfg/enemy_explosion.json") as enemy_explosion_file:
            self.enemy_explosion_cfg = json.load(enemy_explosion_file)
        with open("assets/cfg/player_explosion.json") as player_explosion_file:
            self.player_explosion_cfg = json.load(player_explosion_file)
        with open("assets/cfg/enemies_sounds.json") as enemies_sounds_file:
            self.enemies_sounds_cfg = json.load(enemies_sounds_file)

        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self._paused = False
        self.ecs_world = esper.World()

        self.num_bullets = 0
        self.is_player_dead = [False]
        self.last_player_death_time = [None]
        self.game_over = False

    def do_create(self):
        create_text(self.ecs_world, "1UP", 8,
                    pygame.Color(50, 255, 50), pygame.Vector2(160, 20),
                    TextAlignment.CENTER)

        self._player_entity = create_player_square(
            self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"], self.bullet_cfg)
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(
            self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(
            self._player_entity, CSurface)

        s_bullet_components = self.ecs_world.get_components(
            CTagBulletStatic, CTransform, CVelocity, CSurface)

        for entity, (c_tag, c_t, c_v, c_s) in s_bullet_components:
            self._static_bullet_entity = entity,
            self._sb_transform = c_t
            self._sb_velocity = c_v
            self._sb_surface = c_s

        create_flying_enemies(self.ecs_world, self.level_01_cfg)
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)
        create_background(self.ecs_world, self.bg_cfg, self.screen)
        self.is_paused = False

        self.indicators = {
            "current_score": 0,
            "remaining_lives": 3,
            "curent_lvl": self.level_01_cfg["lvl_name"],
            "highest_score": self.level_01_cfg["highest_score"],
        }

    def do_update(self, delta_time: float):

        if not self.is_paused:
            if self.indicators["remaining_lives"] >= 1 and self.is_player_dead[0] and pygame.time.get_ticks() >= self.last_player_death_time[0]+self.level_01_cfg["player_respawn_time"]:
                self.reduce_lives()
                self.respawn_player()

            if not self.game_over and self.indicators["remaining_lives"] == 0 and self.is_player_dead[0]:
                self.game_over = True

            system_movement(self.ecs_world, delta_time)
            system_enemy_spawner(
                self.ecs_world, self.enemies_cfg, delta_time)
            system_static_bullet_movement(self.ecs_world)

            if not self.is_player_dead[0]:
                system_enemies_bullets(
                    self.ecs_world, self.level_01_cfg, self.enemy_bullet_cfg, self._player_c_t)
                system_enemies_fly(self.ecs_world, delta_time)

            system_screen_bounce(self.ecs_world, self.screen)
            system_screen_player(self.ecs_world, self.screen)
            system_screen_bullet(self.ecs_world, self.screen)

            if not self.is_player_dead[0]:
                system_collision_enemy_bullet(
                    self.ecs_world, self.enemy_explosion_cfg)
                system_collision_player_bullet(
                    self.ecs_world, self.player_explosion_cfg, self.is_player_dead, self.last_player_death_time)
                system_collision_player_enemy(self.ecs_world, self._player_entity,
                                              self.level_01_cfg, self.player_explosion_cfg, self.is_player_dead, self.last_player_death_time)

            system_explosion_kill(self.ecs_world)

            system_enemy_state(
                self.ecs_world, self._player_c_t, self.enemies_sounds_cfg, self.screen)
            # system_enemy_hunter_state(
            # self.ecs_world, self._player_entity, self.enemies_cfg["TypeHunter"])
            # system_update_cd_text(self.ecs_world, self._player_entity)

        # system_update_pause_texts(self.ecs_world, self.is_paused)
        system_animation(self.ecs_world, delta_time)

        system_background(self.ecs_world, delta_time, self.screen)
        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))

    """ def do_clean(self):
        self._paused = False """

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_FIRE" and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"] and not self.is_player_dead[0]:
            ServiceLocator.sounds_service.play(self.player_cfg["fire_sound"])
            create_bullet(self.ecs_world, self._player_c_t.pos,
                          self._player_c_s.area.size, self.bullet_cfg, False)
            self._sb_surface.show = False

        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                self.is_paused = not self.is_paused

    def respawn_player(self):
        self.is_player_dead[0] = False
        self._player_c_s.show = True
        self._sb_surface.show = True
        size = self._player_c_s.surf.get_size()
        pos = pygame.Vector2(self.level_01_cfg["player_spawn"]["position"]["x"] - (size[0] / 2),
                             self.level_01_cfg["player_spawn"]["position"]["y"] - (size[1] / 2))
        self._player_c_t.pos = pos

    def reduce_lives(self):
        self.indicators["remaining_lives"] -= 1
        # print("Reducing lives -1, remaining %s" %
        #       self.indicators["remaining_lives"])

    def increase_score(self, enemy_type: str, is_flying: bool):
        if is_flying:
            self.indicators["current_score"] += self.enemies_cfg[enemy_type]["kill_score"]
            # print("Updating scores (+%s)" %
            #       self.enemies_cfg[enemy_type]["kill_score"])
        else:
            self.indicators["current_score"] += (
                self.enemies_cfg[enemy_type]["kill_score"]*2)
            # print("Updating scores (+%s)" %
            #       self.enemies_cfg[enemy_type]["kill_score"] * 2)

    # def do_draw(self, screen: pygame.Surface):
    #    system_background(self.ecs_world, self.delta_time, screen)
