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
from coletaveis import XP, Coin, Banana

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILE_SIZE = 64

class Game:
    def __init__(self):
        pygame.init()
        
        self.window_width = 1200
        self.window_height = 800
        
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Apenas Comece")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Grupos de sprites
        self.all_sprites = CameraGroups()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.banana_sprites = pygame.sprite.Group()

        self.spawn_positions = []
        self.score = 0

        # Cria o player
        self.player_size = 50
        self.player = Player(500, 300, size=50, groups=self.all_sprites, collision_sprites=self.collision_sprites)
        
        # Cria a mira
        try:
            mira_path = os.path.join(BASE_DIR, "..", "assets", "images", "mira.png")
            self.mira = Crosshair(mira_path)
        except:
            print("Imagem da mira não encontrada.")
            self.mira = None
        
        self.setup()
        self.load_images()

        # Configurações de combate
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 200
        
        # Sistema de invencibilidade
        self.player_invincible = False
        self.invincible_duration = 500
        self.last_damage_time = 0

        # UI
        self.show_attributes = False
        self.ui_font = pygame.font.Font(None, 30)
        self.game_over_font = pygame.font.Font(None, 80)
        self.hud_font = pygame.font.Font(None, 40)
        
        # Mensagens temporárias
        self.temp_message = ""
        self.temp_message_time = 0
        self.temp_message_duration = 2000

        # Timers de spawn
        self.enemy_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_event, 2000)
        
        self.coin_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.coin_event, 3000)
        
        self.banana_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.banana_event, 5000)  # Banana spawna a cada 5 segundos
    
    def load_images(self):
        self.bullet_surf = pygame.Surface((10, 10))
        self.bullet_surf.fill("red")
    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot and not self.game_over:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(self.player.rect.center)
            player_screen_pos = player_pos + self.all_sprites.offset
            direction = (mouse_pos - player_screen_pos).normalize()

            Bullet(
                surf=self.bullet_surf, 
                pos=self.player.rect.center, 
                direction=direction, 
                groups=(self.all_sprites, self.bullet_sprites)
            )
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    def invincibility_timer(self):
        if self.player_invincible:
            if pygame.time.get_ticks() - self.last_damage_time >= self.invincible_duration:
                self.player_invincible = False

    def setup(self):
        map_path = os.path.join(BASE_DIR, "..", "data", "maps", "world.tmx")
        
        if not os.path.exists(map_path):
            print(f"ERRO: Mapa não encontrado em {map_path}")
            return
        
        self.map = load_pygame(map_path)
        
        # Carrega camadas do mapa
        for x, y, image in self.map.get_layer_by_name("Ground").tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in self.map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in self.map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        
        # Carrega entidades
        player_spawned = False
        try:
            for obj in self.map.get_layer_by_name("Entities"):
                if obj.name in ("PLayer", "Player"):
                    self.player.rect.x = obj.x
                    self.player.rect.y = obj.y
                    player_spawned = True
                else:
                    self.spawn_positions.append((obj.x, obj.y))
        except Exception as e:
            print(f"Erro ao carregar Entities: {e}")

        if not player_spawned:
            self.player.rect.center = (600, 400)
        
        if not self.spawn_positions:
           self.spawn_positions = [(100, 100), (1000, 100)]

        self.player_start_pos = self.player.rect.center
        self.map_width = self.map.width * TILE_SIZE
        self.map_height = self.map.height * TILE_SIZE

    def spawn_coin(self):
        """Spawna uma moeda em posição aleatória"""
        x = randint(100, self.map_width - 100)
        y = randint(100, self.map_height - 100)
        coin_value = randint(1, 5)
        Coin(pos=(x, y), value=coin_value, groups=(self.all_sprites, self.coin_sprites))

    def spawn_banana(self):
        """Spawna uma banana em posição aleatória"""
        x = randint(100, self.map_width - 100)
        y = randint(100, self.map_height - 100)
        heal_amount = randint(2, 4)  # Cura entre 2-4 de vida
        Banana(pos=(x, y), heal_amount=heal_amount, groups=(self.all_sprites, self.banana_sprites))

    def collect_coins(self):
        """Verifica e coleta moedas"""
        for coin in self.coin_sprites:
            if self.player.rect.colliderect(coin.rect):
                self.score += coin.value
                coin.kill()
                self.show_temp_message(f" +{coin.value} moedas!", (255, 215, 0))
                print(f"+{coin.value} moedas! Total: {self.score}")

    def collect_bananas(self):
        """Verifica e coleta bananas"""
        for banana in self.banana_sprites:
            if self.player.rect.colliderect(banana.rect):
                # Cura o player (sem ultrapassar vida máxima)
                heal_amount = banana.heal_amount
                old_health = self.player.current_health
                self.player.current_health = min(self.player.current_health + heal_amount, self.player.health)
                actual_heal = self.player.current_health - old_health
                
                banana.kill()
                
                if actual_heal > 0:
                    self.show_temp_message(f"🍌 +{actual_heal} HP!", (255, 255, 0))
                    print(f"🍌 Banana coletada! +{actual_heal} HP ({self.player.current_health}/{self.player.health})")
                else:
                    self.show_temp_message("🍌 Vida cheia!", (255, 255, 255))
                    print("🍌 Banana coletada, mas vida já está cheia!")

    def show_temp_message(self, message, color=(255, 255, 255)):
        """Mostra uma mensagem temporária na tela"""
        self.temp_message = message
        self.temp_message_color = color
        self.temp_message_time = pygame.time.get_ticks()

    def draw_temp_message(self):
        """Desenha mensagem temporária se houver uma ativa"""
        if self.temp_message and pygame.time.get_ticks() - self.temp_message_time < self.temp_message_duration:
            msg_surf = self.hud_font.render(self.temp_message, True, self.temp_message_color)
            msg_rect = msg_surf.get_rect(center=(self.window_width // 2, 100))
            
            # Sombra
            shadow_surf = self.hud_font.render(self.temp_message, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(self.window_width // 2 + 2, 102))
            self.display_surface.blit(shadow_surf, shadow_rect)
            
            self.display_surface.blit(msg_surf, msg_rect)

    def draw_hud(self):
        """Desenha HUD com informações do jogador"""
        # Pontuação
        hud_bg = pygame.Surface((220, 50))
        hud_bg.set_alpha(150)
        hud_bg.fill((0, 0, 0))
        self.display_surface.blit(hud_bg, (10, 10))
        
        score_text = self.hud_font.render(f"{self.score}", True, "gold")
        self.display_surface.blit(score_text, (20, 15))
        
        # XP e Level
        xp_bg = pygame.Surface((220, 60))
        xp_bg.set_alpha(150)
        xp_bg.fill((0, 0, 0))
        self.display_surface.blit(xp_bg, (10, 70))
        
        level_text = self.ui_font.render(f"Level: {self.player.level}", True, "cyan")
        self.display_surface.blit(level_text, (20, 75))
        
        xp_text = self.ui_font.render(f"XP: {self.player.current_xp}/{self.player.next_level_up}", True, "white")
        self.display_surface.blit(xp_text, (20, 100))
        
        # Vida com barra visual
        health_bg = pygame.Surface((220, 50))
        health_bg.set_alpha(150)
        health_bg.fill((0, 0, 0))
        self.display_surface.blit(health_bg, (10, 140))
        
        # Barra de vida
        bar_width = 180
        bar_height = 20
        bar_x = 20
        bar_y = 150
        
        # Fundo da barra (vermelho escuro)
        pygame.draw.rect(self.display_surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de vida atual (verde/amarelo/vermelho baseado na porcentagem)
        health_percent = self.player.current_health / self.player.health
        current_bar_width = int(bar_width * health_percent)
        
        if health_percent > 0.6:
            bar_color = (0, 200, 0)  # Verde
        elif health_percent > 0.3:
            bar_color = (255, 200, 0)  # Amarelo
        else:
            bar_color = (255, 0, 0)  # Vermelho
        
        pygame.draw.rect(self.display_surface, bar_color, (bar_x, bar_y, current_bar_width, bar_height))
        
        # Borda da barra
        pygame.draw.rect(self.display_surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Texto da vida
        health_text = self.ui_font.render(f"{self.player.current_health}/{self.player.health}", True, "white")
        self.display_surface.blit(health_text, (bar_x + bar_width // 2 - health_text.get_width() // 2, bar_y - 2))

    def draw_attribute_menu(self):
        """Menu de atributos do jogador"""
        bg_color = (40, 40, 40)
        border_color = "white"
        text_color = "white"
        padding = 20
        width, height = 350, 250
        
        x = (self.window_width - width) // 2
        y = (self.window_height - height) // 2
        menu_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.display_surface, bg_color, menu_rect)
        pygame.draw.rect(self.display_surface, border_color, menu_rect, 3)

        title_surf = self.ui_font.render("=== ATRIBUTOS ===", True, "yellow")
        title_rect = title_surf.get_rect(midtop=(menu_rect.centerx, menu_rect.top + padding))
        self.display_surface.blit(title_surf, title_rect)

        y_offset = title_rect.bottom + 20
        attributes = [
            f"Level: {self.player.level}",
            f"Attack: {self.player.damage}",
            f"Health: {self.player.current_health}/{self.player.health}",
            f"Range: {self.player.range_size}",
            f"XP: {self.player.current_xp}/{self.player.next_level_up}",
            f"Moedas: {self.score}"
        ]
        
        for attr in attributes:
            surf = self.ui_font.render(attr, True, text_color)
            self.display_surface.blit(surf, (menu_rect.left + padding, y_offset))
            y_offset += 30
    
    def draw_game_over_screen(self):
        """Tela de Game Over"""
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))

        game_over_surf = self.game_over_font.render("GAME OVER", True, "red")
        game_over_rect = game_over_surf.get_rect(center=(self.window_width/2, self.window_height/2 - 80))
        self.display_surface.blit(game_over_surf, game_over_rect)
        
        # Estatísticas finais
        score_surf = self.ui_font.render(f"Moedas: {self.score}", True, "gold")
        score_rect = score_surf.get_rect(center=(self.window_width/2, self.window_height/2 - 20))
        self.display_surface.blit(score_surf, score_rect)
        
        level_surf = self.ui_font.render(f"Level: {self.player.level}", True, "cyan")
        level_rect = level_surf.get_rect(center=(self.window_width/2, self.window_height/2 + 10))
        self.display_surface.blit(level_surf, level_rect)

        restart_surf = self.ui_font.render("Pressione R para reiniciar", True, "white")
        restart_rect = restart_surf.get_rect(center=(self.window_width/2, self.window_height/2 + 60))
        self.display_surface.blit(restart_surf, restart_rect)
    
    def bullet_collision(self):
        """Verifica colisões de balas"""
        hits = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.health -= self.player.damage
                if enemy.health <= 0:
                    self.drop_xp(enemy.rect.center, xp_amount=5)
                    enemy.kill()
                    
        for bullet in self.bullet_sprites:
            for sprite in self.collision_sprites:
                if bullet.rect.colliderect(sprite.rect):
                    bullet.kill()
                    break
    
    def drop_xp(self, position, xp_amount=1):
        """Dropa XP na posição especificada"""
        XP(
            pos=position,
            xp_value=xp_amount,
            groups=(self.all_sprites, self.collectible_sprites),
            player=self.player
        )
    
    def collect_items(self):
        """Coleta XP"""
        if self.player.current_health <= 0:
            return
        
        hits = pygame.sprite.spritecollide(self.player, self.collectible_sprites, True)
        for item in hits:
            if isinstance(item, XP):
                try:
                    xp_gained = item.collect()
                    if self.player.level < 5:
                        self.player.current_xp += xp_gained
                        print(f"✨ +{xp_gained} XP! ({self.player.current_xp}/{self.player.next_level_up})")
                    
                    # Level up
                        if self.player.current_xp >= self.player.next_level_up:
                            self.player.level += 1
                            self.player.current_xp = 0
                            if self.player.level == 2:
                                self.player.next_level_up = 20
                            elif self.player.level == 3:
                                self.player.next_level_up = 30
                            elif self.player.level == 4:
                                self.player.next_level_up = 40
                            elif self.player.level >= 5:
                                self.player.next_level_up = 9999
                                print("Nível Máximo Alcançado")

                            self.player.damage += 1
                            self.show_temp_message(f"🎉 LEVEL {self.player.level}!", (0, 255, 255))
                            print(f"🎉 LEVEL UP! Level {self.player.level}! Dano +1")
                except Exception as e:
                    print(f"Erro ao coletar XP: {e}")

    def reset_game(self):
        """Reseta o jogo"""
        # Limpa grupos
        self.enemy_sprites.empty()
        self.bullet_sprites.empty()
        self.collectible_sprites.empty()
        self.coin_sprites.empty()
        self.banana_sprites.empty()
        
        # Remove sprites
        for sprite in list(self.all_sprites):
            if isinstance(sprite, (Enemy, Bullet, XP, Coin, Banana)):
                sprite.kill()
        
        # Reseta player
        self.player.health = 10
        self.player.current_health = 10
        self.player.current_xp = 0
        self.player.level = 1
        self.player.next_level_up = 10
        self.player.damage = 2
        self.player.rect.center = self.player_start_pos
        
        # Reseta estado
        self.player_invincible = False
        self.score = 0
        self.game_over = False
        self.temp_message = ""
        print("Jogo resetado!")

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()
                
                if not self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.show_attributes = not self.show_attributes
                
                # Spawn de inimigos
                if event.type == self.enemy_event and not self.game_over:
                    if self.spawn_positions:
                        Enemy(
                            pos=choice(self.spawn_positions), 
                            frames=None, 
                            groups=(self.all_sprites, self.enemy_sprites), 
                            player=self.player,
                            collision_sprites=self.collision_sprites
                        )
                
                # Spawn de moedas
                if event.type == self.coin_event and not self.game_over:
                    self.spawn_coin()
                
                # Spawn de bananas
                if event.type == self.banana_event and not self.game_over:
                    self.spawn_banana()

            # Atualização
            if not self.game_over and not self.show_attributes:
                self.gun_timer()
                self.invincibility_timer()
                self.input()
                if self.mira:
                    self.mira.update()
                
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.collect_items()
                self.collect_coins()
                self.collect_bananas()
                
                # Dano de inimigos
                if not self.player_invincible:
                    for enemy in self.enemy_sprites:
                        if self.player.rect.colliderect(enemy.rect):
                            damage = getattr(enemy, 'damage', 1)
                            self.player.current_health -= damage
                            
                            self.player_invincible = True
                            self.last_damage_time = pygame.time.get_ticks()
                            
                            # Knockback
                            vec = pygame.Vector2(self.player.rect.center) - pygame.Vector2(enemy.rect.center)
                            if vec.length() > 0:
                                self.player.rect.center += vec.normalize() * 10
                            
                            if self.player.current_health <= 0:
                                self.game_over = True
                                print("GAME OVER!")
                            
                            break

            # Renderização
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            
            # Desenha player com efeito de piscar quando invencível
            if self.player.current_health > 0:
                if not self.player_invincible or (pygame.time.get_ticks() // 100) % 2:
                    player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
                    self.display_surface.blit(self.player.image, player_screen_pos)
            
            if self.mira and not self.game_over:
                self.mira.draw(self.display_surface)
            
            if not self.game_over:
                self.draw_hud()
                self.draw_temp_message()

            if self.show_attributes:
                overlay = pygame.Surface((self.window_width, self.window_height))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.display_surface.blit(overlay, (0, 0))
                self.draw_attribute_menu()
            
            if self.game_over:
                self.draw_game_over_screen()

            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()