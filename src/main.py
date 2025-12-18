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
        
        # ### NOVO: Variável de estado do jogo
        self.game_over = False
        
        # Grupos de sprites
        self.all_sprites = CameraGroups()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

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
        self.game_over_font = pygame.font.Font(None, 80)

        # Timer de spawn
        self.enemy_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_event, 2000)
    
    def load_images(self):
        self.bullet_surf = pygame.Surface((10, 10))
        self.bullet_surf.fill("red")
    
    def input(self):
        # ### SÓ ATIRA SE NÃO FOR GAME OVER
        if pygame.mouse.get_pressed()[0] and self.can_shoot and not self.game_over:
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
        map_path = os.path.join(BASE_DIR, "..", "data", "maps", "world.tmx")
        
        if not os.path.exists(map_path):
            print(f"ERRO: Mapa não encontrado em {map_path}")
            return
        
        self.map = load_pygame(map_path)
        
        # Tiles chão
        for x, y, image in self.map.get_layer_by_name("Ground").tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        # Objetos
        for obj in self.map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        # Colisões invisíveis
        for obj in self.map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        # Entidades
        player_spawned = False
        try:
            # Tente verificar se o nome da layer no Tiled é "Entities" ou "PLayer"
            for obj in self.map.get_layer_by_name("Entities"):
                if obj.name == "PLayer" or obj.name == "Player":
                    self.player.rect.x = obj.x
                    self.player.rect.y = obj.y
                    player_spawned = True
                else:
                    self.spawn_positions.append((obj.x, obj.y))
        except Exception as e:
            print(f"Erro ao carregar layer Entities: {e}")

        if not player_spawned:
            self.player.rect.center = (600, 400)
        
        if not self.spawn_positions:
           self.spawn_positions = [(100, 100), (1000, 100)]

        # ### IMPORTANTE: Salva onde o player começou para usar no reset
        self.player_start_pos = self.player.rect.center

    def draw_attribute_menu(self):
        bg_color = (40, 40, 40)
        border_color = "white"
        text_color = "white"
        padding = 20
        width, height = 300, 200
        
        x = (self.window_width - width) // 2
        y = (self.window_height - height) // 2
        menu_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.display_surface, bg_color, menu_rect)
        pygame.draw.rect(self.display_surface, border_color, menu_rect, 3)

        title_surf = self.ui_font.render("Atributos", True, "yellow")
        attack_surf = self.ui_font.render(f"Attack: {self.player.damage}", True, text_color)
        health_surf = self.ui_font.render(f"Health: {self.player.current_health}/{self.player.health}", True, text_color)
        range_surf = self.ui_font.render(f"Range: {self.player.range_size}", True, text_color)

        title_rect = title_surf.get_rect(midtop=(menu_rect.centerx, menu_rect.top + padding))
        self.display_surface.blit(title_surf, title_rect)

        self.display_surface.blit(attack_surf, (menu_rect.left + padding, title_rect.bottom + 20))
        self.display_surface.blit(health_surf, (menu_rect.left + padding, title_rect.bottom + 50))
        self.display_surface.blit(range_surf, (menu_rect.left + padding, title_rect.bottom + 80))
    
    def draw_game_over_screen(self):
        # Fundo escuro transparente
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))

        # Texto GAME OVER
        game_over_surf = self.game_over_font.render("GAME OVER", True, "red")
        game_over_rect = game_over_surf.get_rect(center=(self.window_width/2, self.window_height/2 - 50))
        self.display_surface.blit(game_over_surf, game_over_rect)

        # Texto reiniciar
        restart_surf = self.ui_font.render("Pressione R para reiniciar", True, "white")
        restart_rect = restart_surf.get_rect(center=(self.window_width/2, self.window_height/2 + 20))
        self.display_surface.blit(restart_surf, restart_rect)
    
    def bullet_collision(self):
        hits = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.health -= self.player.damage
                if enemy.health <= 0:
                    enemy.die() # Chama o die() do inimigo que dropa XP
                    
        for bullet in self.bullet_sprites:
            for sprite in self.collision_sprites:
                if bullet.rect.colliderect(sprite.rect):
                    bullet.kill()
                    break

    def reset_game(self):
        # Limpa grupos
        self.enemy_sprites.empty()
        self.bullet_sprites.empty()
        
        # Limpa sprites da tela (Inimigos e balas)
        for sprite in self.all_sprites:
            if isinstance(sprite, (Enemy, Bullet)):
                sprite.kill()
        
        # Reseta Player
        self.player.health = 10
        self.player.current_health = 10
        self.player.rect.center = self.player_start_pos

        self.game_over = False

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # ### CHECK DE RESET (R)
                if self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()
                
                # Menu de atributos
                if not self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.show_attributes = not self.show_attributes
                
                # Spawn de inimigos (SÓ SE NÃO FOR GAME OVER)
                if event.type == self.enemy_event and not self.game_over:
                    if self.spawn_positions:
                        Enemy(
                            pos=choice(self.spawn_positions), 
                            frames=None, 
                            groups=(self.all_sprites, self.enemy_sprites), 
                            player=self.player,
                            collision_sprites=self.collision_sprites
                        )

            # ### ATUALIZAÇÃO DO JOGO
            # Só roda a lógica se não for Game Over
            if not self.game_over:
                if not self.show_attributes:
                    self.gun_timer()
                    self.input()
                    if self.mira:
                        self.mira.update()
                    
                    self.all_sprites.update(dt)
                    
                    self.bullet_collision()
                    
                    # Dano Inimigo -> Player
                    for enemy in self.enemy_sprites:
                        if self.player.rect.colliderect(enemy.rect):
                            if hasattr(self.player, 'take_damage'):
                                self.player.take_damage(enemy.damage if hasattr(enemy, 'damage') else 1)
                            else:
                                self.player.current_health -= 1
                            
                            # Empurrão (Knockback) para não tomar dano infinito instantâneo
                            vec = pygame.Vector2(self.player.rect.center) - pygame.Vector2(enemy.rect.center)
                            if vec.length() > 0:
                                self.player.rect.center += vec.normalize() * 5

                            # ### AQUI É O PULO DO GATO:
                            if self.player.current_health <= 0:
                                self.game_over = True
                                print("GAME OVER! A tela deve aparecer agora.")

            # ### RENDERIZAÇÃO
            self.display_surface.fill("black")  
            
            self.all_sprites.draw(self.player.rect.center)
            
            # Desenha player se estiver vivo (ou pode desenhar sempre)
            if self.player.current_health > 0:
                player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
                self.display_surface.blit(self.player.image, player_screen_pos)
            
            if self.mira and not self.game_over:
                self.mira.draw(self.display_surface)

            if self.show_attributes:
                overlay = pygame.Surface((self.window_width, self.window_height))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.display_surface.blit(overlay, (0, 0))
                self.draw_attribute_menu()
            
            # ### DESENHA O GAME OVER
            if self.game_over:
                self.draw_game_over_screen()

            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()