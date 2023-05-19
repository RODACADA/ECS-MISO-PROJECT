import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.show = True

    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        c_surf.show = True
        return c_surf

    """ @classmethod
    def from_text(cls, text: pygame.SurfaceType):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))

        c_surf.surf = text
        c_surf.area = text.get_rect()
        c_surf.show = True

        return c_surf """
    @classmethod
    def from_text(cls, text:str, font:pygame.font.Font, color:pygame.color):
        c_surf = cls(pygame.Vector2(0,0), color)
        c_surf.surf = font.render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        return c_surf
