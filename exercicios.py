import pygame
from pygame import mixer
from pathlib import Path
import random

DIRETORIO_ATUAL = str(Path(__file__).parent.absolute())

pygame.init()
mixer.init()

tela = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Sonic Game")
try:
    sonic_img = pygame.image.load(DIRETORIO_ATUAL + '/imagens/sonic-stop.png')
    fundo = pygame.image.load(DIRETORIO_ATUAL + '/imagens/green-hills.png')
    vilao_img = pygame.image.load(DIRETORIO_ATUAL + '/imagens/vilao.png')
except pygame.error as e:
    print(f"Erro ao carregar as imagens: {e}")
    pygame.quit()
    exit()

try:
    mixer.music.load(DIRETORIO_ATUAL + '/musicas/musica1.wav')
    mixer.music.play(-1)
except pygame.error as e:
    print(f"Erro ao carregar ou tocar a música: {e}")
    pygame.quit()
    exit()

score = 0
clock = pygame.time.Clock()

class Sonic:
    def __init__(self):
        self.x = 100
        self.y = 350  # Posição inicial do Sonic no chão
        self.speed = 10
        self.image = sonic_img
        self.velocidade_pulo = 0
        self.no_chao = True  # Indica se o Sonic está no chão

    def draw(self):
        tela.blit(self.image, (self.x, self.y))
    
    def move(self, dx, dy):
        """Move Sonic apenas horizontalmente, já que ele não pode flutuar verticalmente com as setas"""
        self.x += dx * self.speed
        self.x = max(0, min(self.x, 800 - self.image.get_width()))

    def pular(self):
        """Sonic só pode pular se estiver no chão"""
        if self.no_chao:
            self.velocidade_pulo = -15  # Força do pulo
            self.no_chao = False
    
    def gravidade(self):
        """Aplica a gravidade ao Sonic para que ele caia de volta ao chão"""
        if not self.no_chao:
            self.velocidade_pulo += 1  # Aceleração da gravidade
            self.y += self.velocidade_pulo

            # Se o Sonic atingir o chão, ele para de cair
            if self.y >= 350:  # Ajuste do chão fixo
                self.y = 350
                self.no_chao = True
                self.velocidade_pulo = 0

class Vilao:
    def __init__(self):
        self.x = 600  # Posição fixa do vilão
        self.y = 350  # Posição fixa do vilão
        self.image = pygame.transform.scale(vilao_img, (sonic_img.get_width(), sonic_img.get_height()))  # Redimensiona a imagem do vilão

    def draw(self):
        tela.blit(self.image, (self.x, self.y))
    
    # Remover o movimento do vilão
    # A função move() foi removida, já que o vilão não se move

def colidiu(obj1, obj2):
    return obj1.x < obj2.x + obj2.image.get_width() and obj1.x + obj1.image.get_width() > obj2.x \
        and obj1.y < obj2.y + obj2.image.get_height() and obj1.y + obj1.image.get_height() > obj2.y

# Sombra do Sonic
class Shadow:
    def __init__(self):
        self.x = sonic.x
        self.y = 350  # A sombra sempre vai ficar na mesma posição do chão, onde o Sonic deve estar

    def draw(self):
        sombra_img = pygame.Surface((sonic_img.get_width(), sonic_img.get_height() // 4))  # Fazendo uma sombra simples
        sombra_img.fill((0, 0, 0))  # Cor preta para a sombra
        sombra_img.set_alpha(100)  # Transparência para a sombra
        tela.blit(sombra_img, (self.x, self.y + 20))  # Desenha a sombra um pouco abaixo do Sonic

sonic = Sonic()
vilao = Vilao()
shadow = Shadow()

executando = True

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:  # O Sonic pula quando a tecla de espaço é pressionada
                sonic.pular()

    keys = pygame.key.get_pressed()
    dx = dy = 0
    
    # Movimento horizontal com as setas
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    sonic.move(dx, dy)
    
    sonic.gravidade()  # A gravidade afeta o Sonic

    if colidiu(sonic, vilao):
        print("Game Over! Sonic colidiu com o vilão.")
        executando = False

    score += 1

    tela.blit(fundo, (0, 0))
    shadow.draw()  # Desenha a sombra do Sonic
    sonic.draw()
    vilao.draw()  # O vilão não se move, ele é desenhado na posição fixa

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    tela.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
