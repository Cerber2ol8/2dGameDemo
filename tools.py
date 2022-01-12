# -*- coding: utf-8 -*-
import pygame as pg
import sys
import numpy as np

DEBUG = False
res = (1024,768)
keybinding = {
    'left':pg.K_LEFT,
    'right':pg.K_RIGHT,
    'down':pg.K_DOWN,
    'up':pg.K_UP,
    'attack':pg.K_x,
    'jump':pg.K_c,
    'pickOn':pg.K_z,
    'swordSkill':pg.K_a,
    'sub_addNpc':pg.K_p,
    'sub_npcAttack':pg.K_F1,
    'sub_debug':pg.K_F2,
    'sub_bag':pg.K_b
}

actionbinding = {
    'left':0,
    'right':1,
    'down':2,
    'up':3,
    'attack':4,
    'jump':5,
    'pickOn':6,
    'swordSkill':7
}



_actionbinding = {
    'stand':0,
    'left':1,
    'right':2,
    'down':3,
    'up':4,
    'attack':5,
    'jump':6,
    'pickOn':7,
    'swordSkill':8
}

def mapActiontoKeycode(key):
    zeros = np.zeros(323).tolist()
    for action in actionbinding:
        if key == actionbinding[action]:
            if action in keybinding:
                zeros[keybinding[action]] = 1

            return zeros


position = {'left':0,'right':1}

def cutImgR(n, img):
    if img.get_width() == 3000 and img.get_height() == 300:
        subImgs = []
        for i in range(n):
            rect = (300 * i, 0, 300, 300)
            subImgs.append(img.subsurface(rect))
        return(subImgs)
    else:
        print('image size is not (3000,300)')
        sys.exit()
def cutImgL(n, img):
    if img.get_width() == 3000 and img.get_height() == 300:
        subImgs = []
        for i in range(n):
            rect = (300 * (n-i-1), 0, 300, 300)
            subImgs.append(img.subsurface(rect))
        return(subImgs)
    else:
        print('image size is not (3000,300)')
        sys.exit()

def resize(crops, n):
    """
    缩放资源尺寸
    param1: 裁剪rect列表crops
    param2: 缩放倍率
    """
    new_crops = []
    for rect in crops:
        new_rect = []
        for i in rect:
            i = int(i * n)
            new_rect.append(i)
        new_crops.append(new_rect)
    return new_crops


class t_press(object):
    def __init__(self):
        self.K_UP = 0
        self.K_DOWN = 0
        self.K_LEFT = 0
        self.K_RIGHT = 0
        self.K_x = 0
        self.K_c = 0
        self.K_z = 0
        self.K_a = 0
    def keys(self):
        return self.K_UP,self.K_DOWN,self.K_LEFT,self.K_RIGHT,self.K_x,self.K_c,self.K_z 
