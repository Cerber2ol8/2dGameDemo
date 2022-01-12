# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *

class MouseIcon(pygame.sprite.Sprite):
    """指针图标"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('mouse.tga', -1)
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = [0,0]
        self.xy = [0,0]
        self.punching = 0
        self.whiff_sound = load_sound('whiff.wav')
        self.punch_sound = load_sound('punch.wav')
        self.down_img, rect= load_image('mouse_down.tga', -1)
        self.up_img, rect= load_image('mouse_up.tga', -1)
    def update(self):
        "根据鼠标位置移动图标"
        self.pos = pygame.mouse.get_pos()
        self.rect.midtop = self.pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        "如果拳头与目标发生碰撞，则返回True"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        "调用函数拉回拳头"
        self.punching = 0


