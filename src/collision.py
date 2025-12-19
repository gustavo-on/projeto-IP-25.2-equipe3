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
    """Ataque de soco corpo-a-corpo com sprites direcionais (8 direções) e animação suave"""
    def __init__(self, pos, direction, damage, groups):
        super().__init__(groups)
        
        # Carrega os sprites direcionais
        self.load_directional_sprites()
        
        # Salva a direção e ângulo
        self.direction = direction
        angle = direction.angle_to(pygame.Vector2(1, 0))
        self.base_angle = angle
        
        # Escolhe o sprite base
        self.base_sprite = self.get_sprite_for_direction(direction)
        self.original_sprite = self.base_sprite.copy()
        
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 200
        
        self.start_scale = 0.4
        self.max_scale = 1.1
        self.current_scale = self.start_scale
        
        self.alpha = 0
        self.max_alpha = 255
        
        self.rotation_speed = 360  
        self.current_rotation = 0
        
        self.attack_distance = 60  # Distância em pixels do centro do player
        
        # Calcula posição com offset na direção do ataque
        offset = direction * self.attack_distance
        self.spawn_pos = (pos[0] + offset.x, pos[1] + offset.y)
        self.anchor_type = self.get_anchor_type(angle)
        
        # Cria a imagem inicial
        self.image = self.original_sprite.copy()
        self.rect = self.image.get_rect(center=self.spawn_pos)
        
        self.damage = damage
        self.hit_enemies = set()
    
    def get_anchor_type(self, angle):
        """Retorna o tipo de âncora baseado no ângulo"""
        if -22.5 <= angle < 22.5:
            return "midleft"
        elif 22.5 <= angle < 67.5:
            return "bottomleft"
        elif 67.5 <= angle < 112.5:
            return "midbottom"
        elif 112.5 <= angle < 157.5:
            return "bottomright"
        elif angle >= 157.5 or angle < -157.5:
            return "midright"
        elif -157.5 <= angle < -112.5:
            return "topright"
        elif -112.5 <= angle < -67.5:
            return "midtop"
        else:
            return "topleft"
    
    def update_animation(self, dt):
        """Atualiza a animação do ataque"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.spawn_time
        progress = elapsed / self.lifetime  # 0.0 a 1.0
        
        if progress < 0.3:  
            self.current_scale = self.start_scale + (self.max_scale - self.start_scale) * (progress / 0.3)
        elif progress < 0.7:  
            self.current_scale = self.max_scale
        else:  
            fade_progress = (progress - 0.7) / 0.3
            self.current_scale = self.max_scale - (fade_progress * 0.3)
        
       
        if progress < 0.2:  
            self.alpha = int(self.max_alpha * (progress / 0.2))
        elif progress < 0.8:  
            self.alpha = self.max_alpha
        else:  
            fade_progress = (progress - 0.8) / 0.2
            self.alpha = int(self.max_alpha * (1 - fade_progress))
        
        
        self.current_rotation += self.rotation_speed * dt * 0.3  
        # Aplica transformações
        self.apply_transformations()
    
    def apply_transformations(self):
        """Aplica escala, rotação e alpha ao sprite"""
        # Calcula novo tamanho
        original_size = self.original_sprite.get_size()
        new_size = (
            int(original_size[0] * self.current_scale),
            int(original_size[1] * self.current_scale)
        )
        
        # Escala
        scaled = pygame.transform.scale(self.original_sprite, new_size)
        
        total_rotation = self.current_rotation
        rotated = pygame.transform.rotate(scaled, total_rotation)
        
        
        rotated.set_alpha(self.alpha)
        
        # Atualiza imagem
        old_center = self.rect.center
        self.image = rotated
        self.rect = self.image.get_rect()
        
        setattr(self.rect, self.anchor_type, self.spawn_pos)
    
    def load_directional_sprites(self):
        """Carrega os sprites (4 cardinais + 4 diagonais se existirem)"""
        try:
            import os
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            
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
        # Atualiza animação
        self.update_animation(dt)
        
        # Remove após o lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()