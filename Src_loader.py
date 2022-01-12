# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')
import os, sys

def load_img(img):
    img = pygame.image.load(img)
    img = img.convert_alpha()
    return img

def load_image(name, colorkey=None):
    fullname = os.path.join('src', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print('Cannot load image:', name, e)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('src', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', wav)
        raise SystemExit
    return sound





def cropimg(img, rect):

    subImg = img.subsurface(rect)


    return subImg 


