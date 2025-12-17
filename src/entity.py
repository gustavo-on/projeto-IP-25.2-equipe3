import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 6
        self.direction = pygame.Vector2()
    
    def take_damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.die()
    
    def die(self):
        self.kill()