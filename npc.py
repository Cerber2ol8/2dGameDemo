# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *
from GameObject import *
import time
from tools import *
import tools
from Character import *
from AI import AI
import numpy as np
import time
position = {'left':0,'right':1}

class Npcs(Character):
    """
    npc角色
    """

    def __init__(self):
        Character.__init__(self) #call Sprite intializer
        self.interactiveEnable = True
        self.name = 'npc_'+ str(time.clock())
        self.maxHp = 9999
        self.hp = 9999
        self.xy = [700,600]
        self.position = position['left']

    def interactive(self):
        if self.interactiveEnable:
            pass

        pass

class Npc(Character):
    """
    npc角色
    """
    __slots__ = ['name','image','mask',
                 'rect','width','height','frame','ticks',
                 'pos','xy','z','actionSpace','state','lastState',
                 'actComplete','allowControl','allowJump','doublePress','doubleAttack','hurtToFall','position','stickPosition',
                 'next_state','speed','walkSpeed','runSpeed','dizzy','move_direction','atkSpeed','jumpSpeed','jumpHeight',
                 'jumpHigher','floated','gAccel','playRate','src_path','printState','isCout','repeat','maxHp','hp','lastHp',
                 'maxEnergy','energy','lastEnergy','isDead','lossingHp','lossingEnergy','phyAttack','damaged','damageList','interactiveEnable'
                 'keys']
    def __init__(self):
        Character.__init__(self) #call Sprite intializer
        self.name = 'target0'
        self.maxHp = 500
        self.hp = 500
        #self.AI = AI()
        self.keys = 0
        self.xy = [700,600]
        self.pos = self.xy
        self.position = position['left']
        self.dummy = True
    def x(self):
        if not self.dummy:
            key = np.random.randint(0,7)
        else:
            self.hp = 500
            key = 0
        
        return key
    def get_random_action(self):
        return self.x()

    def get_action(self,target):

        return
    def get_distence(self,target):
        dx = self.xy[0] - target.xy[0]
        dy = self.xy[1] - target.xy[1]
        return dx,dy

    def move_to_target(self,target):
        dx,dy = self.get_distence(target)
        if self.x_vel > 0 and dx > 0 or self.x_vel < 0 and dx < 0:
            self.x_vel = -self.x_vel
        if self.y_vel > 0 and dy > 0 or self.y_vel < 0 and dy < 0:
            self.y_vel = self.y_vel

        if self.state == self.actionSpace['walk'] or self.state == self.actionSpace['run']:
            if dx > 0:
                self.position = position['left']
            else:
                self.position = position['right']

            
    def update(self, dt):

        self.dt = dt 

        self.ticks += 1
        if self.ticks % self.playRate == 0 and self.printState:  
            print('frame:{},state:{}'.format(self.frame,self.state))

        #print(self.state)
        self.check_is_dead()
        #self.check_is_floated()
        self.check_on_the_ground()
        #self.check_to_allow_jump()
        keys = tools.mapActiontoKeycode(self.keys)
        self.handle_state(keys)

        self.updateHeight(self.z_vel,self.z, self.gAccel, self.dt)
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        self.actComplete = False
        

        self.update_mask()
        self.animation()
        self.ticks += 1
        if self.frame == 0:
            self.keys = self.get_random_action()

        if int(self.ticks % self.playRate) == 0:

            self.frame += 1

    def showDamage(self):

        pass

    def animation(self):
        """
            根据当前帧更新精灵image
        """
        n = self.frame
        if self.position == position['right']:
            #if self.state == self.actionSpace['con_combo']:
            #    print(n)
            if n < len(self.right_frames[self.state]):
                self.image = self.right_frames[self.state][n]
            else:
                self.frame -= 1
        else:

            if n < len(self.left_frames[self.state]):
                self.image = self.left_frames[self.state][n]
            else:
                self.frame -= 1