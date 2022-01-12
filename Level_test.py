# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *
from Level import *
import tools as t
from npc import Npc
class Background(pygame.sprite.Sprite):
    def __init__(self,image,rect,mask):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.name = 'background'
        self.image, self.rect = image, rect
        self.mask = mask
        self.width = self.rect.width
        self.height = self.rect.height
        self.xy =[self.width/2,self.rect.height]
        self.z = 0
        self.pos = []
    def update(self):

        self.rect.left = self.pos[0] - self.width
        self.rect.top = self.pos[1] - self.rect.height


    def setPos(rectPos):
        self.pos = rectPospos
        pass
class Level_test(Level):
    """description of class"""
    def __init__(self):
        Level.__init__(self) 
        self.level = 'level_0'
        self.size = (3000,3000)
        self.surface = pygame.Surface(self.size)
        self.src_path = 'src'
        self.map = 'map_test'
        self.sub = None
        self.setup()
 
    def setup(self):

        #image = load_img(self.src_path + '/map/map1.jpg')
        image = load_img(self.src_path + '/level/background.png')
        rect = image.get_rect()
        image_mask = load_img(self.src_path + '/level/background_mask.png')
        image_mask = pygame.mask.from_surface(image_mask)
        self.background = Background(image, rect, image_mask)
        self.spriteGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.config()
        pass
    def loadBackground(self,screen,pos):
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]
        print(dx,dy)
        self.pos = pos
        newpos = self.background.rect.move((dx, dy))

    def sub_addNpcGroup(self,world,n):
        npcNum = n
        for i in range(npcNum):
            npc = Npc()
            npc.name = 'npc' + str(i)
            npc.dummy = False
            npc.maxHp  = 1000
            npc.hp = 1000
            world.npcGroup.add(npc)

    def sub_addNpc(self,world):
        n = len(world.npcs)
        npc = Npc()
        npc.name = 'npc' + str(n)
        npc.dummy = False
        npc.maxHp  = 1000
        npc.hp = 1000
        world.npcGroup.add(npc)