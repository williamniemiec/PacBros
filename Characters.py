# -*- coding: utf-8 -*-

#==========================================================================
#                                  PACBROS
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS 
#--------------------------------------------------------------------------
import pygame
from colors import *
from Itens import *
import math


#--------------------------------------------------------------------------
#    OBJETO CHARACTER
#--------------------------------------------------------------------------
class Character:
    def __init__(self, x_axis, y_axis, size, color = WHITE):
        self.x0_axis = x_axis
        self.y0_axis = y_axis
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.size = size
        self.color = color
        self.queijo = None

    def get_x_axis(self):
        return self.x_axis

    def get_y_axis(self):
        return self.y_axis

    def moveDown(self, init, item, hold):
        init.mapUpdate(self.x_axis, self.y_axis, self.x_axis, self.y_axis+1, item, hold)
        self.y_axis += 1

    def moveUp(self, init, item, hold):
        init.mapUpdate(self.x_axis, self.y_axis, self.x_axis, self.y_axis-1, item, hold)
        self.y_axis -= 1

    def moveLeft(self, init, item, hold):
        init.mapUpdate(self.x_axis, self.y_axis, self.x_axis-1, self.y_axis, item, hold)
        self.x_axis -= 1
    
    def moveRight(self, init, item, hold):
        init.mapUpdate(self.x_axis, self.y_axis, self.x_axis+1, self.y_axis, item, hold)
        self.x_axis += 1


#--------------------------------------------------------------------------
#    OBJETO CAT
#--------------------------------------------------------------------------
class Cat(Character):
    def __init__(self, x_axis, y_axis, size):
        Character.__init__(self, x_axis, y_axis, size)
        self.color = pygame.Color('#a200ff')
        self.image = 'img/cat.png'
        self.emCimaOsso = False
        self.emCimaQueijo = False
        self.queijo = None
        self.osso = None
        self.dir = 'LEFT'

    def reset(self, init):
        pos_atual_x = self.x_axis
        pos_atual_y = self.y_axis
        # Verifica situação de spawnkill
        if init.player.x_axis == self.x0_axis and init.player.y_axis == self.y0_axis:
            init.mapUpdate(self.x_axis, self.y_axis, self.x0_axis+1, self.y0_axis, self, False)
            self.x_axis = self.x0_axis+1
        else:
            init.mapUpdate(self.x_axis, self.y_axis, self.x0_axis, self.y0_axis, self, False)
            self.x_axis = self.x0_axis

        if self.emCimaQueijo:
            init.mapInsert(pos_atual_x, pos_atual_y, self.queijo)
            self.emCimaQueijo = False

        elif self.emCimaOsso:
            init.mapInsert(pos_atual_x, pos_atual_y, self.osso)
            self.emCimaOsso = False

        
        self.y_axis = self.y0_axis

    def move(self, init):
        dir = self.dir

        if dir == 'LEFT':
            pos_atual = self.x_axis
            prox_pos = pos_atual - 1
            
            if prox_pos > 0:
                item_prox_pos = init.get_map_item(prox_pos, self.y_axis)
                if isinstance(item_prox_pos , Wall) or isinstance(item_prox_pos , Door):
                    self.trocaDir()

                elif isinstance(item_prox_pos , Player):
                    if item_prox_pos.modoCachorro:
                        self.reset(init)
                    else:
                        init.vida -= 1
                        item_prox_pos.reset(init)
                        self.moveLeft(init, self, False)

                elif isinstance(item_prox_pos , Cat):
                    self.trocaDir()
                elif isinstance(item_prox_pos , Bone):
                    if self.emCimaQueijo:
                        #init.mapInsert(pos_atual, self.y_axis, Cheese)
                        self.emCimaQueijo = False
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)
                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.emCimaOsso = False
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveLeft(init, self, False)
                    self.osso = item_prox_pos
                elif isinstance(item_prox_pos, Cheese):

                    if self.emCimaQueijo:
                        #print('dentro em cima queijo')
                        #init.mapInsert(pos_atual, self.y_axis, self.queijo)
                        #print(init.get_map_item(pos_atual, self.y_axis))
                        self.emCimaQueijo = False
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)
                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.emCimaOsso = False
                        self.emCimaQueijo = True
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveLeft(init, self, False)

                    #self.queijo = item_prox_pos
                    self.emCimaQueijo = True
                    self.queijo = item_prox_pos
                    
                elif not item_prox_pos:
                    if self.emCimaQueijo:
                        #init.mapInsert(pos_atual, self.y_axis, Cheese)
                        self.emCimaQueijo = False
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.emCimaOsso = False
                        self.moveLeft(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveLeft(init, self, False)
            else:
                self.trocaDir()

        elif dir == 'RIGHT':
            pos_atual = self.x_axis
            prox_pos = pos_atual + 1
            
            if prox_pos < init.larg:
                item_prox_pos = init.get_map_item(prox_pos, self.y_axis)

                if isinstance(item_prox_pos , Wall) or isinstance(item_prox_pos , Door):
                    self.trocaDir()
                elif isinstance(item_prox_pos , Player):
                    if item_prox_pos.modoCachorro:
                        self.reset(init)
                    else:
                        init.vida -= 1
                        item_prox_pos.reset(init)
                        self.moveRight(init, self, False)
                elif isinstance(item_prox_pos , Cat):
                    self.trocaDir()
                    item_prox_pos.trocaDir()
                    # troca direção
                elif isinstance(item_prox_pos , Bone):

                    if self.emCimaQueijo:
                        self.emCimaQueijo = False
                        self.moveRight(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)
                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.emCimaOsso = False
                        self.moveRight(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveRight(init, self, False)
                    self.osso = item_prox_pos
                elif isinstance(item_prox_pos , Cheese):

                    if self.emCimaQueijo:
                        #init.mapInsert(pos_atual, self.y_axis, Cheese)
                        self.moveRight(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.moveRight(init, self, True)
                        self.emCimaOsso = False
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveRight(init, self, False)

                    self.emCimaQueijo = True
                    self.queijo = item_prox_pos
                elif not item_prox_pos:
                    if self.emCimaQueijo:
                        #init.mapInsert(pos_atual, self.y_axis, Cheese)
                        self.emCimaQueijo = False
                        self.moveRight(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(pos_atual, self.y_axis, Bone)
                        self.emCimaOsso = False
                        self.moveRight(init, self, True)
                        init.mapInsert(pos_atual, self.y_axis, self.osso)
                    else:
                        self.moveRight(init, self, False)
            else:
                self.trocaDir()
        elif dir == 'UP':
            pos_atual = self.y_axis
            prox_pos = pos_atual - 1
            #prox_pos = self.y_axis - self.size

            item_prox_pos = init.get_map_item(self.x_axis, prox_pos)
            if prox_pos > 0:
                if isinstance(item_prox_pos , Wall) or isinstance(item_prox_pos , Door):
                    self.trocaDir()
                elif isinstance(item_prox_pos , Player):
                    if item_prox_pos.modoCachorro:
                        self.reset(init)
                    else:
                        init.vida -= 1
                        item_prox_pos.reset(init)
                        self.moveUp(init, self, False)
                elif isinstance(item_prox_pos , Cat):
                    self.trocaDir()
                    item_prox_pos.trocaDir()
                    # troca direção
                elif isinstance(item_prox_pos , Bone):
                    
                    if self.emCimaQueijo:
                        #init.mapInsert(self.x_axis, pos_atual, Cheese)
                        self.emCimaQueijo = False
                        self.moveUp(init, self, True)
                    else:
                        self.moveUp(init, self, False)
                    self.emCimaOsso = True
                    self.osso = item_prox_pos
                elif isinstance(item_prox_pos , Cheese):
                    if self.emCimaQueijo:
                        self.moveUp(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(self.x_axis, pos_atual, Bone)
                        self.emCimaOsso = False
                        self.moveUp(init, self, True)
                    else:
                        self.moveUp(init, self, False)
                    self.emCimaQueijo = True
                    self.queijo = item_prox_pos
                elif not item_prox_pos:
                    if self.emCimaQueijo:
                        #init.mapInsert(self.x_axis, pos_atual, Cheese)
                        self.emCimaQueijo = False
                        self.moveUp(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(self.x_axis, pos_atual, Bone)
                        self.emCimaOsso = False
                        self.moveUp(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.osso)
                    else:
                        self.moveUp(init, self, False)
            else:
                self.trocaDir()
        elif dir == 'DOWN':
            #prox_pos = self.y_axis + 1
            pos_atual = self.y_axis
            #prox_pos = self.y_axis + self.size
            prox_pos = pos_atual + 1


            item_prox_pos = init.get_map_item(self.x_axis, prox_pos)
            if prox_pos < init.alt:
                if isinstance(item_prox_pos , Wall) or isinstance(item_prox_pos , Door):
                    self.trocaDir()

                elif isinstance(item_prox_pos , Player):
                    if item_prox_pos.modoCachorro:
                        self.reset(init)
                    else:
                        init.vida -= 1
                        item_prox_pos.reset(init)
                        self.moveDown(init, self, False)

                elif isinstance(item_prox_pos , Cat):
                    self.trocaDir()
                    item_prox_pos.trocaDir()
                    # troca direção
                elif isinstance(item_prox_pos , Bone):
                    if self.emCimaQueijo:
                        #init.mapInsert(self.x_axis, pos_atual, Cheese)
                        self.emCimaQueijo = False
                        self.moveDown(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)
                    else:
                        self.moveDown(init, self, False)
                    self.emCimaOsso = True
                    self.osso = item_prox_pos
                elif isinstance(item_prox_pos , Cheese):
                    if self.emCimaQueijo:
                        #init.mapInsert(self.x_axis, pos_atual, Cheese)
                        self.moveDown(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(self.x_axis, pos_atual, Bone)
                        self.emCimaOsso = False
                        self.moveDown(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)
                    else:
                        self.moveDown(init, self, False)

                    self.emCimaQueijo = True
                    self.queijo = item_prox_pos
                elif not item_prox_pos:
                    if self.emCimaQueijo:
                        #init.mapInsert(self.x_axis, pos_atual, Cheese)
                        self.emCimaQueijo = False
                        self.moveDown(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.queijo)

                    elif self.emCimaOsso:
                        #init.mapInsert(self.x_axis, pos_atual, Bone)
                        self.emCimaOsso = False
                        self.moveDown(init, self, True)
                        init.mapInsert(self.x_axis, pos_atual, self.osso)
                    else:
                        self.moveDown(init, self, False)
            self.trocaDir()
        return init
    
    def trocaDir(self):
        if self.dir == 'LEFT':
            self.dir = 'UP'
        elif self.dir == 'RIGHT':
            self.dir = 'DOWN'
        elif self.dir == 'UP':
            self.dir = 'RIGHT'
        elif self.dir == 'DOWN':
            self.dir = 'LEFT'

    def autoMove(self, init):
        x_axis_player = init.player.x_axis
        y_axis_player = init.player.y_axis
        #print(x_axis_player, y_axis_player, self.x_axis, self.y_axis)
        distancia = (self.x_axis - x_axis_player)^2 + (self.y_axis - y_axis_player)^2
        
        # TENTA IR PARA ESQ
        dis_esq = (self.x_axis-1 - x_axis_player)^2 + (self.y_axis - y_axis_player)^2
        item_esq = init.get_map_item(self.x_axis-1, self.y_axis)
        # TENTA IR PARA DIR
        dis_dir = (self.x_axis+1 - x_axis_player)^2 + (self.y_axis - y_axis_player)^2
        item_dir = init.get_map_item(self.x_axis+1, self.y_axis)
        # TENTA IR PARA CIMA
        dis_cima = (self.x_axis - x_axis_player)^2 + (self.y_axis-1 - y_axis_player)^2
        item_cima = init.get_map_item(self.x_axis, self.y_axis-1)
        # TENTA IR PARA BAIXO
        dis_baixo = (self.x_axis - x_axis_player)^2 + (self.y_axis+1 - y_axis_player)^2
        item_baixo = init.get_map_item(self.x_axis, self.y_axis+1)
        # ESCOLHE DIR Q DIMINUI DISTANCIA ATÉ JOGADOR
        dis_esq = abs(distancia-dis_esq)
        dis_dir = abs(distancia-dis_dir)
        dis_cima = abs(distancia-dis_cima)
        dis_baixo = abs(distancia-dis_baixo)

        if dis_esq < distancia and not isinstance(item_esq, Wall) and not isinstance(item_esq, Door) and not isinstance(item_esq, Cat):
            self.dir = 'LEFT'
        elif dis_dir < distancia and not isinstance(item_dir, Wall) and not isinstance(item_dir, Door) and not isinstance(item_dir, Cat):
            self.dir = 'RIGHT'
        elif dis_cima < distancia and not isinstance(item_cima, Wall) and not isinstance(item_cima, Door) and not isinstance(item_cima, Cat):
            self.dir = 'UP'
        elif dis_esq < distancia and not isinstance(item_baixo, Wall) and not isinstance(item_baixo, Door) and not isinstance(item_baixo, Cat):
            self.dir = 'DOWN'

        self.move(init)


#--------------------------------------------------------------------------
#    OBJETO PLAYER
#--------------------------------------------------------------------------
class Player(Character):
    def __init__(self, x_axis, y_axis, size):
        Character.__init__(self, x_axis, y_axis, size)
        self.color = pygame.Color('#d62839')
        self.image = 'img/mouse.png'
        self.modoCachorro = False

    def reset(self, init):
        # Verifica situação de spawnkill
        item_pos_spawn = init.get_map_item(self.x0_axis, self.y0_axis)
        
        if item_pos_spawn != None and item_pos_spawn.x_axis == self.x0_axis and item_pos_spawn.y_axis == self.y0_axis:
            init.mapUpdate(self.x_axis, self.y_axis, self.x0_axis, self.y0_axis+2, self, False)
            init.player.y_axis = init.player.y0_axis+2
        else:
            init.mapUpdate(self.x_axis, self.y_axis, self.x0_axis, self.y0_axis, self, False)
            init.player.y_axis = init.player.y0_axis    
        
        init.player.x_axis = init.player.x0_axis
        

    def move(self, init, dir):
        if dir == 'LEFT':
            pos_atual = self.x_axis
            prox_pos = pos_atual - 1
            
            if prox_pos > 0:
                item_prox_pos = init.get_map_item(prox_pos, self.y_axis)
                if isinstance(item_prox_pos , Cat):
                    if self.modoCachorro:
                        item_prox_pos.reset(init)
                        init.placar += 100
                        self.moveLeft(init, self, False)
                    else:
                        #print('-1 vida')
                        init.vida -= 1
                        self.reset(init)
                elif isinstance(item_prox_pos , Bone):
                    self.moveLeft(init, self, False)
                    if self.modoCachorro:
                        init.startTime = pygame.time.get_ticks()
                    else:
                        ativarModoCachorro(init, True)
                    init.placar += 10
                elif isinstance(item_prox_pos , Cheese):
                    init.placar += 1
                    self.moveLeft(init, self, False)
                    init.queijos += 1
                    #print("QUEIJO")
                elif not item_prox_pos:
                    #init.mapUpdate(self.x_axis, self.y_axis, prox_pos, self.y_axis, self.personagem_id['RATO'], False)
                    #self.x_axis = prox_pos
                    self.moveLeft(init, self, False)

        elif dir == 'RIGHT':
            pos_atual = self.x_axis
            prox_pos = pos_atual + 1
            
            if prox_pos < init.larg:
                item_prox_pos = init.get_map_item(prox_pos, self.y_axis)
                if isinstance(item_prox_pos , Cat):
                    if self.modoCachorro:
                        #print('gato eliminado')
                        
                        item_prox_pos.reset(init)
                        init.placar += 100
                        self.moveRight(init, self, False)
                        # reseta gato
                        # add ponto para rato
                    else:
                        #print('-1 vida')
                        init.vida -= 1
                        self.reset(init)
                        # reseta rato
                        # diminui sua vida
                        # se não há mais vidas, fim jogo 
                #elif item_prox_pos == self.item_id['OSSO']:
                elif isinstance(item_prox_pos , Bone):
                    self.moveRight(init, self, False)
                    init.placar += 10
                    if self.modoCachorro:
                        init.startTime = pygame.time.get_ticks()
                    else:
                        ativarModoCachorro(init, True)
                if isinstance(item_prox_pos , Cheese):
                    init.placar += 1
                    self.moveRight(init, self, False)
                    init.queijos += 1
                elif not item_prox_pos:
                    self.moveRight(init, self, False)
        elif dir == 'UP':
            pos_atual = self.y_axis
            prox_pos = pos_atual - 1

            item_prox_pos = init.get_map_item(self.x_axis, prox_pos)
            if prox_pos > 0:
                if isinstance(item_prox_pos , Cat):
                    if self.modoCachorro:
                        #print('gato eliminado')
                        
                        item_prox_pos.reset(init)
                        init.placar += 100
                        self.moveUp(init, self, False)
                        # reseta gato
                        # add ponto para rato
                    else:
                        #print('-1 vida')
                        init.vida -= 1
                        self.reset(init) 
                elif isinstance(item_prox_pos , Bone):
                    # elimina osso
                    init.placar += 10
                    self.moveUp(init, self, False)
                    if self.modoCachorro:
                        init.startTime = pygame.time.get_ticks()
                    else:
                        ativarModoCachorro(init, True)
                    #print('modo cachorro ativado')
                elif isinstance(item_prox_pos , Cheese):
                    init.placar += 1
                    self.moveUp(init, self, False)
                elif not item_prox_pos:
                    self.moveUp(init, self, False)
                    init.queijos += 1
        elif dir == 'DOWN':
            prox_pos = self.y_axis + 1

            item_prox_pos = init.get_map_item(self.x_axis, prox_pos)
            #print('down p p: ', item_prox_pos)
            if prox_pos < init.alt:
                if isinstance(item_prox_pos , Cat):
                    if self.modoCachorro:
                        item_prox_pos.reset(init)
                        init.placar += 100
                        self.moveDown(init, self, False)
                        # reseta gato
                        # add ponto para rato
                    else:
                        #print('-1 vida')
                        init.vida -= 1
                        self.reset(init)
                elif isinstance(item_prox_pos , Bone):
                    # elimina osso
                    init.placar += 10
                    self.moveDown(init, self, False)
                    if self.modoCachorro:
                        init.startTime = pygame.time.get_ticks()
                    else:
                        ativarModoCachorro(init, True)
                    #print('modo cachorro ativado')
                elif isinstance(item_prox_pos , Cheese):
                    self.moveDown(init, self, False)
                    init.placar += 1
                    init.queijos += 1
                elif not item_prox_pos:
                    self.moveDown(init, self, False)
        return init

pygame.time.get_ticks()
def ativarModoCachorro(init, activate = False):
    pygame.mixer.music.load('music/modoCachorro.mp3')
    pygame.mixer.music.play()
    init.startTime = pygame.time.get_ticks()
    init.player.modoCachorro = True

def desativarModoCachorro(init):
    pygame.mixer.music.load('music/game.mp3')
    pygame.mixer.music.play()
    init.player.modoCachorro = False
    init.startTime = 0
    init.actualTime = 0
