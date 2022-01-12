# -*- coding: utf-8 -*-
import os, sys, gc
import pygame
from pygame.locals import *
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')
from GameWorld import *
from Src_loader import *
from Character import *
from MouseIcon import *
from Camera import *
from Level_test import *
from Enermy import *
from pygame.transform import scale
from interface import *
from tools import resize
from tools import *
from system import System

import json


class Editor(object):
    #地图(边界）编辑器
    def __init__(self, world):
        self.world = world
        self.resolution = (1440, 720)
        self.mode = 0 
        self.button_imgs = []
        self.buttons = []
        self.reference_xLines = []
        self.reference_yLines = []
        self.button_pos = []
        self.src = []
        self.imgs = []
        self.sounds = []
        self.lines = []
        self.ui_path = 'src/ui/'
        self.data_path = 'data/'
        self.level = 'level_0'
        self.map = 'map_test'
        self.content = {'level':self.level,'border':self.lines}
        self.src_loader()

        self.resetPos = [0,0]

        self.drawLine = False
        self.editBorder = False
        self.recordBorder = False
        self.loadBorder = False
        self.debug = True
        self.showBorder = False

        self.init()
        self.choose_map()
    def init(self):
        x = self.resolution[0]
        y = self.resolution[1]
        grid_x = int(y/100)
        grid_y = int(x/100)
        for i in range(grid_x + 1):
            self.reference_xLines.append(((0, 100 * i),(x, 100 * i)))
        for i in range(grid_y + 1):
            self.reference_yLines.append(((100 * i, 0),(100 * i, y)))

        #print(self.reference_yLines)
        self.add_buttons(self.button_imgs[2],(1300,100),0)
        self.add_buttons(self.button_imgs[2],(1300,200),1)
        self.add_buttons(self.button_imgs[2],(1300,300),2)
        self.add_buttons(self.button_imgs[2],(1300,400),3)
        self.add_buttons(self.button_imgs[2],(1300,500),4)
        self.add_buttons(self.button_imgs[2],(1300,600),5)
        self.add_buttons(self.button_imgs[2],(1200,100),6)

    def choose_map(self):
        self.world.level.map = self.map
    def bound_function(self):
        pass
    def update(self, dt):
        self.update_config()
        self.draw_controls()
        if self.drawLine:
            self.draw_reference_line()

        if self.editBorder:
            self.world.editBorderOn()
        else:
            self.world.editBorderOff()

        if self.recordBorder:
            self.record_line()
            self.buttons[2].isDown = False

        if self.loadBorder:
            self.load_border()
            self.buttons[3].isDown = False

        if self.saveBorder:
            self.save_border()
            self.buttons[4].isDown = False

        if self.debug:
            tools.DEBUG = True

        else:
            tools.DEBUG = False
  

        if self.reset:
            self.reset_player()
            self.buttons[6].isDown = False

    def update_config(self):
        self.drawLine = self.buttons[0].isDown
        self.editBorder = self.buttons[1].isDown
        self.recordBorder = self.buttons[2].isDown
        self.loadBorder = self.buttons[3].isDown
        self.saveBorder = self.buttons[4].isDown
        self.debug = self.buttons[5].isDown
        self.reset = self.buttons[6].isDown

    def add_buttons(self,img, pos, buttonType):
        """
        添加操作按钮
        param1:按钮图片(imgUp,imgDown)
        param2:按钮位置pos
        param3:按钮类型: 0:网格线开关 1:编辑边界线 2:记录边界线 3:读取边界线 4：保存边界线 5:debug模式 6:重置
        """

        if buttonType == 0:
            button_drawLine = Button(img[0],img[1],pos,id=0, name='button_drawLine',text = 'grid')
            self.buttons.append(button_drawLine)
        if buttonType == 1:
            button_drawBorder = Button(img[0],img[1],pos,id=1,name='button_drawBorder',text='Draw Border')
            self.buttons.append(button_drawBorder)
        if buttonType == 2:
            button_recordBorder = Button(img[0],img[1],pos,id=2,name='button_recordBorder',text='Record Borde')
            self.buttons.append(button_recordBorder)
        if buttonType == 3:
            button_loadBorder = Button(img[0],img[1],pos,id=3,name='button_loadBorder',text='Load Border')
            self.buttons.append(button_loadBorder)
        if buttonType == 4:
            button_saveBorder = Button(img[0],img[1],pos,id=4,name='button_saveBorder',text='Save Border')
            self.buttons.append(button_saveBorder)
        if buttonType == 5:
            button_debug = Button(img[0],img[1],pos,id=5,name='button_debug',text='debug')
            self.buttons.append(button_debug)
        if buttonType == 6:
            button_reset = Button(img[0],img[1],pos,id=6,name='button_reset',text='reset')
            self.buttons.append(button_reset)

        


    def draw_reference_line(self):
        
        for line in self.reference_xLines:
            pygame.draw.line(self.world.camera.screen,(255,0,0),line[0],line[1],1)
        for line in self.reference_yLines:
            pygame.draw.line(self.world.camera.screen,(255,0,0),line[0],line[1],1)

    def draw_controls(self):
        """
        画出控件
        """

        #画出按钮
        if len(self.buttons) > 0:
            for button in self.buttons:
                button.render(self.world.camera.screen)
            pass

        pass
    def record_line(self):
        """
        记录画线操作
        """
        self.lines = self.world.lines

        print(self.lines)
        pass

    def record_rect(self):
        """
        记录画框操作
        """
        pass
    def is_saved(self):
        if os.path.exists(self.data_path + 'level/'+ self.level + '.level'):
            return True
        else:
            return False
    def load_border(self):
        if self.is_saved:
            with open(self.data_path + 'level/' + self.level + '.level','r') as f:
                dict = json.load(f)
                print(dict[self.map]['border'])
                self.world.lines = dict[self.map]['border']
        else:
            print('没有可读取的数据')

    def reset_player(self):

        """method1
        """

        #del self.world.player
        #del self.world.playerGroup
        #del self.world.c_group
        #gc.collect()
        #self.world.player = Character()
        #self.world.playerGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        #self.world.playerGroup.add(self.world.player)
        #self.world.c_group = pygame.sprite.Group()
        #self.world.c_group.add(self.world.player.volumeBox)
        #self.world.player.pos = [1000,1000]
        #self.world.camera.Cxy = self.world.player.xy

        """method2
        """
        self.world.player.pos = [1000,1000]
        self.world.camera.Cxy = self.world.player.pos
        self.world.player.maxHp = 500
        self.world.player.hp = 500
        self.world.player.lastHp = self.world.player.hp
        self.world.player.maxEnergy = 200
        self.world.player.energy = 200
        self.world.player.lastEnergy = self.world.player.energy

        self.world.player.isDead = False
        self.world.player.lossingHp = False
        self.world.player.lossingEnergy = False
        self.world.player.state = self.world.player.actionSpace['stand']

        pass
    def save_border(self):
        if not self.is_saved():
            self.content = {self.map:{'border':self.lines}}
            if self.lines != []:
                self.content = {self.map:{'border':self.lines}}
                print(self.lines)
                with open(self.data_path + 'level/'+ self.level + '.level','w') as f:
                    json.dump(self.content, f)
            else:
                print('border为空')
        else:
            with open(self.data_path + 'level/'+ self.level + '.level','r') as f:
                dict = json.load(f)
            dict[self.map] = {'border':self.lines}
            with open(self.data_path + 'level/'+ self.level + '.level','w') as f:
                json.dump(dict, f)

    def src_loader(self):
        """
        资源导入
        """
        n = 0.3
        img = load_img(self.ui_path + 'button.png')
        img = pygame.transform.scale(img,(300,300))
        img_down = load_img(self.ui_path + 'button_down.png')
        img_down = pygame.transform.scale(img_down,(300,300))
        crops = [(76,140,215,200),(300,140,300,140),(550,140,380,200),(70,400,550,190),(650,390,140,210),(795,390,140,210),(93,666,840,193)]
        crops = resize(crops,n)
        for crop in crops:
            button_img = img.subsurface(crop)
            button_down_img = img_down.subsurface(crop)
            self.button_imgs.append((button_img,button_down_img))


def start():
    pygame.init()
    pygame.display.set_caption('Border Editor')
    pygame.mouse.set_visible(0)
    #pygame.key.set_repeat(20)
    world = GameWorld()
    #world.setup()
    camera = Camera([0,-768],(1440, 720))

    icon = MouseIcon()
    player = Character()
    level = Level_test()
    system = System()
    world.setup(level,player,camera,system)
    world.mouseIcon.add(icon)
    editor = Editor(world)
    #world.level = Level_test()

    #world.camera.screen.set_clip((0, 0,world.camera.area[0] ,world.camera.area[1] ))
    #view_rect = Rect(0, 0, world.camera.area[0], world.camera.area[1])
    #scale(world.level.background.image.subsurface(view_rect),
    #     (world.camera.area[0], world.camera.area[1]),
    #world.camera.screen.subsurface(world.camera.screen.get_clip()))
    pygame.display.flip()

    clock = pygame.time.Clock()
    
    t = time.time()
    while 1:
        clock.tick(60)

        dt = time.time() - t
        t = time.time()

        world.update(dt)
        world.camera.render(world.render)
        editor.update(dt)
        

        #camera.render(pygame.sprite.RenderPlain(icon,world.sprites))
    sys.exit()


if __name__ == '__main__':
    start()
    exit()