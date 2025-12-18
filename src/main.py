import pygame
import os

from random import randint, choice
from pytmx.util_pygame import load_pygame
from player import Player
from allsprites import CameraGroups, TelaInicial
from sprite import Tile
from collision import CollisionSprite, Bullet, Punch
from aim import Crosshair
from enemies import Enemy
from coletaveis import XP, Coin, Banana, Rock
from button import Button
from store import Store

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILE_SIZE = 64

class Game:
    def __init__(self):
        pygame.init()
        
        self.window_width = 1200
        self.window_height = 800
        
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Apenas Comece")

        self.store = Store(self.display_surface, self.window_width, self.window_height)
        self.show_store = False
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Grupos de sprites
        self.all_sprites = CameraGroups()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.punch_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.banana_sprites = pygame.sprite.Group()
        self.rock_sprites = pygame.sprite.Group()

        self.spawn_positions = []
        self.score = 0
        
        # INVENTÁRIO DE BANANAS
        self.banana_inventory = 0
        self.banana_heal_amount = 3
        
        # INVENTÁRIO DE PEDRAS (MUNIÇÃO)
        self.rock_inventory = 3

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
        
        # Sistema de soco
        self.can_punch = True
        self.punch_time = 0
        self.punch_cooldown = 500
        
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

        # Timers de spawn, spawn rate
        self.enemy_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_event, 2000)
        
        self.coin_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.coin_event, 3000)
        
        self.banana_event = pygame.USEREVENT + 3
        pygame.time.set_timer(self.banana_event, 2000)
        
        self.rock_event = pygame.USEREVENT + 4
        pygame.time.set_timer(self.rock_event, 4000)
        
        self.attribute_points = 0
        self.upgrade_buttons = []

        pygame.mouse.set_visible(False)

        self.game_state = "menu"
        self.menu = TelaInicial(self.display_surface, self.window_width, self.window_height)
    
    def load_images(self):
        """Carrega imagens para projéteis"""
        try:
            # Tenta carregar imagem da pedra
            bullet_path = os.path.join(BASE_DIR, "..", "assets", "images", "pedra.png")
            original_bullet = pygame.image.load(bullet_path).convert_alpha()
            
            # Redimensiona a pedra (ajuste o tamanho conforme necessário)
            self.bullet_surf = pygame.transform.scale(original_bullet, (20, 20))
            
            
        except Exception as e:
            # Fallback: quadrado vermelho se não encontrar a imagem
            self.bullet_surf = pygame.Surface((10, 10))
            self.bullet_surf.fill("red")
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot and not self.game_over:
            if self.rock_inventory > 0:
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
                
                self.rock_inventory -= 1
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                
                if self.rock_inventory == 0:
                    self.show_temp_message("⚠️ Sem pedras!", (255, 150, 0))
            else:
                if not hasattr(self, '_last_no_rock_msg') or pygame.time.get_ticks() - self._last_no_rock_msg > 1000:
                    self.show_temp_message("❌ Colete pedras para atirar!", (255, 100, 100))
                    self._last_no_rock_msg = pygame.time.get_ticks()
    
    def input_punch(self):
        """Detecta clique direito para soco"""
        if pygame.mouse.get_pressed()[2] and self.can_punch and not self.game_over:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            player_pos = pygame.Vector2(self.player.rect.center)
            player_screen_pos = player_pos + self.all_sprites.offset
            direction = (mouse_pos - player_screen_pos).normalize()

            Punch(
                pos=self.player.rect.center,
                direction=direction,
                damage=self.player.damage * 2,
                groups=(self.all_sprites, self.punch_sprites)
            )
            
            self.can_punch = False
            self.punch_time = pygame.time.get_ticks()
            
    
    def use_banana(self):
        """Usa uma banana do inventário para curar"""
        if self.banana_inventory > 0 and self.player.current_health < self.player.health:
            old_health = self.player.current_health
            self.player.current_health = min(self.player.current_health + self.banana_heal_amount, self.player.health)
            actual_heal = self.player.current_health - old_health
            
            self.banana_inventory -= 1
            
            self.show_temp_message(f"🍌 Usou banana! +{actual_heal} HP", (255, 255, 0))
        
        elif self.banana_inventory <= 0:
            self.show_temp_message("❌ Sem bananas!", (255, 100, 100))
        
        elif self.player.current_health >= self.player.health:
            self.show_temp_message("💚 Vida cheia!", (100, 255, 100))
    
    def gun_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    def punch_timer(self):
        """Gerencia cooldown do soco"""
        if not self.can_punch:
            if pygame.time.get_ticks() - self.punch_time >= self.punch_cooldown:
                self.can_punch = True
    
    def invincibility_timer(self):
        if self.player_invincible:
            if pygame.time.get_ticks() - self.last_damage_time >= self.invincible_duration:
                self.player_invincible = False

    def setup(self):
        map_path = os.path.join(BASE_DIR, "..", "data", "maps", "world.tmx")
        
        if not os.path.exists(map_path):
            return
        
        self.map = load_pygame(map_path)
        
        # Carrega camadas do mapa
        for x, y, image in self.map.get_layer_by_name("Ground").tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in self.map.get_layer_by_name("Objects"):
            if obj.image is not None:
                CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
            else:
                print(f"⚠️ Objeto sem imagem ignorado em ({obj.x}, {obj.y})")
        
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
        self.map_width = 130 * TILE_SIZE
        self.map_height = 130 * TILE_SIZE

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
        heal_amount = self.banana_heal_amount
        Banana(pos=(x, y), heal_amount=heal_amount, groups=(self.all_sprites, self.banana_sprites))

    def spawn_rock(self):
        """Spawna uma pedra em posição aleatória"""
        x = randint(100, self.map_width - 100)
        y = randint(100, self.map_height - 100)
        Rock(pos=(x, y), groups=(self.all_sprites, self.rock_sprites))

    def collect_coins(self):
        """Verifica e coleta moedas"""
        for coin in self.coin_sprites:
            if self.player.rect.colliderect(coin.rect):
                self.score += coin.value
                coin.kill()
                self.show_temp_message(f"💰 +{coin.value} moedas!", (255, 215, 0))
                print(f"💰 +{coin.value} moedas! Total: {self.score}")

    def collect_bananas(self):
        """Verifica e coleta bananas para o inventário"""
        for banana in self.banana_sprites:
            if self.player.rect.colliderect(banana.rect):
                self.banana_inventory += 1
                banana.kill()
                
                self.show_temp_message(f"🍌 Banana coletada! ({self.banana_inventory})", (255, 255, 0))
                print(f"🍌 Banana coletada! Inventário: {self.banana_inventory}")

    def collect_rocks(self):
        """Verifica e coleta pedras"""
        for rock in self.rock_sprites:
            if self.player.rect.colliderect(rock.rect):
                self.rock_inventory += 1
                rock.kill()
                
                self.show_temp_message(f"🪨 Pedra coletada! ({self.rock_inventory})", (150, 150, 150))
                print(f"🪨 Pedra coletada! Inventário: {self.rock_inventory}")

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
        
        score_text = self.hud_font.render(f"💰 {self.score}", True, "gold")
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
            bar_color = (0, 200, 0)
        elif health_percent > 0.3:
            bar_color = (255, 200, 0)
        else:
            bar_color = (255, 0, 0)
        
        pygame.draw.rect(self.display_surface, bar_color, (bar_x, bar_y, current_bar_width, bar_height))
        
        # Borda da barra
        pygame.draw.rect(self.display_surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Texto da vida
        health_text = self.ui_font.render(f"{self.player.current_health}/{self.player.health}", True, "white")
        self.display_surface.blit(health_text, (bar_x + bar_width // 2 - health_text.get_width() // 2, bar_y - 2))
        
        # INVENTÁRIO DE BANANAS
        banana_bg = pygame.Surface((220, 50))
        banana_bg.set_alpha(150)
        banana_bg.fill((0, 0, 0))
        self.display_surface.blit(banana_bg, (10, 200))
        
        banana_text = self.hud_font.render(f"🍌 x{self.banana_inventory}", True, (255, 255, 0))
        self.display_surface.blit(banana_text, (20, 205))
        
        # Dica de uso
        hint_text = self.ui_font.render("(H para usar)", True, (200, 200, 200))
        self.display_surface.blit(hint_text, (120, 212))
        
        # INVENTÁRIO DE PEDRAS
        rock_bg = pygame.Surface((220, 50))
        rock_bg.set_alpha(150)
        rock_bg.fill((0, 0, 0))
        self.display_surface.blit(rock_bg, (10, 260))
        
        rock_text = self.hud_font.render(f"🪨 x{self.rock_inventory}", True, (150, 150, 150))
        self.display_surface.blit(rock_text, (20, 265))
        
        rock_hint = self.ui_font.render("(Munição)", True, (200, 200, 200))
        self.display_surface.blit(rock_hint, (120, 272))
        
        # Indicador de cooldown do soco
        if not self.can_punch:
            cooldown_percent = (pygame.time.get_ticks() - self.punch_time) / self.punch_cooldown
            cooldown_surf = pygame.Surface((80, 10))
            cooldown_surf.fill((50, 50, 50))
            pygame.draw.rect(cooldown_surf, (255, 200, 0), (0, 0, int(80 * cooldown_percent), 10))
            
            self.display_surface.blit(cooldown_surf, (self.window_width - 100, 20))
            
            cooldown_text = self.ui_font.render("👊", True, (255, 200, 0))
            self.display_surface.blit(cooldown_text, (self.window_width - 130, 10))

    def draw_attribute_menu(self):
        """Menu de atributos com sistema de pontos de skill"""
        bg_color = (40, 40, 40)
        border_color = "white"
        text_color = "white"
        padding = 20
        width, height = 450, 450
        
        x = (self.window_width - width) // 2
        y = (self.window_height - height) // 2
        menu_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.display_surface, bg_color, menu_rect)
        pygame.draw.rect(self.display_surface, border_color, menu_rect, 3)

        title_surf = self.ui_font.render("=== ATRIBUTOS ===", True, "yellow")
        title_rect = title_surf.get_rect(midtop=(menu_rect.centerx, menu_rect.top + padding))
        self.display_surface.blit(title_surf, title_rect)

        # Pontos disponíveis
        y_offset = title_rect.bottom + 15
        points_color = (0, 255, 0) if self.attribute_points > 0 else (150, 150, 150)
        points_surf = self.ui_font.render(f"Pontos Disponíveis: {self.attribute_points}", True, points_color)
        points_rect = points_surf.get_rect(centerx=menu_rect.centerx, top=y_offset)
        self.display_surface.blit(points_surf, points_rect)
        
        y_offset += 50
        
        # Limpa e recria botões
        self.upgrade_buttons = []
        button_font = pygame.font.Font(None, 26)
        
        # Configuração dos atributos
        upgrades = [
            {
                'name': '1. Attack',
                'current': self.player.damage,
                'key': 'attack',
                'color': (255, 100, 100),
                'icon': '⚔️'
            },
            {
                'name': '2. Health Max',
                'current': self.player.health,
                'key': 'health',
                'color': (100, 255, 100),
                'icon': '❤️'
            },
            {
                'name': '3. Speed',
                'current': int(self.player.speed),
                'key': 'speed',
                'color': (100, 150, 255),
                'icon': '⚡'
            }
        ]
        
        for i, upgrade in enumerate(upgrades):
            # Texto do atributo
            attr_text = f"{upgrade['icon']} {upgrade['name']}: {upgrade['current']}"
            attr_surf = self.ui_font.render(attr_text, True, upgrade['color'])
            self.display_surface.blit(attr_surf, (menu_rect.left + padding, y_offset))
            
            # Botão de upgrade
            if self.attribute_points > 0:
                button_x = menu_rect.right - 100
                button_y = y_offset - 5
                button = Button(
                    button_x, button_y, 80, 35,
                    f"+ UP",
                    color=(0, 100, 0),
                    hover_color=(0, 150, 0),
                    text_color=(255, 255, 255)
                )
                
                button.upgrade_key = upgrade['key']
                self.upgrade_buttons.append(button)
                
                # Desenha o botão
                mouse_pos = pygame.mouse.get_pos()
                button.check_hover(mouse_pos)
                button.draw(self.display_surface, button_font)
            else:
                locked_text = button_font.render("---", True, (80, 80, 80))
                self.display_surface.blit(locked_text, (menu_rect.right - 90, y_offset))
            
            y_offset += 60
        
        # Separador
        pygame.draw.line(self.display_surface, (100, 100, 100), 
                        (menu_rect.left + padding, y_offset), 
                        (menu_rect.right - padding, y_offset), 2)
        y_offset += 15
        
        # Informações adicionais
        info_texts = [
            f"Level: {self.player.level}",
            f"XP: {self.player.current_xp}/{self.player.next_level_up}",
            f"Moedas: {self.score}",
            f"Bananas: {self.banana_inventory}",
            f"Pedras: {self.rock_inventory}"
        ]
        
        info_font = pygame.font.Font(None, 26)
        for text in info_texts:
            surf = info_font.render(text, True, text_color)
            self.display_surface.blit(surf, (menu_rect.left + padding, y_offset))
            y_offset += 28
        
        # Instruções
        y_offset += 5
        if self.attribute_points > 0:
            inst_text = "Clique nos botões ou pressione 1, 2 ou 3"
            inst_color = (255, 255, 100)
        else:
            inst_text = "Suba de nível para ganhar pontos!"
            inst_color = (150, 150, 150)
        
        inst_surf = pygame.font.Font(None, 22).render(inst_text, True, inst_color)
        inst_rect = inst_surf.get_rect(centerx=menu_rect.centerx, top=y_offset)
        self.display_surface.blit(inst_surf, inst_rect)
        
        # Fechar menu
        close_text = pygame.font.Font(None, 22).render("Pressione M para fechar", True, (200, 200, 200))
        close_rect = close_text.get_rect(midbottom=(menu_rect.centerx, menu_rect.bottom - 10))
        self.display_surface.blit(close_text, close_rect)
    
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
    
    def punch_collision(self):
        """Verifica colisões do soco com inimigos"""
        for punch in self.punch_sprites:
            hits = pygame.sprite.spritecollide(punch, self.enemy_sprites, False)
            for enemy in hits:
                # Evita atingir o mesmo inimigo múltiplas vezes com o mesmo soco
                if enemy not in punch.hit_enemies:
                    enemy.health -= punch.damage
                    punch.hit_enemies.add(enemy)
                    
                    # Efeito de knockback maior no soco
                    enemy_pos = pygame.Vector2(enemy.rect.center)
                    punch_pos = pygame.Vector2(punch.rect.center)
                    knockback = (enemy_pos - punch_pos).normalize() * 30
                    enemy.rect.center += knockback
                    
                    if enemy.health <= 0:
                        self.drop_xp(enemy.rect.center, xp_amount=5)
                        enemy.kill()
                    
                    print(f"💥 Soco acertou! Dano: {punch.damage}")
    
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

                            self.attribute_points += 1
                            self.show_temp_message(f"🎉 LEVEL {self.player.level}! +1 Ponto", (0, 255, 255))
                            print(f"🎉 LEVEL UP! Level {self.player.level}! Ganhou 1 ponto de atributo")
                except Exception as e:
                    print(f"Erro ao coletar XP: {e}")

    def reset_game(self):
        """Reseta o jogo"""
        # Limpa grupos
        self.attribute_points = 0
        self.enemy_sprites.empty()
        self.bullet_sprites.empty()
        self.punch_sprites.empty()
        self.collectible_sprites.empty()
        self.coin_sprites.empty()
        self.banana_sprites.empty()
        self.rock_sprites.empty()
        
        # Remove sprites
        for sprite in list(self.all_sprites):
            if isinstance(sprite, (Enemy, Bullet, Punch, XP, Coin, Banana, Rock)):
                sprite.kill()
        
        # Reseta player
        self.player.health = 10
        self.player.current_health = 10
        self.player.current_xp = 0
        self.player.level = 1
        self.player.next_level_up = 10
        self.player.damage = 2
        self.player.speed = 500
        self.player.rect.center = self.player_start_pos
        
        # Reseta estado
        self.player_invincible = False
        self.score = 0
        self.banana_inventory = 0
        self.rock_inventory = 3
        self.game_over = False
        self.temp_message = ""
        print("✅ Jogo resetado!")
    
    def apply_attribute_upgrade(self, upgrade_key):
        """Aplica upgrade de atributo usando 1 ponto"""
        if self.attribute_points <= 0:
            self.show_temp_message("Sem pontos disponíveis!", (255, 100, 100))
            return
        
        self.attribute_points -= 1
        
        if upgrade_key == 'attack':
            self.player.damage += 1
            self.show_temp_message("⚔️ Attack +1!", (255, 100, 100))
            print(f"[UPGRADE] Attack aumentado para {self.player.damage}")
            
        elif upgrade_key == 'health':
            self.player.health += 5
            self.player.current_health += 5
            self.show_temp_message("❤️ Health +5!", (100, 255, 100))
            print(f"[UPGRADE] Health aumentado para {self.player.health}")
            
        elif upgrade_key == 'speed':
            self.player.speed += 10
            self.show_temp_message("⚡ Speed +10!", (100, 150, 255))
            print(f"[UPGRADE] Speed aumentado para {self.player.speed}")
        
        print(f"Pontos restantes: {self.attribute_points}")

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            dt = self.clock.tick(60) / 1000

            # ========= EVENTOS =========
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # ----- MENU -----
                if self.game_state == "menu":
                    result = self.menu.handle_events(event)
                    if result == "start_game":
                        self.game_state = "playing"
                        pygame.mouse.set_visible(False)
                        print("Jogo iniciado!")
                    elif result == "quit":
                        self.running = False

                # ----- JOGANDO -----
                elif self.game_state == "playing":

                    # Reiniciar no game over
                    if self.game_over:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.reset_game()

                    # Teclas
                    if not self.game_over and event.type == pygame.KEYDOWN:
                        # Abrir/fechar menu de atributos
                        if event.key == pygame.K_l:
                            self.show_store = not self.show_store
                            pygame.mouse.set_visible(self.show_store)
                            print(f"Loja {'aberta' if self.show_store else 'fechada'}")
                        if event.key == pygame.K_m:
                            self.show_attributes = not self.show_attributes
                            pygame.mouse.set_visible(self.show_attributes)

                        # Usar banana
                        if event.key == pygame.K_h:
                            self.use_banana()

                        # Upgrades 1, 2, 3
                        if self.show_attributes and self.attribute_points > 0:
                            if event.key == pygame.K_1:
                                self.apply_attribute_upgrade('attack')
                            elif event.key == pygame.K_2:
                                self.apply_attribute_upgrade('health')
                            elif event.key == pygame.K_3:
                                self.apply_attribute_upgrade('speed')

                    # Clique nos botões do menu de atributos
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.show_attributes and self.attribute_points > 0:
                            mouse_pos = pygame.mouse.get_pos()
                            for button in self.upgrade_buttons:
                                if button.is_clicked(mouse_pos):
                                    self.apply_attribute_upgrade(button.upgrade_key)
                        
                        if self.show_store:
                            mouse_pos = pygame.mouse.get_pos()
                            item, success = self.store.handle_click(mouse_pos, self.score)
                            
                            if item and success:
                                # Compra bem-sucedida
                                self.score -= 4  # Gasta 4 moedas
                                
                                if item == 'banana':
                                    self.banana_inventory += 1
                                    self.show_temp_message("🍌 Banana comprada!", (255, 255, 0))
                                    print(f"🛒 Comprou BANANA! Moedas: {self.score}")
                                
                                elif item == 'rock':
                                    self.rock_inventory += 1
                                    self.show_temp_message("🪨 Pedra comprada!", (150, 150, 150))
                                    print(f"🛒 Comprou PEDRA! Moedas: {self.score}")
                            
                            elif item and not success:
                                # Tentou comprar sem moedas
                                self.show_temp_message("❌ Moedas insuficientes!", (255, 100, 100))
                                print(f"❌ Sem moedas! Você tem {self.score}, precisa de 4")

                    # Spawns
                    if event.type == self.enemy_event and not self.game_over:
                        if self.spawn_positions:
                            Enemy(
                                pos=choice(self.spawn_positions),
                                frames=None,
                                groups=(self.all_sprites, self.enemy_sprites),
                                player=self.player,
                                collision_sprites=self.collision_sprites
                            )

                    if event.type == self.coin_event and not self.game_over:
                        self.spawn_coin()

                    if event.type == self.banana_event and not self.game_over:
                        self.spawn_banana()
                    
                    if event.type == self.rock_event and not self.game_over:
                        self.spawn_rock()

            # ========= ATUALIZAÇÃO / DESENHO =========

            # ----- MENU -----
            if self.game_state == "menu":
                self.menu.update()
                self.menu.draw()

            # ----- JOGANDO -----
            elif self.game_state == "playing":

                # Atualização da lógica
                if not self.game_over and not self.show_attributes and not self.show_store:
                    self.gun_timer()
                    self.punch_timer()
                    self.invincibility_timer()
                    self.input()
                    self.input_punch()
                    if self.mira:
                        self.mira.update()

                    self.all_sprites.update(dt)
                    self.bullet_collision()
                    self.punch_collision()
                    self.collect_items()
                    self.collect_coins()
                    self.collect_bananas()
                    self.collect_rocks()

                    # Dano dos inimigos
                    if not self.player_invincible:
                        for enemy in self.enemy_sprites:
                            if self.player.rect.colliderect(enemy.rect):
                                damage = getattr(enemy, 'damage', 1)
                                self.player.current_health -= damage

                                self.player_invincible = True
                                self.last_damage_time = pygame.time.get_ticks()

                                vec = pygame.Vector2(self.player.rect.center) - pygame.Vector2(enemy.rect.center)
                                if vec.length() > 0:
                                    self.player.rect.center += vec.normalize() * 10

                                if self.player.current_health <= 0:
                                    self.game_over = True
                                    print("💀 GAME OVER!")
                                break

                # Renderização
                self.display_surface.fill("black")
                self.all_sprites.draw(self.player.rect.center)

                # Player piscando quando invencível
                if self.player.current_health > 0:
                    if not self.player_invincible or (pygame.time.get_ticks() // 100) % 2:
                        player_screen_pos = self.player.rect.topleft + self.all_sprites.offset
                        self.display_surface.blit(self.player.image, player_screen_pos)
                
                # Desenha socos
                for punch in self.punch_sprites:
                    punch_screen_pos = punch.rect.topleft + self.all_sprites.offset
                    self.display_surface.blit(punch.image, punch_screen_pos)

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
                
                if self.show_store:
                    self.store.draw(self.score)

                if self.game_over:
                    self.draw_game_over_screen()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
