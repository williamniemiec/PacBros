# -*- coding: utf-8 -*-

#==========================================================================
#                                  PACBROS
#==========================================================================
#--------------------------------------------------------------------------
#    IMPORTS 
#--------------------------------------------------------------------------
import pygame
from colors import *


#--------------------------------------------------------------------------
#    OBJETO ITEM
#--------------------------------------------------------------------------
class Item:
    def __init__(self, x_axis, y_axis, size, color = WHITE):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.size = size
        self.color = color


#--------------------------------------------------------------------------
#    OBJETO CHEESE
#--------------------------------------------------------------------------
class Cheese(Item):
    def __init__(self, x_axis, y_axis, size):
        Item.__init__(self, x_axis, y_axis, size)
        self.color = pygame.Color('#e5e500')
        self.image = 'img/cheese.png'


#--------------------------------------------------------------------------
#    OBJETO WALL
#--------------------------------------------------------------------------
class Wall(Item):
    def __init__(self, x_axis, y_axis, size):
        Item.__init__(self, x_axis, y_axis, size)
        self.color = pygame.Color('#0000FF')


#--------------------------------------------------------------------------
#    OBJETO BONE
#--------------------------------------------------------------------------
class Bone(Item):
    def __init__(self, x_axis, y_axis, size):
        Item.__init__(self, x_axis, y_axis, size)
        self.color = pygame.Color('#e8e8e8')
        self.image = 'img/bone.png'


#--------------------------------------------------------------------------
#    OBJETO DOOR
#--------------------------------------------------------------------------
class Door(Item):
    def __init__(self, x_axis, y_axis, x2_axis, y2_axis, size):
        Item.__init__(self, x_axis, y_axis, size)
        self.x2_axis = x2_axis
        self.y2_axis = y2_axis
        self.color = pygame.Color('#00afaf')
        self.moved = False
        self.emCimaQueijo = False
        self.queijo = None

    # Move uma porta
    def move(self, init):
        if not self.moved:
            # Verifica se porta não vai ser posta na mesma posição do jogador
            if self.x2_axis != init.player.x_axis or self.y2_axis != init.player.y_axis:
                # Verifica se porta não vai ser posta na mesma posição de um gato
                for cat in init.list_cats:
                    if cat.x_axis == self.x2_axis and cat.y_axis == self.y2_axis:
                        return
                
                proxPos = init.get_map_item(self.x2_axis, self.y2_axis)
                # Verifica se porta vai ser posta na mesma posição de um queijo
                if isinstance(proxPos, Cheese):
                    self.emCimaQueijo = True
                    self.queijo = proxPos

                self.moved = True
                init.mapUpdate(self.x_axis, self.y_axis, self.x2_axis, self.y2_axis, self, False)
        else:
            # Verifica se porta não vai ser posta na mesma posição do jogador
            if self.x_axis != init.player.x_axis or self.y_axis != init.player.y_axis:  
                # Verifica se porta não vai ser posta na mesma posição de um gato
                for cat in init.list_cats:
                    if cat.x_axis == self.x_axis and cat.y_axis == self.y_axis:
                        return

                self.moved = False
                init.mapUpdate(self.x2_axis, self.y2_axis, self.x_axis, self.y_axis, self, False)

                # Verifica se porta estava anteriormente sobre um queijo (se sim, coloca ele de volta)
                if self.emCimaQueijo:
                    init.mapInsert(self.x2_axis, self.y2_axis, self.queijo)
                    self.queijo = None
                    self.emCimaQueijo = False