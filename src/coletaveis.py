import pygame

class XP(pygame.sprite.Sprite):
    def __init__(self, pos, amount, groups):
        super().__init__(groups)

        self.image = pygame.Surface((12, 12))
        self.image.fill('gold')

        self.rect = self.image.get_rect(center=pos)

        self.amount = amount

class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        