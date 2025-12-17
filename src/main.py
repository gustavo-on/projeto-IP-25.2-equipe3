import pygame
import os

from random import randint
from pytmx.util_pygame import load_pygame
from player import Player
from allsprites import CameraGroups
from sprite import Tile
from collision import CollisionSprite, Bullet
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
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Cria o player
        self.player_size = 50
        self.player = Player(500, 300, size=50, groups=self.all_sprites, collision_sprites=self.collision_sprites)
        
        # Cria a mira
        try:
            mira_path = os.path.join(BASE_DIR, "..", "assets", "images", "mira.png")
            self.mira = Crosshair(mira_path)
        except:
            print("Imagem da mira não encontrada, usando mira padrão.")
        
        # Carrega o mapa e configura o mundo
        self.setup()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 200
        self.load_images()

        self.show_attributes = False
        self.ui_font = pygame.font.Font(None, 30)
    
    def load_images(self):
        self.bullet_surf = pygame.Surface((10, 10))
        self.bullet_surf.fill("red")
    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(self.player.rect.center)
            player_screen_pos = player_pos + self.all_sprites.offset

            direction = (mouse_pos - player_screen_pos).normalize()

            Bullet(surf=self.bullet_surf, pos=self.player.rect.center, direction=direction, groups=self.all_sprites)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() 
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):
        # Carrega o mapa TMX e cria todos os sprites do mundo
        map_path = os.path.join(BASE_DIR, "..", "data", "maps", "world.tmx")
        
        if not os.path.exists(map_path):
            print(f"ERRO: Mapa não encontrado em {map_path}")
            return
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

    def draw_attribute_menu(self):
        # 1. Configurações da Janela
        bg_color = (40, 40, 40)
        border_color = "white"
        text_color = "white"
        padding = 20
        width, height = 300, 200
        
        # Centraliza a janela
        x = (self.window_width - width) // 2
        y = (self.window_height - height) // 2
        menu_rect = pygame.Rect(x, y, width, height)

        # 2. Desenha fundo e borda
        pygame.draw.rect(self.display_surface, bg_color, menu_rect)
        pygame.draw.rect(self.display_surface, border_color, menu_rect, 3)

        # 3. Textos (Atualizado para Vida Máxima)
        title_surf = self.ui_font.render("Atributos", True, "yellow")
        
        attack_surf = self.ui_font.render(f"Attack: {self.player.damage}", True, text_color)
        
        # --- MUDANÇA AQUI ---
        # Mostra a Vida Máxima (self.player.health)
        health_surf = self.ui_font.render(f"Max Health: {self.player.health}", True, text_color)
        
        range_surf = self.ui_font.render(f"Range: {self.player.range_size}", True, text_color)

        # 4. Posiciona e desenha
        title_rect = title_surf.get_rect(midtop=(menu_rect.centerx, menu_rect.top + padding))
        self.display_surface.blit(title_surf, title_rect)

        self.display_surface.blit(attack_surf, (menu_rect.left + padding, title_rect.bottom + 20))
        self.display_surface.blit(health_surf, (menu_rect.left + padding, title_rect.bottom + 50))
        self.display_surface.blit(range_surf, (menu_rect.left + padding, title_rect.bottom + 80))

    def run(self):
        #Loop principal 
        while self.running:
            # Calcula delta time
            dt = self.clock.tick(60) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.show_attributes = not self.show_attributes
            
            if not self.show_attributes:
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.mira.update()

                hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
                for enemy in self.enemy_sprites:
                    if self.player.rect.colliderect(enemy.rect):
                        self.player.take_damage(enemy.damage)
                
                hits = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)
                for bullet, enemies_hit in hits.items():
                    for enemy in enemies_hit:
                        enemy.take_damage(self.player.damage) 


            self.all_sprites.update(dt)
            # RENDERIZAÇÃO 
            self.display_surface.fill("black")  
            
            # Desenha todos os sprites do mapa com câmera centralizada no player
            self.all_sprites.draw(self.player.rect.center)
            self.mira.draw(self.display_surface)

            if self.show_attributes:
                overlay = pygame.Surface((self.window_width, self.window_height))
                overlay.set_alpha(128)
                overlay.fill((0,0,0))
                self.display_surface.blit(overlay, (0,0))
                
                self.draw_attribute_menu()

            # Desenha o player aplicando o offset da câmera (para acompanhar o mapa)
            player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
            player_screen_rect = pygame.Rect(player_screen_pos, (self.player.size, self.player.size))
            pygame.draw.rect(self.display_surface, "blue", player_screen_rect)

            pygame.display.flip()
            
        pygame.quit()
    
    

if __name__ == "__main__":
    game = Game()
    game.run()