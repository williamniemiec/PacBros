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
from Display import *
import pickle


#--------------------------------------------------------------------------
#    OBJETO INIT
#--------------------------------------------------------------------------
class Init:
    def __init__(self, filename, size):
        self.filename = filename
        self.size = size

        self.map_color_background = BLACK
        self.map_size_cheese = size*0.5

        self.player = None
        self.list_cats = []
        self.list_doors = []
        self.map = []
        self.larg = 680
        self.alt =  480
        self.placar = 0
        self.vida = 3
        self.actualTime = 0
        self.startTime = 0
        self.queijos = 0
        self.TOT_QUEIJOS = 116

    def get_player(self):
        return self.player

    def get_doors(self):
        return self.list_doors

    def get_cats(self):
        return self.list_cats

    # Converte um mapa .txt em uma matriz
    def parseMap(self):
        file = open(self.filename, 'r')
        content = file.readlines()
        file.close()
        x_axis = 0
        y_axis = 0
        
        # Percorre todas as linhas do arquivo
        for line in content:
            lineMap = []
            
            # Percorre todas as colunas do arquivo
            for caracter in line:
                if caracter == 'X':
                    lineMap.append(Wall(x_axis, y_axis, self.size))
                elif caracter == 'M':
                    lineMap.append(Player(x_axis, y_axis, self.size))
                    self.player = Player(x_axis, y_axis, self.size)
                elif caracter == 'Q':
                    lineMap.append(Cheese(x_axis, y_axis, self.size))
                elif caracter == 'G':
                    lineMap.append(Cat(x_axis, y_axis, self.size))
                    self.list_cats.append(Cat(x_axis, y_axis, self.size))
                elif caracter == 'T':
                    lineMap.append(Door(x_axis, y_axis, x_axis+1, y_axis+1, self.size))
                    self.list_doors.append(Door(x_axis, y_axis, x_axis+1, y_axis+1, self.size))
                elif caracter == 'O':
                    lineMap.append(Bone(x_axis, y_axis, self.size))
                x_axis += 1

            x_axis = 0
            y_axis += 1
            self.map.append(lineMap)

    
    # Atualiza coordenadas (x0,y0) = (x,y)
    # OBS: matriz - linhas são como se fosse eixo y; colunas, eixo x
    def mapUpdate(self, x0_axis, y0_axis, x_axis, y_axis, content, hold = False):
        if hold:
            tmp = self.map[y0_axis][x0_axis]
            self.map[y_axis][x_axis] = content
            self.map[y0_axis][x0_axis] = tmp
        else:
            self.map[y_axis][x_axis] = content
            self.map[y0_axis][x0_axis] = None

    # Insere um item em uma coordenada no mapa
    def mapInsert(self, x_axis, y_axis, content, hold = False):
        self.map[y_axis][x_axis] = content

    # Retorna o item do mapa presente na coordenada (x,y)
    def get_map_item(self, x_axis, y_axis):
        return self.map[y_axis][x_axis]

    # Salva o objeto em disco
    def save(self):
        outFile = open('PB_saveGame.pbs', 'wb')
        pickle.dump(self, outFile)
        outFile.close()

    # Carrega o objeto em disco
    def load(self):
        try:
            inFile = open('PB_saveGame.pbs', 'rb')
            obj = pickle.load(inFile)
            inFile.close()

            self.filename = obj.filename
            self.size = obj.size
            self.player = obj.player
            self.list_cats = obj.list_cats
            self.list_doors = obj.list_doors
            self.map = obj.map
            self.placar = obj.placar
            self.vida = obj.vida
            self.player.modoCachorro = obj.player.modoCachorro
            self.actualTime = obj.actualTime + pygame.time.get_ticks()
            self.startTime = obj.startTime + pygame.time.get_ticks()
            self.queijos = obj.queijos
        except:
            print('erro')
            return False

        return True

    # Função que inicia o jogo
    def startGame(self):
        sair = False
        voltarMenu = False

        # Cria display
        display = Display(self.larg, self.alt, self)
        screen = display.get_screen()
        pygame.display.set_caption("PacBros")
        icon = pygame.image.load('img/icon.png')
        pygame.display.set_icon(icon)

        # Inicializa Clock
        clock = pygame.time.Clock()

        # Converte mapa .txt em matriz
        self.parseMap()

        # Exibe menu principal
        sair = display.mainMenu()
        
        # Se opção for por sair do jogo, volta pro main retornando True
        if sair:
            return True

        doors = self.get_doors()
        cats = self.get_cats()

        # Escolhe música adequada
        if self.player.modoCachorro:
            pygame.mixer.music.load('music/modoCachorro.mp3')
        else:
            pygame.mixer.music.load('music/game.mp3')

        pygame.mixer.music.play(-1)
        
        # Loop principal do jogo
        ''' Executa enquanto:   * Usuário não sair do jogo
                                * Jogador tiver vidas
                                * Houver queijos no mapa
        '''
        while not sair and self.vida > 0 and self.queijos != self.TOT_QUEIJOS:
            # Verifica eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        self.player.move(self, 'LEFT')
                    elif event.key == K_RIGHT:
                        self.player.move(self, 'RIGHT')
                    elif event.key == K_UP:
                        self.player.move(self, 'UP')
                    elif event.key == K_DOWN:
                        self.player.move(self, 'DOWN')
                    elif event.key == K_b:
                        for door in doors:
                            door.move(self)
                    elif event.key == K_TAB:
                        sair = display.pauseMenu()
                        if sair == None:
                            return True

                        # Seleciona música adequada
                        if self.player.modoCachorro:
                            pygame.mixer.music.load('music/modoCachorro.mp3')
                        else:
                            pygame.mixer.music.load('music/game.mp3')

                        pygame.mixer.music.play(-1)
            
            # Se modo cachorro está ativado, verifica se já passou o tempo para desativá-lo
            if self.player.modoCachorro:
                self.actualTime = pygame.time.get_ticks()
                timer = abs((self.actualTime - self.startTime)//1000)
                if timer > 8:
                    desativarModoCachorro(self)
            
            # Faz os gatos se moverem
            for cat in cats:
                cat.autoMove(self)        
            
            # Printa mapa na tela
            screen.fill(BLACK)
            display.printMap()
            display.rodape()
            display.instrucoes()
            pygame.display.update()

            # Seta fps do jogo
            clock.tick(5)

        # Verifica o tipo de saída do jogo
        # Se saída for por ter consumido todos os queijos, jogador ganha o jogo
        if self.queijos == self.TOT_QUEIJOS:
            return display.fimJogo()

        # Se saída for por ter acabado as vidas do jogador ele perde o jogo
        elif self.vida <= 0:
            return display.gameOver()

        # Senão, saída é para sair do jogo e encerrar programa
        return False