import json
import pygame
import esper

from src.create import prefab_creator_interface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

from src.ecs.systems.s_blink import system_blinking

from src.ecs.systems.s_delete_start_text import system_delete_start_text
from src.ecs.systems.s_show_static_bullet import system_show_static_bullet


from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_player_square, \
    create_bullet, create_background, create_flying_enemies

from src.create.prefab_creator_interface import TextAlignment, create_level_flags, create_life_counter, create_text, update_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_bullet_static import CTagBulletStatic

from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_player_bullet import system_collision_player_bullet
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_enemies_bullets import system_enemies_bullets
from src.ecs.systems.s_enemies_fly import system_enemies_fly
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_static_bullet_movement import system_static_bullet_movement
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

        self.ecs_world = esper.World()

        self.title_text_color = pygame.Color(self.interface_cfg["title_text_color"]["r"], self.interface_cfg["title_text_color"]
                                             ["g"], self.interface_cfg["title_text_color"]["b"])
        self.normal_text_color = pygame.Color(self.interface_cfg["normal_text_color"]["r"], self.interface_cfg["normal_text_color"]
                                              ["g"], self.interface_cfg["normal_text_color"]["b"])
        self.high_score_color = pygame.Color(self.interface_cfg["high_score_color"]["r"], self.interface_cfg["high_score_color"]
                                             ["g"], self.interface_cfg["high_score_color"]["b"])

    def do_create(self, context=None):
        self._paused = False
        self.finished_time = 0
        self.num_bullets = 0
        self.remaining_enemies = 10
        self.is_player_dead = [False]
        self.last_player_death_time = [None]
        self.game_over = False
        self.last_enemies_dir_swap = [0]

        self.allow_compensation_left = False
        self.allow_compensation_right = False
        if context is None:
            self.indicators = {
                "current_score": self.level_01_cfg["initial_score"],
                "remaining_lives": self.level_01_cfg["player_lives"],
                "curent_lvl": self.level_01_cfg["lvl_name"],
                "highest_score": self.level_01_cfg["highest_score"],
            }
        else:
            self.indicators = context

        level_str = "0" + \
            str(self.indicators["curent_lvl"]) if self.indicators["curent_lvl"] < 10 else str(
                self.indicators["curent_lvl"])

        prefab_creator_interface.create_menus(self.ecs_world)
        self.start_time = pygame.time.get_ticks()
        ServiceLocator.sounds_service.play(self.level_01_cfg["start_sound"])
        create_text(self.ecs_world, "1UP", 8,
                    self.title_text_color, pygame.Vector2(32, 15),
                    TextAlignment.LEFT)

        score = "00" if self.indicators["current_score"] == 0 else str(
            self.indicators["current_score"])
        self.score_text = create_text(self.ecs_world, score, 8,
                                      self.normal_text_color, pygame.Vector2(
                                          70, 25),
                                      TextAlignment.RIGHT)

        # Creación del contador de niveles
        lvl = "00" if self.indicators["curent_lvl"] == 0 else str(
            self.indicators["curent_lvl"])
        self.level_text = create_text(self.ecs_world, "0" + lvl, 8,
                                      self.normal_text_color, pygame.Vector2(220, 24), TextAlignment.RIGHT)

        create_text(self.ecs_world, "HI-SCORE", 8,  pygame.Color(
            self.interface_cfg["title_text_color"]["r"],
            self.interface_cfg["title_text_color"]["g"],
            self.interface_cfg["title_text_color"]["b"]),
            pygame.Vector2(152, 15), TextAlignment.RIGHT)

        create_text(self.ecs_world, "HI-SCORE", 8,  pygame.Color(self.interface_cfg["title_text_color"]["r"], self.interface_cfg["title_text_color"]
                                                                 ["g"], self.interface_cfg["title_text_color"]["b"]),
                    pygame.Vector2(152, 15), TextAlignment.RIGHT)

        create_text(self.ecs_world, str(self.interface_cfg["high_score_max_value"]),
                    8, self.high_score_color, pygame.Vector2(145, 25), TextAlignment.RIGHT)

        self.start_text = create_text(self.ecs_world, "GAME START", 8,
                                      self.normal_text_color, pygame.Vector2(
                                          128, 160),
                                      TextAlignment.CENTER)

        self.paused_text = create_text(self.ecs_world, "PAUSED", 8,
                                       self.title_text_color, pygame.Vector2(
                                           128, 160),
                                       TextAlignment.CENTER)

        self._paused_cs = self.ecs_world.component_for_entity(
            self.paused_text, CSurface)
        self._paused_cs.show = False

        self.game_over_text = create_text(self.ecs_world, "GAME OVER - PRESS 'M'", 8,
                                          self.normal_text_color, pygame.Vector2(
                                              128, 160),
                                          TextAlignment.CENTER)

        self._game_over_cs = self.ecs_world.component_for_entity(
            self.game_over_text, CSurface)
        self._game_over_cs.show = False

        self.next_lvl_text = create_text(self.ecs_world, "GET READY FOR THE NEXT LEVEL", 8,
                                         self.title_text_color, pygame.Vector2(
                                             128, 160),
                                         TextAlignment.CENTER)
        self._next_lvl_cs = self.ecs_world.component_for_entity(
            self.next_lvl_text, CSurface)
        self._next_lvl_cs.show = False

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
        life_config = ServiceLocator.setting_service.get(
            "assets/cfg/interface.json")["vidas"]
        # Dibuja el contador de vidas
        self.lives = create_life_counter(
            self.ecs_world, life_config, self.indicators["remaining_lives"])

        # Crea la bandera del primer nivel
        self.flag_entities = create_level_flags(self.ecs_world, 1)

        self.is_paused = False

    def do_update(self, delta_time: float):
        if self._next_lvl_cs.show and pygame.time.get_ticks() >= 2000 + self.finished_time:
            self.indicators["curent_lvl"] += 1
            self.switch_scene("LEVEL_01", context=self.indicators)

        if not self.is_paused and pygame.time.get_ticks() >= 2000 + self.start_time:
            if self.remaining_enemies == 0 and pygame.time.get_ticks() >= 5000 + self.start_time:
                self._next_lvl_cs.show = True
                if self.finished_time == 0:
                    self.finished_time = pygame.time.get_ticks()

            if self.indicators["remaining_lives"] >= 1 and self.is_player_dead[0] and pygame.time.get_ticks() >= self.last_player_death_time[0]+self.level_01_cfg["player_respawn_time"]:
                self.reduce_lives()
                self.respawn_player()

            if not self.game_over and self.indicators["remaining_lives"] == 0 and self.is_player_dead[0]:
                self.game_over = True
                ServiceLocator.sounds_service.play(
                    self.level_01_cfg["game_over_sound"])
                self._game_over_cs.show = True

            system_movement(self.ecs_world, delta_time)
            system_enemy_spawner(
                self.ecs_world, self.enemies_cfg, delta_time)
            system_static_bullet_movement(self.ecs_world)
            system_show_static_bullet(
                self.ecs_world, self._sb_surface, self.is_player_dead)

            if not self.is_player_dead[0]:
                system_enemies_bullets(
                    self.ecs_world, self.level_01_cfg, self.enemy_bullet_cfg, self._player_c_t)
                system_enemies_fly(self.ecs_world, delta_time)

            system_screen_bounce(self.ecs_world, self.screen,
                                 self.last_enemies_dir_swap)
            system_screen_player(self.ecs_world, self.screen)
            system_screen_bullet(self.ecs_world, self.screen)

            if not self.is_player_dead[0]:
                system_collision_enemy_bullet(
                    self.ecs_world, self.enemy_explosion_cfg, self.increase_score)
                system_collision_player_bullet(
                    self.ecs_world, self.player_explosion_cfg, self.is_player_dead, self.last_player_death_time)
                system_collision_player_enemy(self.ecs_world, self._player_entity,
                                              self.level_01_cfg, self.player_explosion_cfg, self.is_player_dead, self.last_player_death_time)

            system_explosion_kill(self.ecs_world)
            system_delete_start_text(
                self.ecs_world, self.start_time, self.start_text)
            system_enemy_state(
                self.ecs_world, self._player_c_t, self.enemies_sounds_cfg, self.screen)

        system_animation(self.ecs_world, delta_time)

        system_background(self.ecs_world, delta_time, self.screen)
        system_blinking(self.ecs_world, delta_time)

        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))
        self.remaining_enemies = len(self.ecs_world.get_component(CTagEnemy))

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self.allow_compensation_left = True
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END and self.allow_compensation_left:
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self.allow_compensation_right = True
                self._player_c_v.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END and self.allow_compensation_right:
                self._player_c_v.vel.x -= self.player_cfg["input_velocity"]

        if c_input.name == "PLAYER_FIRE" and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"] and not self.is_player_dead[0]:
            ServiceLocator.sounds_service.play(self.player_cfg["fire_sound"])
            create_bullet(self.ecs_world, self._player_c_t.pos,
                          self._player_c_s.area.size, self.bullet_cfg, False)
            self._sb_surface.show = False

        if c_input.name == "BACK_TO_HOME" and self.game_over:
            self.switch_scene("MENU_SCENE")

        if c_input.name == "PAUSE":
            if c_input.phase == CommandPhase.START:
                if not self.is_paused:
                    ServiceLocator.sounds_service.play(
                        self.level_01_cfg["pause_sound"])
                    self._paused_cs.show = True
                else:
                    self._paused_cs.show = False

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
        # Reduce la cantidad de vidas en los indicadores
        self.indicators["remaining_lives"] -= 1

        # Elimina una de las entidades de vida
        if self.lives:
            life_to_remove = self.lives.pop()
            self.ecs_world.delete_entity(life_to_remove)

    def increase_score(self, enemy_type: str, is_flying: bool):
        if not is_flying:
            self.indicators["current_score"] += self.enemies_cfg[enemy_type]["kill_score"]
        else:
            self.indicators["current_score"] += (
                self.enemies_cfg[enemy_type]["kill_score"]*2)

        update_text(self.ecs_world, self.score_text, str(
            self.indicators["current_score"]), 8, self.normal_text_color)
