import pygame
import os
from random import randint
from pytmx.util_pygame import load_pygame
from player import Player
from allsprites import CameraGroups
from sprite import Tile
from collision import CollisionSprite
from aim import Crosshair

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
        self.all_sprites = CameraGroups()
        self.collision_sprites = pygame.sprite.Group()

        # Cria o player
        self.player_size = 50
        self.player = Player(500, 300, self.player_size, self.collision_sprites)
        
        # Cria a mira
        mira_path = os.path.join(BASE_DIR, "..", "assets", "images", "mira.png")
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
            Tile((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
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

if __name__ == "__main__":
    game = Game()
    game.run()