import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text, create_image
from src.ecs.components.c_input_command import CInputCommand 

class MenuScene(Scene):
    
    def do_create(self):
        # Crea las entidades de texto y asigna a los atributos correspondientes
        self.title = create_text(self.ecs_world, "MAIN MENU", 12, 
                    pygame.Color(50, 255, 50), pygame.Vector2(128, 200), TextAlignment.CENTER)
        
        self.logo = create_image(self.ecs_world, "./assets/img/invaders_logo_title.png",
                                pygame.Vector2(55, 220))
        
        self.start = create_text(self.ecs_world, "PRESS Z TO START GAME", 9, 
                    pygame.Color(255, 255, 0), pygame.Vector2(128, 275), TextAlignment.CENTER)
        
        self.controls = create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 7, 
                    pygame.Color(150, 150, 255), pygame.Vector2(128, 290), TextAlignment.CENTER)
        
        

        # Define la velocidad de movimiento de las entidades de texto
        self.speed = pygame.Vector2(0, -40)
        
        # Agrega un componente de entrada de comando a la entidad de inicio del juego
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,CInputCommand("START_GAME", pygame.K_z))
        
    def do_update(self, delta_time):
        for text_entity in [self.logo, self.title, self.start, self.controls]:
            text_transform = self.ecs_world.component_for_entity(text_entity, CTransform)
            text_transform.pos += self.speed * delta_time

        if text_transform.pos.y < 100:
            self.speed = pygame.Vector2(0, 0) 
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")