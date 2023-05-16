import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand 

class MenuScene(Scene):
    
    def do_create(self):
        create_text(self.ecs_world, "MAIN MENU", 12, 
                    pygame.Color(50, 255, 50), pygame.Vector2(128, 100), TextAlignment.CENTER)
        create_text(self.ecs_world, "PRESS Z TO START GAME", 9, 
                    pygame.Color(255, 255, 0), pygame.Vector2(128, 140), TextAlignment.CENTER)
        create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 7, 
                    pygame.Color(150, 150, 255), pygame.Vector2(128, 167), TextAlignment.CENTER)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")