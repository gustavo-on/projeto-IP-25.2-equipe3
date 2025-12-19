import pygame
import os
from entity import Entity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Player(Entity):
    def __init__(self, x, y, size, groups, collision_sprites, color="blue"):
        super().__init__(groups)
        
        # Carrega os sprites de animação
        self.load_animations()
        
        # Configuração inicial
        self.current_animation = "right"
        self.frame_index = 0
        self.animation_speed = 10
        
        self.image = self.animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Status
        self.health = 10
        self.current_health = 10
        self.damage = 2
        
        # Sistema de Level
        self.level = 1
        self.current_xp = 0
        self.next_level_up = 10
        self.attributes_points = 0
        
        # Movimento
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        self.speed = 300
        
        # Especial
        self.special_cooldown = 10000
        self.can_use_special = True
        self.last_special_time = 0
        self.special_damage = 10
        self.special_range = 200
    
    def load_animations(self):
        """Carrega sprites apenas para esquerda e direita"""
        self.animations = {
            "left": [],
            "right": []
        }
        
        animations_path = os.path.join(BASE_DIR, "..", "assets", "images", "player")
        
        try:
            # Carrega sprites da DIREITA
            right_path = os.path.join(animations_path, "right")
            if os.path.exists(right_path):
                files = sorted([f for f in os.listdir(right_path) if f.endswith('.png')])
                for file in files:
                    image_path = os.path.join(right_path, file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (100, 100))
                    self.animations["right"].append(image)
            
            # Carrega sprites da ESQUERDA
            left_path = os.path.join(animations_path, "left")
            if os.path.exists(left_path):
                files = sorted([f for f in os.listdir(left_path) if f.endswith('.png')])
                for file in files:
                    image_path = os.path.join(left_path, file)
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (100, 100))
                    self.animations["left"].append(image)
            
            # Verifica se carregou pelo menos uma direção
            if not self.animations["right"] and not self.animations["left"]:
                raise Exception("Nenhum sprite encontrado")
            
            # Se só tem uma direção, espelha para a outra
            if not self.animations["left"] and self.animations["right"]:
                print("⚠️ Espelhando sprites da direita para esquerda")
                for frame in self.animations["right"]:
                    self.animations["left"].append(pygame.transform.flip(frame, True, False))
            
            if not self.animations["right"] and self.animations["left"]:
                print("⚠️ Espelhando sprites da esquerda para direita")
                for frame in self.animations["left"]:
                    self.animations["right"].append(pygame.transform.flip(frame, True, False))
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar sprites: {e}")
            # Fallback: quadrado azul
            fallback = pygame.Surface((50, 50))
            fallback.fill("blue")
            self.animations["left"] = [fallback]
            self.animations["right"] = [fallback]
    
    def animate(self, dt):
        """Atualiza a animação"""
        self.frame_index += self.animation_speed * dt
        
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0
        
        self.image = self.animations[self.current_animation][int(self.frame_index)]
    
    def get_animation_direction(self):
        """Retorna 'left' ou 'right' baseado na direção horizontal"""
        if self.direction.x > 0:
            return "right"
        elif self.direction.x < 0:
            return "left"
        else:
            return self.current_animation  # Mantém a última direção se parado
    
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
    
    def update(self, dt):
        self.input()
        self.move(dt)
        
        # Atualiza animação (só muda se andar na horizontal)
        if self.direction.x != 0:
            self.current_animation = self.get_animation_direction()
        
        self.animate(dt)
