# -*- coding: utf-8 -*-
import sys,gc
import pygame
import math
from pygame.locals import *
from Level_test import *
from MouseIcon import *
from Camera import *
from Level_test import *
from Enermy import *
from npc import *
from pygame.transform import scale
from tools import *
from interface import Textbox
from system import System

import time




class GameWorld(object):
    def __init__(self):
        self.level = None
        self.load = False
        self.counts = 0 # world alive ticks
        self.gravity = 9.8
        self.xy = (0,0)
        self.rotation = 0
        self.dt = 0
        self.camera = None
        self.mouseIcon = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.bgGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.playerGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.npcGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.uiGroup = pygame.sprite.LayeredUpdates(pygame.sprite.Group())
        self.render = pygame.sprite.LayeredUpdates(self.bgGroup,
                                                   self.playerGroup,
                                                   self.npcGroup,
                                                   self.mouseIcon,
                                                   self.uiGroup)
        self.player = None
        self.now_press = t_press()
        self.last_press = t_press()
        self.keys = pygame.key.get_pressed()
        self.point1 = None
        self.point2 = None
        self.lines = []
        self.Wb = []
        
        self.damageList = []

        self.sub = None
        self.textbox = None

        self.npcs = None
        self.debug = t.DEBUG
        self.editBorder = False

        self.toReset = False

        self.system = None
        self.tracker = None
        self.spriteTracker = None


    def draw_health(self):
        """画UI中玩家的生命值条"""
        x = 40
        y = 40
        screen = self.camera.screen
        """画血条边框"""
        pygame.draw.rect(screen, (255,255,255),
                         (x - 2, y - 1, self.player.maxHp + 3, 15 + 2),1)
        percent = self.player.hp / self.player.maxHp

        """血量流失槽"""
        if self.player.lossingHp:
            if self.player.lastHp != self.player.hp:
                pygame.draw.rect(screen, (240,100,0),
                             (x, y, self.player.lastHp, 15))
                self.player.lastHp -= 2 
            else:
                self.player.lossingHp = False
        clr = (255,52,0)
        if percent <= 0.4:
            clr = (255,60,0)
        elif percent <= 0.2:
            clr = (255,20,0)
        elif percent <= 0.1:
            clr = (255,0,0)
        """画血量条"""
        pygame.draw.rect(screen, clr,
                         (x, y, self.player.hp, 15))


    def draw_energy(self):
        """画UI中玩家的精力值条"""
        x = 40
        y = 80
        screen = self.camera.screen
        """画精力条边框"""
        pygame.draw.rect(screen, (255,255,255),
                         (x - 2, y - 1, self.player.maxEnergy + 3, 15 + 2),1)
        percent = self.player.energy / self.player.maxEnergy

        """精力流失槽"""
        if self.player.lossingEnergy:
            if self.player.lastEnergy != self.player.energy:
                pygame.draw.rect(screen, (240,100,0),
                             (x, y, self.player.lastEnergy, 15))
                self.player.lastEnergy -= 2 
            else:
                self.player.lossingEnergy = False
        clr = (0,128,0)
        if percent <= 0.4:
            clr = (255,60,0)
        elif percent <= 0.2:
            clr = (255,20,0)
        elif percent <= 0.1:
            clr = (255,0,0)

        """画精力条"""
        pygame.draw.rect(screen, clr,
                         (x, y, self.player.energy, 15))


    def draw_monster_health(self,monster):
        """画怪物头顶的生命值条"""
        x = monster.pos[0] + monster.rect.width * 0.3
        y = monster.pos[1] + monster.rect.height* 0.5
        screen = self.camera.screen
        l = 100
        w = 5
        """画血条边框"""
        pygame.draw.rect(screen, (255,255,255),
                         (x - 2, y - 1, l + 3, w + 2),1)
        percent = monster.hp / monster.maxHp
        ratio = percent * l
        clr = (255,128,0)
        if percent <= 0.3:
            clr = (255,60,0)
        elif percent <= 0.1:
            clr = (255,20,0)

        """血量流失槽"""
        if monster.lossingHp:
            if monster.lastHp != monster.hp:
                pygame.draw.rect(screen, (240,100,0),
                             (x, y, ratio, w))
                monster.lastHp -= 2 * ratio
            else:
                monster.lossing = False


        """画血量条"""
        pygame.draw.rect(screen, clr,
                         (x, y, ratio, w))

        """画血量网格"""
        hp_each_gird = 200
        n = int(monster.maxHp / hp_each_gird)
        grid = int(l / n)
        for i in range(n):
            if not i == 0 and i * hp_each_gird <= monster.hp:
                pygame.draw.line(screen,(255,255,255),
                                 (x + i * grid, y),(x + i * grid, y + w), 1)

        

    def editBorderOn(self):
        self.editBorder = True
    def editBorderOff(self):
        self.editBorder = False
    def deleteBorder(self):
        if len(self.lines) > 0:
            self.lines.remove(self.lines[len(self.lines) - 1])
        else:
            print('边界线少于一条')
            return False
    def draw_rect(self,sprites):
        for sprite in sprites:
            pygame.draw.rect(self.camera.screen,(0,0,255),sprite.rect,1)
        pass
    def draw_border(self):
        mouse = self.mouseIcon.sprites()[0]
        if tools.DEBUG and self.editBorder:
            print('drawing lines')
            if self.point1 == None:
                self.point1 = self.__getXyfromPos(pygame.mouse.get_pos())
            elif self.point2 == None:
                self.point2 = self.__getXyfromPos(pygame.mouse.get_pos())
                #pos1 = self.__getPosfromXy(self.point1)
                #pos2 = self.__getPosfromXy(self.point2)
                self.lines.append((self.point1,self.point2))
                self.__getLine(self.point1,self.point2)
                self.point1 = self.point2
                self.point2 = None
                #print(self.Wb)
        else:
            self.point1 = None
            self.point2 = None
            


    def keySub(self,event):
        """按键事件"""
        if event.type == KEYDOWN:
            #print(self.last_press.keys())

            if event.key == K_ESCAPE:
                sys.exit()
                pass
            else:
                
                if event.key == keybinding['up']:
                    self.now_press.K_UP = pygame.time.get_ticks()
                    self.input_judge(self.now_press.K_UP ,self.last_press.K_UP)
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_UP = self.now_press.K_UP

                elif event.key == keybinding['down']:
                    self.now_press.K_DOWN = pygame.time.get_ticks()
                    self.input_judge(self.now_press.K_DOWN ,self.last_press.K_DOWN)
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_DOWN = self.now_press.K_DOWN

                elif event.key == keybinding['left']:
                    self.now_press.K_LEFT = pygame.time.get_ticks()
                    self.input_judge(self.now_press.K_LEFT ,self.last_press.K_LEFT)
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_LEFT = self.now_press.K_LEFT

                elif event.key == keybinding['right']:
                    self.now_press.K_RIGHT = pygame.time.get_ticks()
                    self.input_judge(self.now_press.K_RIGHT ,self.last_press.K_RIGHT)
                    #print(self.now_press.K_RIGHT ,self.last_press.K_RIGHT)
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_RIGHT = self.now_press.K_RIGHT

                elif event.key == keybinding['attack']:
                    self.now_press.K_x = pygame.time.get_ticks()
                    self.input_judge(self.now_press.K_x ,self.last_press.K_x,key=keybinding['attack'])
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_x = self.now_press.K_x

                elif event.key == keybinding['jump']:
                    self.now_press.K_c = pygame.time.get_ticks()
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_c = self.now_press.K_c
                elif event.key == keybinding['pickOn']:
                    self.now_press.K_z = pygame.time.get_ticks()
                    self.keys = pygame.key.get_pressed()
                    self.last_press.K_z = self.now_press.K_z
                elif event.key == keybinding['sub_addNpc']:
                    if tools.DEBUG:
                        if  self.level != None:
                            self.level.sub_addNpc(self)
                            print('size of npc objects  '+str(sys.getsizeof(self.npcs)))
                            print('size of game world   ' + str(sys.getsizeof(self)))
                            self.tracker.create_snapshot("world memory usage")
                            self.tracker.stats.print_summary()


                elif event.key == keybinding['sub_bag']:
                    self.system.bag.isOpen = not self.system.bag.isOpen
                elif event.key == keybinding['sub_debug']:
                    tools.DEBUG = not tools.DEBUG
                elif event.key == keybinding['sub_npcAttack']:
                    for npc in self.npcs:
                        npc.dummy = not npc.dummy
                        print("npc开启攻击:{}".format(npc.dummy))
                elif event.key == pygame.K_r:
                    self.toReset= True
                if tools.DEBUG:
                    if event.key == K_END:
                        self.point1 = None
                    if event.key == K_DELETE:
                        self.point1 = None
                        self.deleteBorder()


        elif event.type == KEYUP:
            self.keys = pygame.key.get_pressed()



        elif event.type == MOUSEBUTTONDOWN:
            
            mouse = self.mouseIcon.sprites()[0]
            if tools.DEBUG:
                pass
                #print('当前坐标：{}'.format(mouse.xy))
            mouse.image = mouse.up_img
            self.draw_border()

        elif event.type == MOUSEBUTTONUP:
            mouse = self.mouseIcon.sprites()[0]
            mouse.image = mouse.up_img

    def input_judge(self,now_press,last_press,key=None):
        """连击按键判断"""
        if key == None:
            t1,t2 = .05 * 1000 ,.3 * 1000
        
            if last_press != 0 and now_press - last_press >= t1 and now_press - last_press <= t2:
                self.player.doublePress = True
                print('连按间隔：{}ms'.format(now_press - last_press))
        elif key == keybinding['attack']:
            
            t1,t2 = .05 * 1000 ,.7 * 1000
            if last_press != 0 and now_press - last_press >= t1 and now_press - last_press <= t2:
                self.player.doubleAttack = True
                print('连按x间隔：{}ms'.format(now_press - last_press))
            else:
                print('连续攻击结束')

    def printInfo(self):
        #print("mouse location(world):",self.mouseIcon.sprites()[0].pos)
        print('camera location(world):',self.camera.xy)
        print('player location(world):',self.player.xy)
        print('player location(local):',self.player.pos)
        #print(self.bgGroup.sprites())
        pass

    def camera_follow(self):
        """移动镜头坐标跟随角色"""

        def isInside(pos, rect):
            """
            参数类型 pos[x,y], rect[x, y, width, height]
            返回值类型 tuple(int x,int y)
            判断角色是否在给摄像机跟随矩形内部，如果在则无需跟随,返回 x = y = 0
            ，如果不在则：
                如果在矩形左侧： x = -1
                如果在矩形右侧： x = 1
                如果在矩形上侧： y = 1
                如果在矩形下侧： y = -1
            """
            if pos[0] < rect[0]:
                x = -1
            elif pos[0] > rect[0] + rect[2]:
                x = 1
            else:
                x = 0
            if pos[1] < rect[1]:
                y = 1
            elif pos[1] > rect[1] + rect[3]:
                y = -1
            else:
                y = 0
            return x,y


        player = self.player
        vel_x = player.x_vel
        vel_y = player.y_vel

        """自适应分辨率比例"""
        tL = 0.1
        tR = 0.1
        tT = 1 - 0.05
        tB = 1 - 0.55

        """角色精灵Image位置偏移"""
        w = 80 
        h = 20
        dx = 100
        dy = 270        
        """镜头跟的随矩形，可定义函数来生成"""
        rect = [300, 400, 300, 200]
        if tools.DEBUG:
            pygame.draw.rect(self.camera.screen,(0,255,0),rect,3)

        """计算出角色脚下坐标的位置"""
        pRect = (self.player.rect[0] + dx, self.player.rect[1] + dy + self.player.z, w, h)
        pos = [int(pRect[0]+w/2),int(pRect[1]+h/2)]

        """"判断是否越界"""
        inside = isInside(pos, rect)

        """根据返回值移动镜头"""
        if inside[0] == 1:
            if player.x_vel > 0:
                self.camera.scroll(inside[0]*vel_x*self.dt, 0)
        elif inside[0] == -1:
            if player.x_vel < 0:
                self.camera.scroll( -1 * inside[0]*vel_x*self.dt, 0)

        if inside[1] == 1:
            if player.y_vel > 0:
                self.camera.scroll(0, -1 * inside[1]*vel_y*self.dt)
        elif inside[1] == -1:
            if player.y_vel < 0:
                self.camera.scroll(0, inside[1]*vel_y*self.dt)




    def remove_offset(self):
        #碰撞坐标偏差
        w = 80 
        h = 20
        dx = 100
        dy = 270
        rect = (self.player.rect[0] + dx, self.player.rect[1] + dy + self.player.z, w, h)
        self.player.pos = [int(rect[0]+w/2),int(rect[1]+h/2)]

    def sprite_move(self,sprite, dt):
        sprite.xy[0] += sprite.x_vel * dt
        sprite.xy[1] -= sprite.y_vel * dt
        sprite.z += 0.5 * sprite.gAccel * dt * dt



    def setup(self,level,player,camera,system):
        """初始化"""
        self.level = level
        self.camera = camera
        self.player = player 
        self.npcGroup = pygame.sprite.Group()
        self.lines = self.level.load_border()
        self.system = system
        self.system.setup(self)

        #self.camera.screen.blit(self.level.background.image,(0,0))

        self.bgGroup.add(self.level.background)
        self.playerGroup.add(self.player)

        #创建体积碰撞组
        self.c_group = pygame.sprite.Group()
        self.c_group.add(self.player.volumeBox)


        x = self.player.xy[0]
        y = self.player.xy[1]

        self.camera.xy = [x,y]


        for sprite in self.bgGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)
        for sprite in self.playerGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)
        for sprite in self.npcGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)






        self.load_text()
        pygame.display.flip()


    def load_text(self):
        self.textbox = Textbox()
        
        f = open("data/instructions.txt",'r')             
        lines = f.readlines()             # 调用文件的 readline()方法  
        self.textbox.dialogue = []

        for line in lines:
            if line != '':
                self.textbox.dialogue.append(line)
        self.textbox.textIndex = 0
    def update(self,dt):
        if self.counts%60 == 0:
            pass
            #self.printInfo()
        self.dt = dt
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            else:
                self.keySub(event)
                pass

        

        """运动处理"""

        #参数更新
        self.system.update()

        #更新所有sprites
        self.bgGroup.update()
        self.playerGroup.update(dt)
        self.npcGroup.update(dt)
        self.mouseIcon.update()
        player = self.player
        self.npcs = self.npcGroup
        sprites = [player]


        #体积碰撞检测
        self.decectCollision()
        for npc in self.npcs:
            self.decectCollisionMonster(npc)

        #角色运动
        self.sprite_move(player, dt)
        #摄像机镜头跟随角色
        self.camera_follow()
        #self.camera.update()

        
        for npc in self.npcs:
            npc.move_to_target(player)
            self.sprite_move(npc, dt)
            sprites.append(npc)


        #获取所有sprite的摄像机局部坐标
        for sprite in self.bgGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)
        for sprite in self.playerGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)
        for sprite in self.npcGroup.sprites():
            sprite.pos = self.__getPos(sprite)
            #print(sprite)

        self.mouseIcon.sprites()[0].pos = pygame.mouse.get_pos()


        



        player.doublePress = False
        player.doubleAttack = False
        



        #攻击判定，先角色后怪物
        player.collider(self.npcGroup)
        
        for npc in self.npcs:
            npc.doublePush = False
            npc.doubleAttack = False
            npc.collider(self.playerGroup)

        #self.camera.focus(self.spritesGroup.get_sprites_from_layer(0)[0])



        #sprites = sorted(sprites,keys=sprites.xy[1])
        sprites.sort(key=lambda obj:obj.xy[1], reverse=False)



        #渲染图像到屏幕
        if tools.DEBUG:
            self.render = pygame.sprite.LayeredUpdates(self.bgGroup,self.c_group,sprites)
            self.draw_rect(self.playerGroup.sprites())
            pygame.draw.circle(self.camera.screen,(255,0,0),self.__getPos(self.player),3)
            pygame.draw.circle(self.camera.screen,(255,0,0),pygame.mouse.get_pos(),3)
            if len(self.lines) > 0:
                for line in self.lines:
                    pygame.draw.line(self.camera.screen,(255,0,0),self.__getPosfromXy(line[0]),self.__getPosfromXy(line[1]),2)
        else:
            self.render = pygame.sprite.LayeredUpdates(self.bgGroup,sprites)
        if self.editBorder:
            text = 'Editing Map Border'
        else:
            text = 'pygame test'
        self.camera.putText(text,None) 
        if tools.DEBUG:
            self.camera.putText("DEBUG",(0,0)) 
        self.draw_health()
        self.draw_energy()
        for npc in self.npcs:
            self.draw_monster_health(npc)


        #UI渲染
        """
        TODO
        伤害数字显示
        """
        #self.showDamage()


        """系统文本显示"""
        if self.textbox != None:
            self.textbox.render(self.camera.screen)
        """UI显示"""
        self.system.ui.render(self.camera.screen)

        """鼠标指针渲染"""
        self.mouseIcon.draw(self.camera.screen)
        pygame.display.flip()
        self.counts += 1
        pass

    def showDamage(self):
        """用于显示玩家造成的伤害数字
        施工中暂不可用
        
        """
        if len(self.npcs)>0:
            for npc in self.npcs:
                
                """demage[target, int damageVar]
                """
                dx = 0
                dy = 0
                if len(npc.damageList)>0:
                    d = [npc,npc.damageList[0]]
                    npc.damageList.pop(0)
                    self.damageList.append(d)




                for d in dlist:
                    self.camera.putText(str(d[2]),(d[1],d[2])) 
                    d[1] += 10
            

        pass


    def decectCollision(self):
        #碰撞坐标偏差
        w = 80 
        h = 20
        dx = 100
        dy = 270
        rect = (self.player.rect[0] + dx, self.player.rect[1] + dy + self.player.z, w, h)
        pos = [int(rect[0]+w/2),int(rect[1]+h/2)]
        if tools.DEBUG:
            pygame.draw.circle(self.camera.screen,(255,0,0),pos,10)
            pygame.draw.rect(self.camera.screen,(255,0,0),rect,1)

        xy = self.__getXyfromPos(pos)
        
        if len(self.lines) > 0:
            for line in self.lines:
                normal_vector = self.detect_toch_line(line[0],line[1],xy)

                if normal_vector:
                    n = 11
                    print("法向量：{}".format(normal_vector))
                    if normal_vector[0] != 0:
                        self.player.vel_x = 0
                        self.player.xy[0] += n * normal_vector[0]
                    #self.camera.scroll(n * normal_vector[0],0)
                    if normal_vector[1] != 0:
                        self.player.vel_y = 0
                    self.player.xy[1] += n * normal_vector[1]
                    #self.camera.scroll(0, n * normal_vector[1])
                    return True

    def decectCollisionMonster(self,monster):
        #碰撞坐标偏差
        w = 80 
        h = 20
        dx = 100
        dy = 270
        rect = (monster.rect[0] + dx, monster.rect[1] + dy + monster.z, w, h)
        pos = [int(rect[0]+w/2),int(rect[1]+h/2)]
        if tools.DEBUG:
            pygame.draw.circle(self.camera.screen,(255,0,0),pos,10)
            pygame.draw.rect(self.camera.screen,(255,0,0),rect,1)

        xy = self.__getXyfromPos(pos)
        
        if len(self.lines) > 0:
            for line in self.lines:
                normal_vector = self.detect_toch_line(line[0],line[1],xy)

                if normal_vector:
                    n = 10
                    #print(normal_vector)
                    monster.xy[0] += n * normal_vector[0]
                    monster.xy[1] += n * normal_vector[1]
    def restart(self):
        """重载关卡
        """
        restart(self)

        pass
    def __loadLevel(self):
        """载入关卡
        """
        pass

    def __unLoadLevel(self):
        """卸载关卡
        """
        del self.camera
        del self.player
        del self.level
        del self.playerGroup
        del self.npcGroup
        del self.render
        pass

    def __function(self):
        pass

    def __getPos(self,sprite):
        """根据世界坐标返回屏幕坐标从而显示到屏幕
            param1:sprite
            return xc,yc
            y'=-(y-y0)  x' = x-x0
            y =-(y'-y0) x  = x'+x0
            摄像机坐标原点的世界坐标 (x0,y0) Cxy
            摄像机下的局部坐标 (x',y') pos
        """
        xw = sprite.xy[0]
        yw = sprite.xy[1]
        Cxy = self.camera.xy

        xc = int(xw - Cxy[0] + sprite.width/2)
        yc = int(yw - Cxy[1] + sprite.height/2 - sprite.z)
        return [xc,yc]
        pass
    def __getPosfromXy(self,pos):
        """根据世界坐标返回屏幕坐标从而显示到屏幕
            param1:pos
            return xc,yc
            y'=-(y-y0)  x' = x-x0
            y =-(y'-y0) x  = x'+x0
            摄像机坐标原点的世界坐标 (x0,y0) Cxy
            摄像机下的局部坐标 (x',y') pos
        """
        xw = pos[0]
        yw = pos[1]
        Cxy = self.camera.xy

        xc = int(xw - Cxy[0])
        yc = int(yw - Cxy[1])
        return [xc,yc]
        pass

    def __getXy(self,sprite):
        """根据屏幕坐标返回世界坐标"""
        xc = sprite.pos[0] - sprite.width/2
        yc = sprite.pos[1] - sprite.height/2
        Cxy = self.camera.Cxy

        xw = int(xc + Cxy[0])
        yw = int(yc + Cxy[1])
        return[xw,yw]

    def __getXyfromPos(self,pos):
        """根据屏幕坐标返回世界坐标"""
        xc = pos[0]
        yc = pos[1]
        Cxy = self.camera.xy

        xw = xc + Cxy[0]
        yw = yc + Cxy[1]
        return[xw,yw]

    def __getLine(self, pos1, pos2):
        dx = pos2[0] - pos1[0] 
        dy = pos2[1] - pos1[1] 
        if dx != 0:
            w = dy / dx
            b = pos1[1] - w * pos1[0]
            self.Wb.append((w,b))
        else:
            self.Wb.append(pos2[0])

        

    def detect_toch_line(self, xy1, xy2, xy, threshold=20):
        """
        检测点与直线的距离，判断是否有越界，若有返回单位法向量，无返回空
        param1: 线段端点1坐标 (x1,y1)
        param2: 线段端点2坐标 (x2,y2)
        param3: 需要判断的点坐标 (x,y)
        """
        def min(a, b):
            return a if a<b else b

        dx = xy2[0] - xy1[0] 
        dy = xy2[1] - xy1[1] 
        if dx != 0:
            #斜率存在
            w = dy / dx
            b = xy1[1] - w * xy1[0]
            d = abs(w * xy[0] - xy[1] + b) / math.sqrt(w * w + 1)

            if dy != 0:
                #垂线斜率存在

                #解方程 xy[1]=(-1/w)*xy[0]+b_
                b_ = xy[1] + (1/w) * xy[0]
                #解方程 y=w*x+b   y=(-1/w)*x +b_
                x_ = (b_ - b)/(w + 1/w)
                y_ = w * x_ + b

                if y_ > xy1[1] and y_ > xy2[1]:
                    return
                elif y_ < xy1[1] and y_ < xy2[1]:
                    return
                if d <= threshold:
                    print("垂线斜率存在")
                    normal_vector = (abs(xy[0]-x_)/(xy[0]-x_), abs(xy[1]-y_)/(xy[1]-y_))
                    return normal_vector
                else:
                    return


            else:
                #垂线斜率不存在
                if xy[0] > xy1[0] and xy[0] > xy2[0]:
                    return
                elif xy[0] < xy1[0] and xy[0] < xy2[0]:
                    return
                if d <= threshold:
                    print("垂线斜率不存在")
                    normal_vector = (0, abs(xy[1]-xy1[1])/(xy[1]-xy1[1]))
                    return normal_vector
                else:
                    return

        else:
            #斜率不存在
            if xy[1] > xy1[1] and xy[1] > xy2[1]:
                return
            elif xy[1] < xy1[1] and xy[1] < xy2[1]:
                return
            d = abs(xy1[0] - xy[0])
            normal_vector = (abs(xy[0]-xy1[0])/xy[0]-xy1[0], 0)
        

            if d <= threshold:
                print("斜率不存在")
                return normal_vector
            else:
                return




    def __del__(self):
        print("回收对象{}".format("world"))