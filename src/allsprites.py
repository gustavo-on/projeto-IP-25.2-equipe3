import pygame 
import os

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