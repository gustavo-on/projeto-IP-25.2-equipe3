import pygame
from random import uniform

class XP(pygame.sprite.Sprite):
    """Orb de XP que dropa quando um inimigo morre"""
    def __init__(self, pos, xp_value, groups, player):
        super().__init__(groups)
        self.player = player
        self.xp_value = xp_value
        
        # Visual: círculo azul brilhante
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 150, 255), (8, 8), 8)
        pygame.draw.circle(self.image, (100, 200, 255), (8, 8), 5)
        
        # Posição com pequeno offset aleatório
        self.rect = self.image.get_rect(center=pos)
        offset_x = uniform(-20, 20)
        offset_y = uniform(-20, 20)
        self.rect.x += offset_x
        self.rect.y += offset_y
        
        # Física para movimento
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2(offset_x * 3, offset_y * 3)
        self.friction = 0.9
        
        # Sistema de atração magnética
        self.attraction_range = 150
        self.attraction_speed = 300
        self.is_attracted = False
    
    def check_attraction(self):
        """Verifica se deve ser atraído pelo player"""
        if not self.player or not hasattr(self.player, 'rect'):
            return
        
        try:
            player_pos = pygame.Vector2(self.player.rect.center)
            distance = self.pos.distance_to(player_pos)
            
            if distance < self.attraction_range:
                self.is_attracted = True
        except (AttributeError, TypeError):
            pass
    
    def move_towards_player(self, dt):
        """Move em direção ao player quando atraído"""
        if not self.player or not hasattr(self.player, 'rect'):
            return
        
        if self.is_attracted:
            try:
                player_pos = pygame.Vector2(self.player.rect.center)
                direction = (player_pos - self.pos)
                
                if direction.length() > 0:
                    direction = direction.normalize()
                    self.velocity = direction * self.attraction_speed
            except (AttributeError, TypeError):
                pass
    
    def update(self, dt):
        """Atualiza física e movimento"""
        self.check_attraction()
        
        if self.is_attracted:
            self.move_towards_player(dt)
        else:
            self.velocity *= self.friction
        
        self.pos += self.velocity * dt
        self.rect.center = self.pos
    
    def collect(self):
        """Retorna o valor de XP ao ser coletado"""
        return self.xp_value


class Coin(pygame.sprite.Sprite):
    """Moeda coletável que spawna aleatoriamente no mapa"""
    def __init__(self, pos, value, groups):
        super().__init__(groups)
        
        # Visual da moeda (círculo amarelo com borda)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (12, 12), 12)  # Ouro
        pygame.draw.circle(self.image, (255, 255, 100), (12, 12), 12, 3)  # Borda brilhante
        pygame.draw.circle(self.image, (200, 160, 0), (12, 12), 7)  # Centro escuro
        
        self.rect = self.image.get_rect(center=pos)
        self.value = value
        
        # Animação de flutuação
        self.float_offset = 0
        self.float_speed = 3
        self.original_y = pos[1]
    
    def update(self, dt):
        """Faz a moeda flutuar suavemente"""
        self.float_offset += self.float_speed * dt
        # Movimento de seno para flutuação suave
        self.rect.centery = self.original_y + int(5 * pygame.math.Vector2(0, 1).rotate(self.float_offset * 100).y)