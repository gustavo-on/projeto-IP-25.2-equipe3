import pygame
import os
from random import randint
from pytmx.util_pygame import load_pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Constante que define o tamanho de cada tile do mapa em pixels
TILE_SIZE = 64

class Game:
    def __init__(self):
        # Inicializa todos os módulos do Pygame
        pygame.init()
        
        # Define dimensões da janela
        self.window_width = 1200
        self.window_height = 800
        
        # Cria a janela do jogo
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("apenas comece")
        
        # Relógio para controlar FPS e delta time
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Grupos de sprites: all_sprites para renderização, collision_sprites para física
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # Cria o player
        self.player_size = 50
        self.player = Player(500, 300, self.player_size, self.collision_sprites)
        
        # Cria a mira
        mira_path = os.path.join(BASE_DIR, "..", "assets", "imagens", "mira.png")
        self.mira = Crosshair(mira_path)
        
        # Carrega o mapa e configura o mundo
        self.setup()

    def setup(self):
        # Carrega o mapa TMX e cria todos os sprites do mundo
        map_path = os.path.join(BASE_DIR, "..", "data", "maps", "world.tmx")
        
        # Carrega o arquivo TMX usando pytmx
        self.map = load_pygame(map_path)
        
        # Carrega a camada "Ground" (chão) tiles não colidíveis
        for x, y, image in self.map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        # Carrega a camada "Objects" (objetos visíveis) com colisão
        for obj in self.map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        # Carrega a camada "Collisions" apenas hitboxes
        for obj in self.map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        # Calcula o centro do mapa e posiciona o player
        map_width = self.map.width * TILE_SIZE
        map_height = self.map.height * TILE_SIZE
        self.player.rect.center = (map_width // 2, map_height // 2)

    def run(self):
        #Loop principal 
        while self.running:
            # Calcula delta time
            dt = self.clock.tick() / 1000

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # atualizacão 
            self.mira.update()        
            self.player.input()       
            self.player.move(dt)      
            
            # RENDERIZAÇÃO 
            self.display_surface.fill("black")  
            
            # Desenha todos os sprites do mapa com câmera centralizada no player
            self.all_sprites.draw(self.player.rect.center)
            
            # Desenha o player aplicando o offset da câmera (para acompanhar o mapa)
            player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
            player_screen_rect = pygame.Rect(player_screen_pos, (self.player.size, self.player.size))
            pygame.draw.rect(self.display_surface, "blue", player_screen_rect)
            
            self.mira.draw(self.display_surface)

            pygame.display.flip()
            
        pygame.quit()


class Player:
    def __init__(self, x, y, size, collision_sprites, color="blue"):
        # Posição inicial
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        
        # Retângulo para posição e colisão 
        self.rect = pygame.Rect(x, y, size, size)


        # Vetor de direção do movimento
        self.direction = pygame.Vector2(0, 0)
        self.speed = 500  
        
        self.collision_sprites = collision_sprites
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal: D/→ (direita) ou A/← (esquerda)
        self.direction.x = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        
        # Movimento vertical: S/↓ (baixo) ou W/↑ (cima)
        self.direction.y = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        
        # Normaliza o vetor para evitar movimento mais rápido na diagonal
        self.direction = self.direction.normalize() if self.direction else self.direction       

    def move(self, dt):
        # Move no eixo X e verifica colisão horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        
        # Move no eixo Y e verifica colisão vertical
        self.rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):
        # Detecta e resolve colisões com sprites de colisão
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    # Colisão horizontal: empurra para o lado oposto
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                else:
                    # Colisão vertical: empurra para cima/baixo
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top


class Sprite(pygame.sprite.Sprite):
    # Sprite para tiles do mapa, chão
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True 


class AllSprites(pygame.sprite.Group):
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


class CollisionSprite(pygame.sprite.Sprite):
    # Sprite com colisão (objetos e paredes)
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

 
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
        # mira na tela
        screen.blit(self.image, self.rect.topleft)


if __name__ == "__main__":
    game = Game()
    game.run()