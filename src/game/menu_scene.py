import pygame
import esper
import json
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_background import system_background
from src.ecs.systems.s_blink import system_blinking
from src.ecs.systems.s_rendering import system_rendering

from src.engine.scenes.scene import Scene
from src.create import prefab_creator_interface, prefab_creator
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator

from src.ecs.components.c_bg_start import CBGStar


class MenuScene(Scene):
    def do_create(self, context=None):
        self.screen = pygame.display.get_surface()
        set_background = ServiceLocator.setting_service.get(
            "assets/cfg/background.json")
        prefab_creator.create_background(
            self.ecs_world, set_background, self.screen)
        self.text_entities = prefab_creator_interface.create_menus(
            self.ecs_world)
        self.logo = prefab_creator_interface.create_logo(self.ecs_world)
        self.blinking_text = prefab_creator_interface.create_blinking_text(self.ecs_world,
                                                                           "PRESS Z TO START",
                                                                           prefab_creator_interface.TextAlignment.CENTER, 0.4)

        # Posiciones finales para cada elemento
        self.final_positions = {
            "up": pygame.Vector2(32, 15),
            "high": pygame.Vector2(152, 15),
            "score": pygame.Vector2(70, 25),            "record": pygame.Vector2(145, 25),
            "logo": pygame.Vector2(55, 57),
            # Posición final para el texto parpadeante
            "blinking_text": pygame.Vector2(128, 157),
        }

        # Define la velocidad de movimiento de las entidades de texto
        self.speed = pygame.Vector2(0, -50)

        # Agrega un componente de entrada de comando a la entidad de inicio del juego
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            start_game_action, CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time):
        self.screen = pygame.display.get_surface()
        system_background(self.ecs_world, delta_time, self.screen)
        system_blinking(self.ecs_world, delta_time)
        # Mueve las entidades de texto, logo y texto parpadeante a sus posiciones finales
        for entity_name, entity_id in {**self.text_entities, "logo": self.logo, "blinking_text": self.blinking_text}.items():
            entity_transform = self.ecs_world.component_for_entity(
                entity_id, CTransform)
            final_position = self.final_positions[entity_name]
        # Solo mover el elemento si aún no ha llegado a su posición final
            if entity_transform.pos.y > final_position.y:
                entity_transform.pos += self.speed * delta_time
                if entity_transform.pos.y < final_position.y:
                    entity_transform.pos.y = final_position.y

        
    def do_draw(self, screen):
        for _, (star, surf, transform) in self.ecs_world.get_components(CBGStar, CSurface, CTransform):
            if surf.show:
                screen.blit(surf.surf, transform.pos)

        for ent, (surf, transform) in self.ecs_world.get_components(CSurface, CTransform):
            if not self.ecs_world.has_component(ent, CBGStar) and surf.show:
                screen.blit(surf.surf, transform.pos)

        pygame.display.flip()    

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
