import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        
        # Imagem temporária 
        self.image = pygame.Surface((40, 40))
        self.image.fill("red")
        
        # Rect
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -20)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 100
        
        # Vida
        self.health = 1
    
    def get_direction(self):
        # Calcula direção em direção ao player
        enemy_pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.player.rect.center)
        
        if enemy_pos.distance_to(player_pos) > 0:
            self.direction = (player_pos - enemy_pos).normalize()
        else:
            self.direction = pygame.Vector2()
    
    def move(self, dt):
        # Move no eixo X e verifica colisão
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        
        # Move no eixo Y e verifica colisão
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        
        # Atualiza rect visual
        self.rect.center = self.hitbox_rect.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
    
    def update(self, dt):
        self.get_direction()
        self.move(dt)