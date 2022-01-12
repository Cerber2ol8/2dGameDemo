# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *

class enermy(pygame.sprite.Sprite):
    """敌人父类"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = None
        self.damage = 0
        self.position = (0,0)

