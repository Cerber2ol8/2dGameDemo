# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *
import json
import os

class Level(object):
    """游戏关卡"""
    def __init__(self):
        self.level = None
        self.background = pygame.sprite.Sprite()
        self.map = None

    def load(self):
        pass

    def loadBackground(self):
        pass

    def loadObj(self):
        pass

    def loadWav(self):
        pass



    def load_border(self):
        if self.is_saved():
            with open('data/level/'+ self.level + '.level','r') as f:
                dict = json.load(f)
                lines = dict[self.map]['border']
                return lines
        else:
            print('没有可读取的数据')
            return []

    def is_saved(self):
        if os.path.exists('data/level/'+ self.level + '.level'):
            return True
        else:
            return False

    def config(self):
        self.load_border()