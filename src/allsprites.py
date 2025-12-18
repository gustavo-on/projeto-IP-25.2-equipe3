import pygame 
import os
from pygame.math import Vector2 as vector

class CameraGroups(pygame.sprite.Group):
    # Grupo customizado de sprites com sistema de câmera
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2() 

    def draw(self, target_pos):
        # Desenha todos os sprites com a câmera centralizada no target_pos
        # Calcula offset para centralizar a câmera no player
        self.offset.x = -target_pos[0] + self.display_surface.get_width() // 2
        self.offset.y = -target_pos[1] + self.display_surface.get_height() // 2
        
        # Desenha cada sprite aplicando o offset da câmera
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

class TelaInicial:
    def __init__(self, display_surface, window_width, window_height):
        self.display_surface = display_surface
        self.window_width = window_width
        self.window_height = window_height

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "..", "assets", "images", "Tela Inicial.jpeg")

        try:
            self.background_image = pygame.image.load(image_path)
            self.background_image = pygame.transform.scale(
                self.background_image,
                (window_width, window_height)
            )
            print(f"Tela inicial carregada: {image_path}")
        except Exception as e:
            print(f"ERRO ao carregar tela inicial: {e}")
            # Fallback: fundo preto com texto
            self.background_image = None
            self.font = pygame.font.Font(None, 60)
        
        self.active = True
    
    def handle_events(self, event):
        """Processa eventos do menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Tecla Enter
                self.active = False
                return "start_game"
            elif event.key == pygame.K_ESCAPE:  # ESC para sair
                return "quit"
        return None
    
    def update(self):
        pass

    def draw(self):
        if self.background_image:
            self.display_surface.blit(self.background_image, (0, 0))

        else:
            self.display_surface.fill((0, 0, 0))
            text = self.font.render("PRESS ENTER TO START", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.display_surface.blit(text, text_rect)

class TelaGameOver:
    def __init__(self, display_surface, window_width, window_height):
        self.display_surface = display_surface
        self.window_width = window_width
        self.window_height = window_height
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "..", "assets", "images", "TelaGameOver.jpg")
        
        try:
            self.background_image = pygame.image.load(image_path)
            self.background_image = pygame.transform.scale(
                self.background_image,
                (window_width, window_height)
            )
            print(f"✅ Tela de Game Over carregada: {image_path}")
        except Exception as e:
            print(f"❌ ERRO ao carregar tela de Game Over: {e}")
            self.background_image = None
            self.game_over_font = pygame.font.Font(None, 80)
            self.ui_font = pygame.font.Font(None, 40)
        
        self.game_over_font = pygame.font.Font(None, 80)
        self.ui_font = pygame.font.Font(None, 40)
        
        self.score = 0
        self.level = 0
    
    def set_stats(self, score, level):
        """Atualiza as estatísticas do jogo"""
        self.score = score
        self.level = level
    
    def handle_events(self, event):
        """Processa eventos do game over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "restart"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return None
    
    def update(self):
        pass
    
    def draw(self):
        """Desenha a tela de game over"""
        if self.background_image:
            self.display_surface.blit(self.background_image, (0, 0))
        else:
            # Fallback
            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.display_surface.blit(overlay, (0, 0))
            
            game_over_surf = self.game_over_font.render("GAME OVER", True, "red")
            game_over_rect = game_over_surf.get_rect(center=(self.window_width/2, self.window_height/2 - 80))
            self.display_surface.blit(game_over_surf, game_over_rect)
            
            score_surf = self.ui_font.render(f"Moedas: {self.score}", True, "gold")
            score_rect = score_surf.get_rect(center=(self.window_width/2, self.window_height/2 - 20))
            self.display_surface.blit(score_surf, score_rect)
            
            level_surf = self.ui_font.render(f"Level: {self.level}", True, "cyan")
            level_rect = level_surf.get_rect(center=(self.window_width/2, self.window_height/2 + 10))
            self.display_surface.blit(level_surf, level_rect)
            
            restart_surf = self.ui_font.render("Pressione R para reiniciar", True, "white")
            restart_rect = restart_surf.get_rect(center=(self.window_width/2, self.window_height/2 + 60))
            self.display_surface.blit(restart_surf, restart_rect)