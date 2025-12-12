import pygame

class Player:
    def __init__(self, x, y, size, color="blue"):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_w]:
            if self.y > 0:
                self.y -= self.speed
        if keys[pygame.K_s]:
            if self.y + self.size < screen_height:
                self.y += self.speed
        if keys[pygame.K_d]:
            if self.x + self.size < screen_width:
                self.x += self.speed
        if keys[pygame.K_a]:
            if self.x > 0:
                self.x -= self.speed

    

pygame.init()
width, height = 1200, 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Apenas Comece")
clock = pygame.time.Clock() #Controla o FPS

#Criação do jogador na tela
player_size = 100

running = True

gorila = Player(550, 350, player_size)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    gorila.move(pygame.key.get_pressed(), width, height)
    player = pygame.Rect(gorila.x, gorila.y, gorila.size, gorila.size)
    screen.fill("black") # 1. Limpa a tela (pinta de preto)
    
    pygame.draw.rect(screen, "blue", player)
    # Aqui você desenha: pygame.draw.rect(...) ou tela.blit(...)

    pygame.display.flip() # 2. Atualiza o display (mostra o frame novo)
    
    clock.tick(60) # Garante que rode a 60 frames por segundo

pygame.quit()