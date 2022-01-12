# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
from tools import *
import tools
import numpy as np

class AI(object):
    
    def __init__(self):
        self.name = 'AI'
        self.actionSpace = actionbinding

    def get_action(self):
        key = np.random.randint(0,7)
        return key

    def get_position(self,target):

        return

    def move_to_target(self,position):

        return
