import pygame

class CollisionSprite(pygame.sprite.Sprite):
    # Sprite com colisão (objetos e paredes)
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)

        self.direction = direction
        self.speed = 800

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()