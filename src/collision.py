import pygame

class CollisionSprite(pygame.sprite.Sprite):
    # Sprite com colisão (objetos e paredes)
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)