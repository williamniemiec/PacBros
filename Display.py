# -*- coding: utf-8 -*-

#==========================================================================
#                                  PACBROS
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS 
#--------------------------------------------------------------------------
import pygame
from pygame.locals import *
from colors import *
from Characters import *
from Itens import *
from Init import *


#--------------------------------------------------------------------------
#    OBJETO DISPLAY
#--------------------------------------------------------------------------
class Display:
    def __init__(self, largura, altura, init):
        self.screen = pygame.display.set_mode((largura,altura))
        self.init = init

        self.map_color_wall = BLUE
        self.map_color_wall_inv = RED
        self.map_color_background = BLACK
        self.map_size_cheese = self.init.size*0.5

    def get_screen(self):
        return self.screen

    def printMap(self):
        x_axis = 0
        y_axis = 0

        for line in self.init.map:
            for column in line:
                if isinstance(column, Wall):
                    if self.init.player.modoCachorro:
                        pygame.draw.rect(self.screen, self.map_color_wall_inv, [x_axis, y_axis, self.init.size, self.init.size])
                    else:
                        pygame.draw.rect(self.screen, self.map_color_wall, [x_axis, y_axis, self.init.size, self.init.size])
                elif isinstance(column, Player):
                    self.iconToRect(x_axis, y_axis, column.image)
                elif isinstance(column, Cheese):
                    self.iconToRect(x_axis, y_axis, column.image)
                elif isinstance(column, Cat):
                    self.iconToRect(x_axis, y_axis, column.image)
                elif isinstance(column, Door):
                    pygame.draw.rect(self.screen, CYAN, [x_axis, y_axis, self.init.size, self.init.size])
                elif isinstance(column, Bone):
                    self.iconToRect(x_axis, y_axis, column.image)
                else:
                    pygame.draw.rect(self.screen, BLACK, [x_axis, y_axis, self.init.size, self.init.size])
                x_axis += self.init.size

            x_axis = 0
            y_axis += self.init.size

    def rodape(self):
        pygame.font.init() # you have to call this at the start, 
                       # if you want to use this module.
        myfont = pygame.font.SysFont('Consolas', 15)
        div = '*********************************************************************'
        placar = 'PLACAR: '+str(self.init.placar)
        vidas = 'VIDA: '+str(self.init.vida)
        cachorroAtivado = 'MODO CACHORRO: ATIVADO'
        cachorroDesativado = 'MODO CACHORRO: DESATIVADO'
        
        #textsurface = myfont.render(div, False, (255, 255, 255))
        #screen.blit(textsurface,(0,300))
        pygame.draw.line(self.screen, WHITE, (0, 295), (self.init.larg, 295), 2)

        textsurface = myfont.render(placar, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,300))

        textsurface = myfont.render(vidas, False, (255, 255, 255))
        self.screen.blit(textsurface,(self.init.larg - len(vidas) - 100,300))

        if self.init.player.modoCachorro:
            textsurface = myfont.render(cachorroAtivado, False, (255, 255, 255))
        else:
            textsurface = myfont.render(cachorroDesativado, False, (255, 255, 255))
        self.screen.blit(textsurface,(240,315))

        pygame.draw.line(self.screen, WHITE, (0, 335), (self.init.larg, 335), 2)

    def instrucoes(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Consolas', 15)

        title = 'COMANDOS'
        w =     'W | SETA PARA CIMA:                        IR PARA CIMA'
        s =     'S | SETA PARA BAIXO:                       IR PARA BAIXO'
        e =     'E | SETA PARA ESQUERDA:                    IR PARA ESQUERDA'
        d =     'D | SETA PARA DIREITA:                     IR PARA DIREITA'
        b =     'B:                                         ABRIR | FECHAR PORTAS'
        tab =   'TAB:                                       MENU'

        textsurface = myfont.render(title, False, (255, 255, 255))
        self.screen.blit(textsurface,(250,340))

        textsurface = myfont.render(w, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,355))

        textsurface = myfont.render(s, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,370))

        textsurface = myfont.render(e, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,385))

        textsurface = myfont.render(d, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,400))

        textsurface = myfont.render(b, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,415))

        textsurface = myfont.render(tab, False, (255, 255, 255))
        self.screen.blit(textsurface,(0,430))

        pygame.draw.line(self.screen, WHITE, (0, 445), (self.init.larg, 445), 2)


    def iconToRect(self, x_axis, y_axis, image):
        picture = pygame.image.load(image)
        picture = pygame.transform.scale(picture, (self.init.size, self.init.size))
        rect = picture.get_rect()
        rect = rect.move((x_axis, y_axis))
        self.screen.blit(picture, rect)

    def pauseMenu(self):
        pygame.mixer.music.load('music/pauseMenu.mp3')
        pygame.mixer.music.play(-1)
        pygame.font.init()
        fontSize = 15
        myfont = pygame.font.SysFont('Consolas', 15)
        jogoSalvo = False

        self.screen.fill(BLACK)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1 or event.key == K_TAB:
                        return False
                    elif event.key == K_2:
                        self.init.save()
                        jogoSalvo = True
                        return False
                    elif event.key == K_3:
                        return True

            self.logo()
            op1 = '(1) Continuar'
            op2 = '(2) Salvar'
            op3 = '(3) Sair'
            saved = 'Jogo salvo com sucesso!'

            textsurface = myfont.render(op1, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*8))

            textsurface = myfont.render(op2, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*9))

            textsurface = myfont.render(op3, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*10))

            if jogoSalvo:
                pygame.draw.line(self.screen, WHITE, (0, fontSize*11), (self.init.larg, fontSize*11), 2)
                textsurface = myfont.render(op3, False, (255, 255, 255))
                self.screen.blit(textsurface,(0,fontSize*11+5))
                pygame.draw.line(self.screen, WHITE, (0, fontSize*12+10), (self.init.larg, fontSize*12+10), 2)

            pygame.display.update()
            

    def mainMenu(self):
        pygame.mixer.music.load('music/mainMenu.mp3')
        pygame.mixer.music.play(-1)
        pygame.font.init()
        fontSize = 15
        myfont = pygame.font.SysFont('Consolas', fontSize)
        erro = False

        self.screen.fill(BLACK)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        pygame.mixer.music.stop()
                        return False
                    elif event.key == K_2:
                        if self.init.load():
                            jogoCarregado = True
                            pygame.mixer.music.stop()
                            return False
                        else:
                            erro = True
                    elif event.key == K_3:
                        pygame.mixer.music.stop()
                        return True

            self.logo()
            op1 = '(1) Novo jogo'
            op2 = '(2) Carregar jogo'
            op3 = '(3) Sair'
            str_erro = 'Ocorreu um erro'

            textsurface = myfont.render(op1, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*8))

            textsurface = myfont.render(op2, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*9))

            textsurface = myfont.render(op3, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,fontSize*10))

            if erro:
                pygame.draw.line(self.screen, WHITE, (0, fontSize*12), (self.init.larg, fontSize*12), 2)
                textsurface = myfont.render(str_erro, False, (255, 255, 255))
                self.screen.blit(textsurface,(0,fontSize*12+5))
                pygame.draw.line(self.screen, WHITE, (0, fontSize*13+10), (self.init.larg, fontSize*13+10), 2)

            pygame.display.update()

    def logo(self):
        fontSize = 15
        title_align = 150
        title_color = RED
        myfont = pygame.font.SysFont('Consolas', fontSize)

        t0 = " _____                      ______               "
        t1 = "/  ___|                     | ___ \\              "
        t2 = "\\ `--. _   _ _ __   ___ _ __| |_/ /_ __ ___  ___ "
        t3 = " `--. \\ | | | '_ \\ / _ \\ '__| ___ \\ '__/ _ \\/ __|"
        t4 = "/\\__/ / |_| | |_) |  __/ |  | |_/ / | | (_) \\__ \\"
        t5 = "\\____/ \\__,_| .__/ \\___|_|  \\____/|_|  \\___/|___/"
        t6 = "            | |                                  "
        t7 = "            |_|   "

        textsurface = myfont.render(t0, False, title_color)
        self.screen.blit(textsurface,(title_align, 0))

        textsurface = myfont.render(t1, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize))

        textsurface = myfont.render(t2, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*2))

        textsurface = myfont.render(t3, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*3))

        textsurface = myfont.render(t4, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*4))

        textsurface = myfont.render(t5, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*5))

        textsurface = myfont.render(t6, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*6))

        textsurface = myfont.render(t7, False, title_color)
        self.screen.blit(textsurface,(title_align,fontSize*7))


    def fimJogo(self):
        pygame.mixer.music.load('music/fimJogo.mp3')
        pygame.mixer.music.play(-1)

        pygame.font.init()
        myfont = pygame.font.SysFont('Consolas', 30)

        self.screen.fill(BLACK)
        title1 = 'Parabéns'
        title2 = 'Você ganhou o jogo!!!'
        title3 = 'Placar final: '+str(self.init.placar)

        textsurface = myfont.render(title1, False, (255, 255, 255))
        self.screen.blit(textsurface,(250,0))

        textsurface = myfont.render(title2, False, (255, 255, 255))
        self.screen.blit(textsurface,(150,40))

        textsurface = myfont.render(title3, False, (255, 255, 255))
        self.screen.blit(textsurface,(150,80))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    return False

    def gameOver(self):
        pygame.mixer.music.load('music/gameOver.mp3')
        pygame.mixer.music.play(-1)

        pygame.font.init()
        myfont = pygame.font.SysFont('Consolas', 30)

        self.screen.fill(BLACK)
        title1 = 'Game Over'
        title2 = ':/'

        textsurface = myfont.render(title1, False, (255, 255, 255))
        self.screen.blit(textsurface,(250,220))

        textsurface = myfont.render(title2, False, (255, 255, 255))
        self.screen.blit(textsurface,(300,250))

        pygame.display.update()

        startTime = pygame.time.get_ticks()
        timer = 0
        while timer < 2:
            actualTime = pygame.time.get_ticks()
            timer = abs((actualTime - startTime)//1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.KEYDOWN:
                    return False