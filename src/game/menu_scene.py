import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_background import system_background

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text, create_image
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator 

from src.ecs.components.c_bg_start import CBGStar
from src.create.prefab_creator import create_star, create_background

class MenuScene(Scene):
    
    def do_create(self):
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
        image = str(set_interface["logo_title"]["image"])
        
        # Crea las entidades de texto y asigna a los atributos correspondientes
        self.up = create_text(self.ecs_world, "1UP", 8, rojo, pygame.Vector2(32, 258), TextAlignment.LEFT)
        self.high = create_text(self.ecs_world, "HI-SCORE", 8, rojo, pygame.Vector2(152, 258), TextAlignment.RIGHT)
        self.score = create_text(self.ecs_world, "00", 8, blanco, pygame.Vector2(70, 268), TextAlignment.RIGHT)
        self.record = create_text(self.ecs_world, record, 8, azul, pygame.Vector2(145, 268), TextAlignment.RIGHT)
        
        self.logo = create_image(self.ecs_world, image, pygame.Vector2(55, 290))
        
        self.start = create_text(self.ecs_world, "PRESS Z TO START", 8, rojo, pygame.Vector2(128, 400), TextAlignment.CENTER)

        # Posiciones finales para cada elemento
        self.final_positions = {
            self.up: pygame.Vector2(32, 18),
            self.high: pygame.Vector2(152, 18),
            self.score: pygame.Vector2(70, 28),
            self.record: pygame.Vector2(145, 28),
            self.logo: pygame.Vector2(55, 50),
            self.start: pygame.Vector2(128, 160),
        }

        # Define la velocidad de movimiento de las entidades de texto
        self.speed = pygame.Vector2(0, -50)
        
        # Agrega un componente de entrada de comando a la entidad de inicio del juego
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,CInputCommand("START_GAME", pygame.K_z))
        
        # Configuración de fondo de estrellas
        bg_cfg = {
            "min_spawn_time": 0.1, 
            "max_spawn_time": 0.3, 
            "min_blink_time": 0.1, 
            "max_blink_time": 0.3, 
            "min_velocity": 10,  # Cambiado de "min_vel" a "min_velocity"
            "max_velocity": 30,  # Cambiado de "max_vel" a "max_velocity"
            "colors": [
                {"r": 100, "g": 100, "b": 255}, 
                {"r": 200, "g": 200, "b": 255}, 
                {"r": 255, "g": 255, "b": 255}
                ]
            }
        
        self.screen = pygame.display.get_surface()  # Obtén la superficie de la pantalla actual
        create_background(self.ecs_world, bg_cfg, self.screen)
        
        
    def do_update(self, delta_time):
        #self.screen = pygame.display.get_surface()
        system_background(self.ecs_world, delta_time, self.screen)
        for text_entity in [self.up, self.high, self.score, self.record, self.logo, self.start]:
            text_transform = self.ecs_world.component_for_entity(text_entity, CTransform)
            final_position = self.final_positions[text_entity]

            # Solo mover el elemento si aún no ha llegado a su posición final
            if text_transform.pos.y > final_position.y:
                text_transform.pos += self.speed * delta_time
                if text_transform.pos.y < final_position.y:
                    text_transform.pos.y = final_position.y
                    
    def do_draw(self, screen):
        # Primero dibuja las estrellas
        for _, (star) in self.ecs_world.get_component(CBGStar):
            screen.blit(star.surface, star.position) 
        
        # Luego dibuja los textos y logos
        for ent, (surf, transform) in self.ecs_world.get_components(CSurface, CTransform):
            if surf.show:
                screen.blit(surf.surf, transform.pos)

        pygame.display.flip()
        
                    
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")

