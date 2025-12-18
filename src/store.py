import pygame
from button import Button

class Store:
    """
    Loja simples com apenas Pedras e Bananas.
    Ambos custam 4 moedas.
    """
    def __init__(self, display_surface, window_width, window_height):
        self.display_surface = display_surface
        self.window_width = window_width
        self.window_height = window_height
        
        # Configurações visuais
        self.bg_color = (30, 30, 30)
        self.border_color = (200, 150, 50)  # Dourado
        self.text_color = (255, 255, 255)
        
        # Fontes
        self.title_font = pygame.font.Font(None, 60)
        self.item_font = pygame.font.Font(None, 36)
        self.price_font = pygame.font.Font(None, 32)
        self.hint_font = pygame.font.Font(None, 24)
        
        # Dimensões da janela
        self.width = 500
        self.height = 400
        self.x = (window_width - self.width) // 2
        self.y = (window_height - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Botões dos itens (serão criados no draw)
        self.banana_button = None
        self.rock_button = None
        
        # Preço fixo
        self.price = 4
    
    def draw(self, player_coins):
        """Desenha a loja na tela"""
        # Fundo semi-transparente atrás da loja
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Janela principal da loja
        pygame.draw.rect(self.display_surface, self.bg_color, self.rect)
        pygame.draw.rect(self.display_surface, self.border_color, self.rect, 5)
        
        # ===== TÍTULO =====
        title_surf = self.title_font.render("🏪 LOJA", True, (255, 215, 0))
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        self.display_surface.blit(title_surf, title_rect)
        
        # ===== MOEDAS DO PLAYER =====
        coins_surf = self.item_font.render(f"Suas moedas: 💰 {player_coins}", True, (255, 215, 0))
        coins_rect = coins_surf.get_rect(midtop=(self.rect.centerx, title_rect.bottom + 15))
        self.display_surface.blit(coins_surf, coins_rect)
        
        # Linha separadora
        line_y = coins_rect.bottom + 20
        pygame.draw.line(self.display_surface, self.border_color,
                        (self.rect.left + 30, line_y),
                        (self.rect.right - 30, line_y), 3)
        
        # ===== ÁREA DOS ITENS =====
        items_start_y = line_y + 30
        item_spacing = 90
        
        # Pega posição do mouse para hover
        mouse_pos = pygame.mouse.get_pos()
        
        # ===== ITEM 1: BANANA 🍌 =====
        banana_y = items_start_y
        
        # Verifica se pode comprar
        can_afford_banana = player_coins >= self.price
        banana_color = (255, 255, 0) if can_afford_banana else (100, 100, 0)
        
        # Ícone e nome
        banana_text = self.item_font.render("🍌 BANANA", True, banana_color)
        banana_text_rect = banana_text.get_rect(topleft=(self.rect.left + 40, banana_y))
        self.display_surface.blit(banana_text, banana_text_rect)
        
        # Descrição
        desc_text = self.hint_font.render("Recupera 3 de vida", True, (200, 200, 200))
        desc_rect = desc_text.get_rect(topleft=(self.rect.left + 40, banana_y + 35))
        self.display_surface.blit(desc_text, desc_rect)
        
        # Botão de compra
        button_x = self.rect.right - 140
        button_y = banana_y - 5
        
        self.banana_button = Button(
            button_x, button_y, 110, 50,
            f"💰 {self.price}",
            color=(0, 120, 0) if can_afford_banana else (80, 80, 80),
            hover_color=(0, 180, 0) if can_afford_banana else (80, 80, 80),
            text_color=(255, 255, 255)
        )
        
        if can_afford_banana:
            self.banana_button.check_hover(mouse_pos)
        
        self.banana_button.draw(self.display_surface, self.price_font)
        
        # ===== ITEM 2: PEDRA 🪨 =====
        rock_y = banana_y + item_spacing
        
        # Verifica se pode comprar
        can_afford_rock = player_coins >= self.price
        rock_color = (150, 150, 150) if can_afford_rock else (60, 60, 60)
        
        # Ícone e nome
        rock_text = self.item_font.render("🪨 PEDRA", True, rock_color)
        rock_text_rect = rock_text.get_rect(topleft=(self.rect.left + 40, rock_y))
        self.display_surface.blit(rock_text, rock_text_rect)
        
        # Descrição
        desc_text = self.hint_font.render("Munição para atirar", True, (200, 200, 200))
        desc_rect = desc_text.get_rect(topleft=(self.rect.left + 40, rock_y + 35))
        self.display_surface.blit(desc_text, desc_rect)
        
        # Botão de compra
        self.rock_button = Button(
            button_x, rock_y - 5, 110, 50,
            f"💰 {self.price}",
            color=(0, 120, 0) if can_afford_rock else (80, 80, 80),
            hover_color=(0, 180, 0) if can_afford_rock else (80, 80, 80),
            text_color=(255, 255, 255)
        )
        
        if can_afford_rock:
            self.rock_button.check_hover(mouse_pos)
        
        self.rock_button.draw(self.display_surface, self.price_font)
        
        # ===== INSTRUÇÕES DE FECHAMENTO =====
        close_text = self.hint_font.render("Pressione L para fechar a loja", True, (180, 180, 180))
        close_rect = close_text.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 15))
        self.display_surface.blit(close_text, close_rect)
    
    def handle_click(self, mouse_pos, player_coins):
        """
        Processa cliques nos botões da loja.
        Retorna uma tupla: (item_comprado, sucesso)
        - item_comprado: 'banana', 'rock', ou None
        - sucesso: True se comprou, False se não tinha moedas
        """
        # Verifica se clicou no botão da banana
        if self.banana_button and self.banana_button.is_clicked(mouse_pos):
            if player_coins >= self.price:
                return ('banana', True)
            else:
                return ('banana', False)
        
        # Verifica se clicou no botão da pedra
        if self.rock_button and self.rock_button.is_clicked(mouse_pos):
            if player_coins >= self.price:
                return ('rock', True)
            else:
                return ('rock', False)
        
        return (None, False)