import pygame 

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
