import pygame
import os
from coletaveis import XP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        self.xp_value = 1
        
        # Carrega sprites
        self.load_animations()
        
        self.current_animation = "right"
        self.frame_index = 0
        self.animation_speed = 8
        
        self.image = self.animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -20)
        
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 100
        
        self.health = 1
        self.damage = 1
    
    def load_animations(self):
        """Carrega sprites do inimigo (esquerda e direita)"""
        self.animations = {
            "left": [],
            "right": []
        }
        
        animations_path = os.path.join(BASE_DIR, "..", "assets", "images", "enemy")
        
        try:
            # Direita
            right_path = os.path.join(animations_path, "right")
            if os.path.exists(right_path):
                files = sorted([f for f in os.listdir(right_path) if f.endswith('.png')])
                for file in files:
                    image_path = os.path.join(right_path, file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (100, 100)) # tamanho 
                    self.animations["right"].append(image)
            
            # Esquerda
            left_path = os.path.join(animations_path, "left")
            if os.path.exists(left_path):
                files = sorted([f for f in os.listdir(left_path) if f.endswith('.png')])
                for file in files:
                    image_path = os.path.join(left_path, file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (100, 100))
                    self.animations["left"].append(image)
            
            # Espelha se necessário
            if not self.animations["left"] and self.animations["right"]:
                for frame in self.animations["right"]:
                    self.animations["left"].append(pygame.transform.flip(frame, True, False))
            
            if not self.animations["right"] and self.animations["left"]:
                for frame in self.animations["left"]:
                    self.animations["right"].append(pygame.transform.flip(frame, True, False))
            
            if not self.animations["right"] and not self.animations["left"]:
                raise Exception("Nenhum sprite de inimigo")
                
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            fallback = pygame.Surface((40, 40))
            fallback.fill("red")
            self.animations["left"] = [fallback]
            self.animations["right"] = [fallback]
    
    def animate(self, dt):
        """Atualiza animação"""
        self.frame_index += self.animation_speed * dt
        
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0
        
        self.image = self.animations[self.current_animation][int(self.frame_index)]
    
    def get_animation_direction(self):
        """Retorna direção baseado no movimento horizontal"""
        if self.direction.x > 0:
            return "right"
        elif self.direction.x < 0:
            return "left"
        else:
            return self.current_animation
    
    def get_direction(self):
        enemy_pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.player.rect.center)
        
        if enemy_pos.distance_to(player_pos) > 0:
            self.direction = (player_pos - enemy_pos).normalize()
        else:
            self.direction = pygame.Vector2()
    
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        
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
        
        # Atualiza animação
        if self.direction.x != 0:
            self.current_animation = self.get_animation_direction()
        
        self.animate(dt)
