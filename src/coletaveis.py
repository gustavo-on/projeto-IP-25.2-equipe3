import pygame
from random import uniform

class XP(pygame.sprite.Sprite):
    """
    Orb de XP que dropa quando um inimigo morre.
    """
    def __init__(self, pos, xp_value, groups, player):
        super().__init__(groups)
        self.player = player
        self.xp_value = xp_value
        
        # Visual: círculo azul brilhante
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 150, 255), (8, 8), 8)  # Azul externo
        pygame.draw.circle(self.image, (100, 200, 255), (8, 8), 5)  # Centro claro
        
        # Posição com pequeno offset aleatório (dispersão)
        self.rect = self.image.get_rect(center=pos)
        offset_x = uniform(-20, 20)
        offset_y = uniform(-20, 20)
        self.rect.x += offset_x
        self.rect.y += offset_y
        
        # Física para movimento
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2(offset_x * 3, offset_y * 3)  # Impulso inicial
        self.friction = 0.9
        
        # Sistema de atração magnética
        self.attraction_range = 150  # Distância que começa a atrair
        self.attraction_speed = 300
        self.is_attracted = False
    
    def check_attraction(self):
        """Verifica se deve ser atraído pelo player"""
        # ✅ PROTEÇÃO: Verifica se player existe e tem rect
        if not self.player or not hasattr(self.player, 'rect'):
            return
        
        try:
            player_pos = pygame.Vector2(self.player.rect.center)
            distance = self.pos.distance_to(player_pos)
            
            if distance < self.attraction_range:
                self.is_attracted = True
        except (AttributeError, TypeError):
            # Se houver erro ao acessar player, apenas ignora
            pass
    
    def move_towards_player(self, dt):
        """Move em direção ao player quando atraído"""
        # ✅ PROTEÇÃO: Verifica se player existe
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
                # Se houver erro, apenas mantém velocidade atual
                pass
    
    def update(self, dt):
        """Atualiza física e movimento"""
        # Verifica se deve ser atraído
        self.check_attraction()
        
        # Move em direção ao player ou aplica fricção
        if self.is_attracted:
            self.move_towards_player(dt)
        else:
            self.velocity *= self.friction
        
        # Atualiza posição
        self.pos += self.velocity * dt
        self.rect.center = self.pos
    
    def collect(self):
        """Retorna o valor de XP ao ser coletado"""
        return self.xp_value