import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, x, y, size, groups, collision_sprites, color="blue"):
        super().__init__(groups)

        self.image = pygame.Surface((size, size))        
        self.image.fill("blue")
        
        self.size = size
        self.rect = self.image.get_frect(topleft=(x, y))
        
        # Status do jogador
        self.rock_quantities = 0
        self.health = 10
        self.current_health = 10
        self.damage = 2
        self.range_size = 30

        # ✅ ADICIONADO: Sistema de Level e XP
        self.level = 1
        self.current_xp = 0
        self.next_level_up = 10

        self.attributes_points = 0
        
        # Vetor de direção do movimento
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        
        self.direction = self.direction.normalize() if self.direction else self.direction       

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        
        self.rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
    
    def die(self):
        print("Game Over")
    
    def update(self, dt):
        self.input()
        self.move(dt)