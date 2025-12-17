import pygame
import os

from random import randint, choice
from pytmx.util_pygame import load_pygame
from player import Player
from allsprites import CameraGroups
from sprite import Tile
from collision import CollisionSprite, Bullet
from aim import Crosshair
from enemies import Enemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constante que define o tamanho de cada tile do mapa em pixels
TILE_SIZE = 64

class Game:
    def __init__(self):
        # Inicializa todos os módulos do Pygame
        pygame.init()

        self.xp = pygame.Surface((20, 20))
        self.xp.fill("blue")
        
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

        # ✅ CORREÇÃO 1: Inicializa spawn_positions
        self.spawn_positions = []

        # Cria o player
        self.player_size = 50
        self.player = Player(500, 300, size=50, groups=self.all_sprites, collision_sprites=self.collision_sprites)
        
        # Cria a mira
        try:
            mira_path = os.path.join(BASE_DIR, "..", "assets", "images", "mira.png")
            self.mira = Crosshair(mira_path)
        except:
            print("Imagem da mira não encontrada, usando mira padrão.")
            self.mira = None
        
        # Carrega o mapa e configura o mundo
        self.setup()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 200
        self.load_images()

        self.show_attributes = False
        self.ui_font = pygame.font.Font(None, 30)

        # ✅ CORREÇÃO 2: Cria evento de spawn de inimigos
        self.enemy_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_event, 2000)  # Spawn a cada 2 segundos
    
    def load_images(self):
        self.bullet_surf = pygame.Surface((10, 10))
        self.bullet_surf.fill("red")
    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(self.player.rect.center)
            player_screen_pos = player_pos + self.all_sprites.offset

            direction = (mouse_pos - player_screen_pos).normalize()

            Bullet(surf=self.bullet_surf, pos=self.player.rect.center, direction=direction, groups=(self.all_sprites, self.bullet_sprites))
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
        
        # Carrega entidades (player spawn e enemy spawns)
        player_spawned = False
        for obj in self.map.get_layer_by_name("Entities"):
            if obj.name == "PLayer":  # Nota: typo no nome da camada
                self.player.rect.x = obj.x
                self.player.rect.y = obj.y
                player_spawned = True
                print(f"Player spawned at ({obj.x}, {obj.y})")
            else:
                self.spawn_positions.append((obj.x, obj.y))
        
        # Se o player não foi posicionado, coloca no centro do mapa
        if not player_spawned:
            map_width = self.map.width * TILE_SIZE
            map_height = self.map.height * TILE_SIZE
            self.player.rect.x = map_width // 2
            self.player.rect.y = map_height // 2
            print(f"Player spawned at center: ({self.player.rect.x}, {self.player.rect.y})")
        
        # Define posições de spawn padrão se não houver no mapa
        if not self.spawn_positions:
            map_width = self.map.width * TILE_SIZE
            map_height = self.map.height * TILE_SIZE
            self.spawn_positions = [
                (100, 100),
                (map_width - 100, 100),
                (100, map_height - 100),
                (map_width - 100, map_height - 100)
            ]

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

        # 3. Textos
        title_surf = self.ui_font.render("Atributos", True, "yellow")
        attack_surf = self.ui_font.render(f"Attack: {self.player.damage}", True, text_color)
        health_surf = self.ui_font.render(f"Max Health: {self.player.health}", True, text_color)
        range_surf = self.ui_font.render(f"Range: {self.player.range_size}", True, text_color)

        # 4. Posiciona e desenha
        title_rect = title_surf.get_rect(midtop=(menu_rect.centerx, menu_rect.top + padding))
        self.display_surface.blit(title_surf, title_rect)

        self.display_surface.blit(attack_surf, (menu_rect.left + padding, title_rect.bottom + 20))
        self.display_surface.blit(health_surf, (menu_rect.left + padding, title_rect.bottom + 50))
        self.display_surface.blit(range_surf, (menu_rect.left + padding, title_rect.bottom + 80))
    
    def bullet_collision(self):
        # Verifica colisão entre balas e inimigos usando sprite groups
        hits = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.health -= self.player.damage
                if enemy.health <= 0:
                    enemy.kill()
                    
        
        # Verifica colisão com paredes
        for bullet in self.bullet_sprites:
            for sprite in self.collision_sprites:
                if bullet.rect.colliderect(sprite.rect):
                    bullet.kill()
                    break

    def run(self):
        # ✅ CORREÇÃO 3: Loop principal organizado
        while self.running:
            # Calcula delta time
            dt = self.clock.tick(60) / 1000
            
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Toggle menu de atributos
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.show_attributes = not self.show_attributes
                
                # Spawn de inimigos
                if event.type == self.enemy_event:
                    if self.spawn_positions:
                        Enemy(
                            pos=choice(self.spawn_positions), 
                            frames=None, 
                            groups=(self.all_sprites, self.enemy_sprites), 
                            player=self.player,
                            collision_sprites=self.collision_sprites
                        )

            # Atualização apenas se não estiver no menu
            if not self.show_attributes:
                self.gun_timer()
                self.input()
                if self.mira:
                    self.mira.update()
                
                # Atualiza todos os sprites
                self.all_sprites.update(dt)
                
                # Verifica colisões
                self.bullet_collision()
                
                # Dano de inimigos no player
                for enemy in self.enemy_sprites:
                    if self.player.rect.colliderect(enemy.rect):
                        if hasattr(self.player, 'take_damage'):
                            self.player.take_damage(enemy.damage if hasattr(enemy, 'damage') else 1)
                        else:
                            self.player.current_health -= (enemy.damage if hasattr(enemy, 'damage') else 1)
                            if self.player.current_health <= 0:
                                if hasattr(self.player, 'die'):
                                    self.player.die()

            # RENDERIZAÇÃO 
            self.display_surface.fill("black")  
            
            # Desenha todos os sprites do mapa com câmera centralizada no player
            self.all_sprites.draw(self.player.rect.center)
            
            # Desenha o player manualmente (aplicando offset da câmera)
            player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
            self.display_surface.blit(self.player.image, player_screen_pos)
            
            # Desenha a mira por cima de tudo
            if self.mira:
                self.mira.draw(self.display_surface)

            # Se menu estiver ativo, desenha overlay e menu
            if self.show_attributes:
                overlay = pygame.Surface((self.window_width, self.window_height))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.display_surface.blit(overlay, (0, 0))
                self.draw_attribute_menu()

            # Atualiza a tela
            pygame.display.flip()
        
        # ✅ CORREÇÃO 4: pygame.quit() FORA do loop
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()