import pygame

class Crosshair:
    # Mira que segue o cursor do mouse
    def __init__(self, image_path, size=(50, 50)):
        # Carrega e redimensiona a imagem da mira
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        
        # Esconde o cursor padrão do sistema
        pygame.mouse.set_visible(False)
    
    def update(self):
        # mira seguir o mouse
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):
        # mira na tela.
        screen.blit(self.image, self.rect.topleft)