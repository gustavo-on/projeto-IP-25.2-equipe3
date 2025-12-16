import pygame

class Player:
    def __init__(self, x, y, size, collision_sprites, color="blue"):
        # Posição inicial
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        
        # Retângulo para posição e colisão 
        self.rect = pygame.Rect(x, y, size, size)

        # Vetor de direção do movimento
        self.direction = pygame.Vector2(0, 0)
        self.speed = 500  
        
        self.collision_sprites = collision_sprites
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal: D/→ (direita) ou A/← (esquerda)
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        
        # Movimento vertical: S/↓ (baixo) ou W/↑ (cima)
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        
        # Normaliza o vetor para evitar movimento mais rápido na diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction       

    def move(self, dt):
        # Move no eixo X e verifica colisão horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        
        # Move no eixo Y e verifica colisão vertical
        self.rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):
        # Detecta e resolve colisões com sprites de colisão
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    # Colisão horizontal: empurra para o lado oposto
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                else:
                    # Colisão vertical: empurra para cima/baixo
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top