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

class Punch(pygame.sprite.Sprite):
    """Ataque de soco corpo-a-corpo com sprites direcionais (8 direções)"""
    def __init__(self, pos, direction, damage, groups):
        super().__init__(groups)
        
        # Carrega os sprites direcionais
        self.load_directional_sprites()
        
        # Calcula o ângulo primeiro para saber a direção
        angle = direction.angle_to(pygame.Vector2(1, 0))
        
        # Escolhe o sprite baseado na direção
        self.image = self.get_sprite_for_direction(direction)
        
        # Posiciona baseado na direção usando diferentes pontos de âncora
        if -22.5 <= angle < 22.5:  # Direita
            self.rect = self.image.get_rect(midleft=(int(pos[0]), int(pos[1])))
        elif 22.5 <= angle < 67.5:  # Cima-Direita (diagonal)
            self.rect = self.image.get_rect(bottomleft=(int(pos[0]), int(pos[1])))
        elif 67.5 <= angle < 112.5:  # Cima
            self.rect = self.image.get_rect(midbottom=(int(pos[0]), int(pos[1])))
        elif 112.5 <= angle < 157.5:  # Cima-Esquerda (diagonal)
            self.rect = self.image.get_rect(bottomright=(int(pos[0]), int(pos[1])))
        elif angle >= 157.5 or angle < -157.5:  # Esquerda
            self.rect = self.image.get_rect(midright=(int(pos[0]), int(pos[1])))
        elif -157.5 <= angle < -112.5:  # Baixo-Esquerda (diagonal)
            self.rect = self.image.get_rect(topright=(int(pos[0]), int(pos[1])))
        elif -112.5 <= angle < -67.5:  # Baixo
            self.rect = self.image.get_rect(midtop=(int(pos[0]), int(pos[1])))
        else:  # Baixo-Direita (diagonal)
            self.rect = self.image.get_rect(topleft=(int(pos[0]), int(pos[1])))
        
        self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 200
        
        self.hit_enemies = set()
    
    def load_directional_sprites(self):
        """Carrega os sprites (4 cardinais + 4 diagonais se existirem)"""
        try:
            import os
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            
            # Carrega sprites cardinais (obrigatórios)
            up_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortecima.png")
            down_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortebaixo.png")
            right_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortedireita.png")
            left_path = os.path.join(BASE_DIR, "..", "assets", "images", "corteesquerda.png")
            
            self.sprite_up = pygame.transform.scale(
                pygame.image.load(up_path).convert_alpha(), (100, 100)
            )
            self.sprite_down = pygame.transform.scale(
                pygame.image.load(down_path).convert_alpha(), (100, 100)
            )
            self.sprite_right = pygame.transform.scale(
                pygame.image.load(right_path).convert_alpha(), (100, 100)
            )
            self.sprite_left = pygame.transform.scale(
                pygame.image.load(left_path).convert_alpha(), (100, 100)
            )
            
            # Tenta carregar sprites diagonais (opcionais)
            try:
                upright_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortecimadireita.png")
                upleft_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortecimaesquerda.png")
                downright_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortebaixodireita.png")
                downleft_path = os.path.join(BASE_DIR, "..", "assets", "images", "cortebaixoesquerda.png")
                
                self.sprite_upright = pygame.transform.scale(
                    pygame.image.load(upright_path).convert_alpha(), (100, 100)
                )
                self.sprite_upleft = pygame.transform.scale(
                    pygame.image.load(upleft_path).convert_alpha(), (100, 100)
                )
                self.sprite_downright = pygame.transform.scale(
                    pygame.image.load(downright_path).convert_alpha(), (100, 100)
                )
                self.sprite_downleft = pygame.transform.scale(
                    pygame.image.load(downleft_path).convert_alpha(), (100, 100)
                )
            except:
                # Se não tiver diagonais, rotaciona os cardinais
                self.sprite_upright = pygame.transform.rotate(self.sprite_right, 45)
                self.sprite_upleft = pygame.transform.rotate(self.sprite_left, -45)
                self.sprite_downright = pygame.transform.rotate(self.sprite_right, -45)
                self.sprite_downleft = pygame.transform.rotate(self.sprite_left, 45)
            
            
        except Exception as e:
            # Fallback: círculo
            fallback = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(fallback, (255, 200, 0), (25, 25), 20)
            pygame.draw.circle(fallback, (255, 150, 0), (25, 25), 15)
            
            self.sprite_right = fallback
            self.sprite_left = fallback
            self.sprite_up = fallback
            self.sprite_down = fallback
            self.sprite_upright = fallback
            self.sprite_upleft = fallback
            self.sprite_downright = fallback
            self.sprite_downleft = fallback
    
    def get_sprite_for_direction(self, direction):
        """Escolhe o sprite correto baseado na direção (8 direções)"""
        # Calcula o ângulo da direção
        angle = direction.angle_to(pygame.Vector2(1, 0))
        
        # Determina qual sprite usar baseado no ângulo (8 direções)
        if -22.5 <= angle < 22.5:
            return self.sprite_right  # →
        elif 22.5 <= angle < 67.5:
            return self.sprite_upright  # ↗
        elif 67.5 <= angle < 112.5:
            return self.sprite_up  # ↑
        elif 112.5 <= angle < 157.5:
            return self.sprite_upleft  # ↖
        elif angle >= 157.5 or angle < -157.5:
            return self.sprite_left  # ←
        elif -157.5 <= angle < -112.5:
            return self.sprite_downleft  # ↙
        elif -112.5 <= angle < -67.5:
            return self.sprite_down  # ↓
        else:
            return self.sprite_downright  # ↘
    
    def update(self, dt):
        # Remove após o lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
