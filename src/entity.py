import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 6
        self.direction = pygame.Vector2()

        self.health = 10
        self.current_health = 10
        self.damage = 1
    
    def take_damage(self, amount):
        self.current_health -= amount

        if self.current_health <= 0:
            self.die()
    
    def die(self):
        self.kill()