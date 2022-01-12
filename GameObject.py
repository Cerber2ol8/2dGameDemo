# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *

class GameObject(pygame.sprite.Sprite):
    """
    对象体抽象类
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.name = None    #对象名
        self.image = None   #对象体图像
        self.rect = None    #对象体矩形
        self.xy = []
        self.z = 0
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0
        self.src_path = 'src/'
        try:
            self.width = self.rect.width    #矩形宽高
            self.height = self.rect.height
            self.xy = [self.width/2, self.height/2]    #矩形形心的世界坐标
            self.pos = None   #矩形形心相对在摄像机坐标系的坐标
        except:
            pass

    def update(self):
        try:
            self.rect.left = self.pos[0]
            self.rect.top = self.pos[1]
        except:
            pass
