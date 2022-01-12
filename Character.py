# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from Src_loader import *
from GameObject import *
import time
from tools import *
import tools as t
import math
position = {'left':0,'right':1}


class Character(GameObject):
    """
    玩家角色
    """
    __slots__ = ['name','image','mask',
                'rect','width','height','frame','ticks',
                'pos','xy','z','actionSpace','state','lastState',
                'actComplete','allowControl','allowJump','doublePress','doubleAttack','hurtToFall','position','stickPosition',
                'next_state','speed','walkSpeed','runSpeed','dizzy','move_direction','atkSpeed','jumpSpeed','jumpHeight',
                'jumpHigher','floated','gAccel','z_vel','playRate','src_path','printState','isCout','repeat','maxHp','hp','lastHp',
                'maxEnergy','energy','lastEnergy','isDead','lossingHp','lossingEnergy','phyAttack','damaged','damageList','interactiveEnable']
    def __init__(self):
        GameObject.__init__(self) #call Sprite intializer

        self.name = 'player0'
        self.image = pygame.image.load('src/saber1/stand.png')
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect = pygame.Rect(600,600,self.image.get_rect()[2],self.image.get_rect()[3])
        self.width = self.rect.width
        self.height = self.rect.height
        self.frame = 0
        self.ticks = 0
        self.pos = []
        self.xy = [200 + self.width/2, 650 + self.height/2]
        self.z = 0

        self.actionSpace = {'stand':0,'walk':1,'run':2,'jump':3,'attack':4,'stick':5,'jumpCut':6,'pickOn':7,'hurt':8, 'attackRig':9,'fall':10,'dead':11,'combo':12,'con_combo':13,'swordSkill':14}
        self.state = self.actionSpace['stand']
        self.lastState = self.state
        self.actComplete = True
        self.allowControl = True
        self.allowJump = True
        self.doublePress = False
        self.doubleAttack = False
        self.hurtToFall = False
        self.position = position['right']
        self.stickPosition = self.position
        self.next_state = self.state
        self.speed = 0
        self.dt = 0

        self.walkSpeed = 200
        self.runSpeed = self.walkSpeed * 2
        self.dizzy = 0
        self.move_direction = 0
        self.atkSpeed = 8
        self.jumpSpeed = 1
        self.jumpHeight = 100
        self.jumpHigher = False
        self.floated = False
        self.onGround = True

        self.gAccel = -980
        self.z_vel = 0
        self.playRate = 7 #  7 正常速度
        self.src_path = 'src/saber1/'
        self.load_imgs()
        self.printState = False
        self.isCout = True
        self.repeat = False
        
        self.maxHp = 500
        self.hp = 500
        self.lastHp = self.hp
        self.maxEnergy = 200
        self.energy = 200
        self.lastEnergy = self.energy
        self.damageList = []

        self.isDead = False
        self.lossingHp = False
        self.lossingEnergy = False

        self.phyAttack = 100

        self.damaged = []

        self.range_config()
        self.collid_config()



    def range_config(self):
        self.attackRange = 80 #pixs
        self.stickRange = 60 #pixs
        self.jumpCutRange = 70
    def collid_config(self):
        #体积碰撞盒
        self.volumeBox = pygame.sprite.Sprite()
        self.volumeBox.rect = self.rect
        self.volumeBox.image = self.location_mask
        self.volumeBox.mask = pygame.mask.from_surface(self.location_mask)
        #攻击判定碰撞盒
        self.attackBox = pygame.sprite.Sprite()
        p = self.position
        self.collidAnchor = []
        for i in range(len(self.mask_keys)):
            key = self.mask_keys[i]
            mask = pygame.sprite.Sprite()
            mask.imgs = [cutImgL(self.frames_num[key],self.img_mask_loader[self.mask_dic[key]][0]),cutImgR(self.frames_num[key],self.img_mask_loader[self.mask_dic[key]][1])]
            mask.image = mask.imgs[p][self.frame]
            mask.rect = mask.image.get_rect()
            mask.mask = pygame.mask.from_surface(mask.image)
            self.collidAnchor.append(mask)

    def finish(self):
        self.lastState = self.state
        self.actComplete = True
        self.allowControl = True
        #print(self.allowControl)
        pass
    def load_imgs(self):
        self.right_frames = []
        self.left_frames = []
        self.frames_num = {'stand':6,'walk':8,'run':8,'attack':10,'jump':8,'stick':10,'jumpCut':6,'pickOn':9,'hurt':6,'attackRig':4,'fall':8,'dead':4,'combo':10,'con_combo':9}


        #{'stand':0,'walk':1,'run':2,'jump':3,'attack':4,'stick':5,'jumpCut':6,'pickOn':7,'hurt':8, 'attackRig':9,'fall':10,'dead':11}
        self.state = self.actionSpace['stand']
        self.img_stand = [load_img(self.src_path + 'stand0.png'),load_img(self.src_path + 'stand1.png')]
        self.img_walk = [load_img(self.src_path + 'walk0.png'),load_img(self.src_path + 'walk1.png')]
        self.img_run = [load_img(self.src_path + 'run0.png'),load_img(self.src_path + 'run1.png')]
        self.img_jump = [load_img(self.src_path + 'jump0.png'),load_img(self.src_path + 'jump1.png')]
        self.img_attack = [load_img(self.src_path + 'attack0.png'),load_img(self.src_path + 'attack1.png')]
        self.img_stick = [load_img(self.src_path + 'stick0.png'),load_img(self.src_path + 'stick1.png')]
        self.img_jumpCut = [load_img(self.src_path + 'jumpCut0.png'),load_img(self.src_path + 'jumpCut1.png')]
        self.img_pickOn = [load_img(self.src_path + 'pickOn0.png'),load_img(self.src_path + 'pickOn1.png')]
        self.img_hurt = [load_img(self.src_path + 'hurt0.png'),load_img(self.src_path + 'hurt1.png')]
        self.img_attackRig = [load_img(self.src_path + 'attackRig0.png'),load_img(self.src_path + 'attackRig1.png')]
        self.img_fall = [load_img(self.src_path + 'fall0.png'),load_img(self.src_path + 'fall1.png')]
        self.img_dead = [load_img(self.src_path + 'dead0.png'),load_img(self.src_path + 'dead1.png')]
        self.img_combo = [load_img(self.src_path + 'combo0.png'),load_img(self.src_path + 'combo1.png')]
        self.img_con_combo = [load_img(self.src_path + 'con_combo0.png'),load_img(self.src_path + 'con_combo1.png')]

        self.img_skill = {}

        #体积碰撞mask
        self.location_mask = load_img(self.src_path + 'location_mask.png')
        #攻击判定mask
        self.img_mask_loader = []
        self.mask_dic = {'attack':0, 'stick':1, 'jumpCut':2, 'pickOn':3,'combo':4, 'con_combo':5}
        self.mask_keys = ['attack', 'stick', 'jumpCut', 'pickOn', 'combo', 'con_combo']
        for i in range(len(self.mask_keys)):
            key = self.mask_keys[i]
            self.img_mask_loader.append([load_img(self.src_path + key + '0_mask.png'),load_img(self.src_path + key + '1_mask.png')])



        #self.img_attack_mask = [load_img(self.src_path + 'attack0_mask.png'),load_img(self.src_path + 'attack1_mask.png')]
        #self.img_stick_mask = [load_img(self.src_path + 'stick0_mask.png'),load_img(self.src_path + 'stick1_mask.png')]
        #self.img_jumpCut_mask = [load_img(self.src_path + 'jumpCut0_mask.png'),load_img(self.src_path + 'jumpCut1_mask.png')]
        #self.img_pickOn_mask = [load_img(self.src_path + 'pickOn0_mask.png'),load_img(self.src_path + 'pickOn1_mask.png')]

        self.left_frames.append(cutImgL(self.frames_num['stand'],self.img_stand[0]))
        self.left_frames.append(cutImgL(self.frames_num['walk'],self.img_walk[0]))
        self.left_frames.append(cutImgL(self.frames_num['run'],self.img_run[0]))
        self.left_frames.append(cutImgL(self.frames_num['jump'],self.img_jump[0]))
        self.left_frames.append(cutImgL(self.frames_num['attack'],self.img_attack[0]))
        self.left_frames.append(cutImgL(self.frames_num['stick'],self.img_stick[0]))
        self.left_frames.append(cutImgL(self.frames_num['jumpCut'],self.img_jumpCut[0]))
        self.left_frames.append(cutImgL(self.frames_num['pickOn'],self.img_pickOn[0]))
        self.left_frames.append(cutImgL(self.frames_num['hurt'],self.img_hurt[0]))
        self.left_frames.append(cutImgL(self.frames_num['attackRig'],self.img_attackRig[0]))
        self.left_frames.append(cutImgL(self.frames_num['fall'],self.img_fall[0]))
        self.left_frames.append(cutImgL(self.frames_num['dead'],self.img_dead[0]))
        self.left_frames.append(cutImgL(self.frames_num['combo'],self.img_combo[0]))
        self.left_frames.append(cutImgL(self.frames_num['con_combo'],self.img_con_combo[0]))


        self.right_frames.append(cutImgR(self.frames_num['stand'],self.img_stand[1]))
        self.right_frames.append(cutImgR(self.frames_num['walk'],self.img_walk[1]))
        self.right_frames.append(cutImgR(self.frames_num['run'],self.img_run[1]))
        self.right_frames.append(cutImgR(self.frames_num['jump'],self.img_jump[1]))
        self.right_frames.append(cutImgR(self.frames_num['attack'],self.img_attack[1]))
        self.right_frames.append(cutImgR(self.frames_num['stick'],self.img_stick[1]))
        self.right_frames.append(cutImgR(self.frames_num['jumpCut'],self.img_jumpCut[1]))
        self.right_frames.append(cutImgR(self.frames_num['pickOn'],self.img_pickOn[1]))
        self.right_frames.append(cutImgR(self.frames_num['hurt'],self.img_hurt[1]))
        self.right_frames.append(cutImgR(self.frames_num['attackRig'],self.img_attackRig[1]))
        self.right_frames.append(cutImgR(self.frames_num['fall'],self.img_fall[1]))
        self.right_frames.append(cutImgR(self.frames_num['dead'],self.img_dead[1]))
        self.right_frames.append(cutImgR(self.frames_num['combo'],self.img_combo[1]))
        self.right_frames.append(cutImgR(self.frames_num['con_combo'],self.img_con_combo[1]))

    def handle_state(self, keys):

        s = self.state
        a = self.actionSpace
        if self.state == a['stand']: 
            self.stand(keys)
                
        elif self.state == a['walk']: 
            self.walk(keys)

        elif self.state == a['run']: 
            self.run(keys)

        elif self.state == a['jump']:
            self.jump(keys)

        elif self.state == a['attack']: 
            self.attack(keys)

        elif self.state == a['stick']: 
            self.stick(keys)

        elif self.state == a['jumpCut']: 
            self.jumpCut(keys)
        elif self.state == a['pickOn']: 
            self.pickOn(keys)
        elif self.state == a['hurt']:
            self.hurt(keys)
        elif self.state == a['attackRig']:
            self.attackRig(keys)
        elif self.state == a['fall']:
            self.fall(keys)
        elif self.state == a['dead']:
            self.dead(keys)
        elif self.state == a['combo']:
            self.combo(keys)
        elif self.state == a['con_combo']:
            self.con_combo(keys)

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
        keys = pygame.key.get_pressed()
        self.handle_state(keys)
        self.updateHeight(self.z_vel,self.z, self.gAccel, self.dt)
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]
        self.actComplete = False
        

        self.update_mask()
        self.animation()
        self.ticks += 1
        if int(self.ticks % self.playRate) == 0:

            self.frame += 1
            

    def updateHeight(self, v0, z0, g, dt):
            z_vel = v0 + g * dt
            z = z0 + z_vel * dt
            if self.onGround:
                self.z = 0
                self.z_vel = 0
            else:
                self.z_vel = z_vel
                self.z  = z
                



    def check_to_allow_jump(self):
        """检查是否可以跳跃
            条件是 处于站立、行走或奔跑状态
        """
        s = self.state
        a = self.actionSpace
        if s == a["stand"] or s == a["walk"] or s == a["run"]:
            self.allowJump = True
        elif s == a["jump"] and self.z_vel == 0:
            self.allowJump = True
        else:
            self.allowJump = False


    def check_on_the_ground(self):
        if self.z > 0 :
            self.onGround = False
        else:
            self.onGround = True

    def check_is_dead(self):
        if self.hp <= 0:
            self.hp = 0
            self.state = self.actionSpace['dead']
    def check_is_floated(self):
        if self.z > 0:
            self.floated = True

    def attack_collider(self, targetGroup):
        return pygame.sprite.spritecollide(self.attackBox,targetGroup,False,pygame.sprite.collide_mask)

    def collider(self, targetGroup):
        if self.state == self.actionSpace['attack']:
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.attackRange:
                        if target not in self.damaged:
                            print('普通攻击打到了{}'.format(target.name))
                            target.get_damage(self.phyAttack)
                            self.damaged.append(target)


        elif self.state == self.actionSpace['stick']:
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.stickRange:
                        if target not in self.damaged:
                            print('突刺攻击打到了{}'.format(target.name))
                            target.get_damage(int(self.phyAttack * 1.5))
                            self.damaged.append(target)

        elif self.state == self.actionSpace['jumpCut']: 
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.jumpCutRange:
                        if target not in self.damaged:
                            print('跃斩攻击打到了{}'.format(target.name))
                            target.get_damage(int(self.phyAttack * 1.3))
                            self.damaged.append(target)
        elif self.state == self.actionSpace['pickOn']: 
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.stickRange:
                        if target not in self.damaged:
                            print('上挑攻击打到了{}'.format(target.name))
                            target.get_damage(int(self.phyAttack * 0.5))
                            if not self.state == self.actionSpace['fall']:
                                target.z_vel += 10
                                target.z += 20
                                self.floated = True
                            self.damaged.append(target)

        elif self.state == self.actionSpace['combo']: 
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.stickRange:
                        if target not in self.damaged:
                            print('连续1攻击打到了{}'.format(target.name))
                            target.get_damage(int(self.phyAttack * 1.2))
                            self.damaged.append(target)

        elif self.state == self.actionSpace['con_combo']: 
            c = self.attack_collider(targetGroup)
            if c != []:
                for target in c:
                    if abs(target.xy[1] - self.xy[1]) <= self.stickRange:
                        if target not in self.damaged:
                            print('连续2攻击打到了{}'.format(target.name))
                            target.get_damage(int(self.phyAttack * 1.4))
                            if not self.state == self.actionSpace['fall']:
                                target.z_vel += 10
                                target.z += 20
                                self.floated = True

                            self.damaged.append(target)

    def get_damage(self,damage):
        if not self.isDead:
            preHp = self.hp
            if not self.lossingHp:
                self.lastHp = self.hp
                self.lossingHp = True
            self.hp -= damage
            self.damageList.append(damage)
            self.check_is_dead()
            print('{}受到了{}点伤害,当前血量{}'.format(self.name,damage,self.hp))
            for i in range(5):
                if i != 0:
                    threhold = self.maxHp * (3 * i) / 5
                    if preHp >= threhold and self.hp <= threhold:
                        
                        self.hurtToFall = True
            if self.hurtToFall:
                self.state = self.actionSpace['fall']
            else:
                self.state = self.actionSpace['hurt']
            self.frame = 0
            if self.hp <= 0:
                print('{}被杀死了'.format(self.name))
                self.isDead = True
                self.state = self.actionSpace['dead']
        else:
            print('{}已经死亡'.format(self.name))

        self.check_is_dead()
    def get_heal(self, heal):
        if not self.isDead:
            preHp = self.hp
            if self.hp+heal <= self.maxHp:
                self.hp += heal
                print('{}受到了{}点治疗'.format(self.name,heal))
            else:
                self.hp = self.maxHp
                print('{}受到了{}点治疗'.format(self.name,self.maxHp-self.hp))

    def stand(self,keys):
        a = self.actionSpace
        self.x_vel = 0
        self.y_vel = 0
        if self.frame >= self.frames_num['stand']:
            self.frame = 0
        if self.doublePress:
            self.speed = self.runSpeed
            self.state = a['run']
            #print('walk->run')
        else:
            self.speed = self.walkSpeed
            self.state = a['walk']


        if keys[t.keybinding['left']]:
            self.position = position['left']
            self.x_vel = -self.speed
        elif keys[t.keybinding['right']]:
            self.position = position['right']
            self.x_vel = self.speed
        if keys[t.keybinding['up']]:
            self.y_vel = self.speed
        elif keys[t.keybinding['down']]:
            self.y_vel = -self.speed

        if not(keys[t.keybinding['up']] or keys[t.keybinding['down']] or keys[t.keybinding['left']] or keys[t.keybinding['right']]):
            #self.frame = 0
            self.state = a['stand']

        if keys[t.keybinding['attack']]:
            self.frame = 0
            self.state = a['attack']

        elif keys[t.keybinding['jump']]:
            self.frame = 0
            self.state = a['jump']
            print('jump')

        elif keys[t.keybinding['pickOn']]:
            self.frame = 0
            self.state = a['pickOn']
            print('pick on')

        self.actComplete = True

    def walk(self,keys):
        s = self.state
        a = self.actionSpace
        #print(self.frame)
        if self.frame >= self.frames_num['walk']:
            self.frame = 0

        if self.doublePress:
            self.speed = self.runSpeed
            self.state = a['run']
            #print('walk->run')
        else:
            self.speed = self.walkSpeed
            self.state = a['walk']
        if keys[t.keybinding['left']]:
            self.position = position['left']
            self.x_vel = -self.speed
        elif keys[t.keybinding['right']]:
            self.position = position['right']
            self.x_vel = self.speed
        else:
            self.x_vel = 0

        if keys[t.keybinding['up']]:
            self.y_vel = self.speed
        elif keys[t.keybinding['down']]:
            self.y_vel = -self.speed
        else:
            self.y_vel = 0

        if not(keys[t.keybinding['up']] or keys[t.keybinding['down']] or keys[t.keybinding['left']] or keys[t.keybinding['right']]):
            self.frame = 0
            print('stop walking')
            self.state = a['stand']

        if keys[t.keybinding['attack']]:
            self.x_vel = 0
            self.y_vel = 0
            self.frame = 0
            self.state = a['attack']

        elif keys[t.keybinding['jump']]:
            self.frame = 0
            self.state = a['jump']   
        elif keys[t.keybinding['pickOn']]:
            self.frame = 0
            self.state = a['pickOn']
            print('pick on')

    def run(self,keys):
        s = self.state
        a = self.actionSpace
        if self.frame >= self.frames_num['run']:
            self.frame = 0

        if keys[t.keybinding['left']]:
            self.position = position['left']
            self.state = a['run']
            self.x_vel = -self.runSpeed
        elif keys[t.keybinding['right']]:
            self.position = position['right']
            self.state = a['run']
            self.x_vel = self.runSpeed
        else:
            self.x_vel = 0

        if keys[t.keybinding['up']]:
            self.state = a['run']
            self.y_vel = self.runSpeed
        elif keys[t.keybinding['down']]:
            self.state = a['run']
            self.y_vel = -self.runSpeed
        else:
            self.y_vel = 0

        if not(keys[t.keybinding['up']] or keys[t.keybinding['down']] or keys[t.keybinding['left']] or keys[t.keybinding['right']]):
            self.frame = 0
            print('stop running')
            self.state = a['stand']

        if keys[t.keybinding['attack']]:
            self.frame = 0
            self.state = a['stick']
            print('stick')
        elif keys[t.keybinding['jump']]:
            self.frame = 0
            self.state = a['jump']   
    def attack(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        self.playRate = self.atkSpeed
        
        if self.frame == 0:
            self.damaged = []

        if keys[t.keybinding['attack']]:
            if self.doubleAttack:
                if self.frame >= self.frames_num['attack'] - 2:
                    self.state = self.actionSpace['combo']
                    self.damaged = []
                    self.playRate = 7
                    self.frame = 0
                    print('combo')

        if self.frame >= self.frames_num['attack']:
            #print('normal attack')
            #self.state = self.actionSpace['attackRig']
            self.state = self.actionSpace['stand']
            self.damaged = []
            self.playRate = 7
            self.frame = 0
    def attackRig(self,keys):
        self.x_vel = 0
        self.y_vel = 0

        if self.frame == 0:
            self.repeat = True

        if self.frame >= self.frames_num['attackRig']:
            
            if self.repeat:
                self.frame = 1
                self.state = self.actionSpace['attackRig']
                self.repeat = False
            else:
                self.frame = 0
                self.state = self.actionSpace['stand']

    def jump(self,keys):
        """
        进行跳跃动作
        执行的逻辑：
            1.如果是第一帧：通过跳跃高度计算初始速度，并将滞空状态floated置为True,将
          将是否允许跳跃 allowJump值置为 False，将是否在地面 onGround 置为False 
          然后执行2；否则：直接执行2
            2.根据加速度公式 v = v0 + g*dt 更新变化后的z轴速度
            3.根据跳跃的三个阶段来更新当前需要的帧值


            关于跳跃的三个阶段：
                跳跃分为：起跳、上升、下降 三个阶段 分别对应 0-7帧
                当 z < 2/height 且 z_vel>0时，播放第 0-2 帧
                当 z > 2/height 时，播放第 3-5 帧
                当 z < 2/height z_vel<0时，播放第 5-7 帧
            
        """

        def cal_vel(height, accel):
            """跳跃高度,加速度"""
            vel = math.sqrt(math.fabs(2 * height * accel))
            return vel

  

        def adjust(frame,start,end):
            if frame > end:
                return end
            elif frame < start:
                return start
            else:
                return frame


        def updateFrame(z, Hmax, z_vel, frame):
            """根据速度和高度选取所需的帧"""
            if z < Hmax/2:
                if z_vel >= 0:
                    frame = adjust(frame,0,0)
                else:
                    frame = adjust(frame,5,7)
            else:
                frame = adjust(frame,1,5)
            return frame

        if self.frame == 0:
            #print("allowJump={}".format(self.allowJump))

            if self.allowJump:
                vel = cal_vel(self.jumpHeight, self.gAccel) 
                self.z_vel = vel
                self.allowJump = False
                self.z += 40
                self.frame += 1
        self.onGround =False
        self.frame = updateFrame(self.z, self.jumpHeight, self.z_vel, self.frame)
        if self.z < 0 :
            self.z = 0
            self.z_vel = 0
            self.state = self.actionSpace['stand']
            self.allowJump = True
            self.onGroud = True

        if keys[t.keybinding['left']]:
            if not abs(self.x_vel) > 0:
                self.x_vel = -self.walkSpeed
            elif self.position == position['right']:
                self.x_vel = -self.x_vel
            self.position = position['left']

        elif keys[t.keybinding['right']]:
            if not abs(self.x_vel) > 0:
                self.x_vel = self.walkSpeed
            elif self.position == position['left']:
                self.x_vel = -self.x_vel
            self.position = position['right']
        else:
            self.x_vel = 0

        if keys[t.keybinding['up']]:
            if not abs(self.y_vel) > 0:
                self.y_vel = self.walkSpeed
            elif self.y_vel < 0:
                self.y_vel = -self.y_vel
        elif keys[t.keybinding['down']]:
            if not abs(self.x_vel) > 0:
                self.y_vel = -self.walkSpeed
            elif self.y_vel > 0:
                self.y_vel = -self.y_vel
        else:
            self.y_vel = 0

        if keys[t.keybinding['attack']]:
            if self.z >= 20:
                print('jump cut')
                self.state = self.actionSpace['jumpCut']
                self.frame = 0
        elif keys[t.keybinding['jump']]:
            if self.jumpHigher:
                if self.z_vel > 0:
                    self.z_vel += .5
        if self.frame >= self.frames_num['jump']:
            if self.z > 5:
                self.frame = self.frames_num['jump'] - 2
            else:
                self.state = self.actionSpace['stand']
                self.playRate = 7
                self.frame = 0
                self.z_vel = 0
                self.z = 0
                

    def stick(self,keys):
        self.x_vel = 0.95 * self.x_vel
        self.y_vel = 0.95 * self.y_vel

        if self.frame == 0:
            self.damaged = []


        if self.frame >= self.frames_num['stick']:
            self.state = self.actionSpace['stand']
            self.damaged = []
            self.frame = 0

    def jumpCut(self,keys):
        #self.x_vel = 0
        #self.y_vel = 0
        if self.frame == 0:
            self.damaged = []

        self.allowJump = False
        self.onGround = False
        self.aallowJump = False
        if self.z_vel >= 0:
            self.z_vel =0
        if not self.frame == 0:
            self.z_vel -= self.gAccel * self.dt * 0.3

        if self.z < 0:
            self.z = 0
            self.state = self.actionSpace['stand']
            self.frame = 0

        if self.frame >= self.frames_num['jumpCut']:
            if self.z > 0:
                self.state = self.actionSpace['jump']
                self.frame = 1
            else:
                self.state = self.actionSpace['stand']
                self.frame = 0
            self.damaged = []
            


    def pickOn(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        if self.frame == 0:
            self.damaged = []
        if self.frame >= self.frames_num['pickOn']:
            self.state = self.actionSpace['stand']
            self.frame = 0

    def combo(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        self.playRate = self.atkSpeed 
        
        if self.frame == 0:
            self.damaged = []

        if keys[t.keybinding['attack']]:
            if self.doubleAttack and self.frame >= self.frames_num['combo'] - 2:
                print('Continuous attack')
                self.state = self.actionSpace['con_combo']
                self.frame = 0
        if self.frame >= self.frames_num['combo']:
            self.damaged = []
            self.playRate = 7
            self.frame = 0
            self.state = self.actionSpace['stand']


    def con_combo(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        self.playRate = self.atkSpeed
        
        if self.frame == 0:
            self.damaged = []


        if self.frame >= self.frames_num['con_combo']:
            self.damaged = []
            self.playRate = 7
            self.frame = 0
            self.state = self.actionSpace['stand']

    def swordSkill(self):
        self.x_vel = 0
        self.y_vel = 0
        self.playRate = self.atkSpeed
        
        if self.frame == 0:
            self.damaged = []

        if keys[t.keybinding['swordSkill']]:
            if self.doubleAttack:
                print('combo')

        if self.frame >= self.frames_num['attack']:
            self.damaged = []
            self.playRate = 7
            self.frame = 0


    def hurt(self,keys):
        self.x_vel = 0
        self.y_vel = 0

        self.playRate = 7
        if self.hurtToFall:
            self.state = self.actionSpace['fall']
        
        if self.frame == 0:
            self.repeat = False

        if self.frame >= self.frames_num['hurt']:
            
            if self.repeat:
                self.frame = 4
                self.state = self.actionSpace['hurt']
                self.repeat = False
            else:
                self.frame = 0
                self.playRate = 7
                self.state = self.actionSpace['stand']

    def fall(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        self.playRate = 20
        self.hurtToFall = False
        if self.frame >= self.frames_num['fall']:
            self.state = self.actionSpace['stand']
            self.playRate = 7
            self.frame = 0

    def dead(self,keys):
        self.x_vel = 0
        self.y_vel = 0
        self.isDead = True

        if self.frame >= self.frames_num['dead']:
            self.state = self.actionSpace['dead']
            self.frame = 0

    def animation(self):
        """
            根据当前帧更新精灵image
        """
        n = self.frame
        try:

            if self.position == position['right']:
                if n < len(self.right_frames[self.state]):
                    self.image = self.right_frames[self.state][n]
                else:
                    self.frame -= 1
            else:

                if n < len(self.left_frames[self.state]):
                    self.image = self.left_frames[self.state][n]
                else:
                    self.frame -= 1
        except Exception as e:
            print("捕捉到来自{}异常：{}，当前帧序号为：{}，帧序列长度：{}".format(self.name, e, n,
                                                           len(self.right_frames[self.state])))
            
            
    def update_mask(self):
        jumpCut_mask = self.collidAnchor[self.mask_dic['jumpCut']]
        jumpCut_mask.xy = self.xy
        jumpCut_mask.z = self.z
        jumpCut_mask.pos = self.pos

        self.volumeBox.rect = self.rect
        self.attackBox.rect = self.rect


        if self.state == self.actionSpace['attack']:
            image = self.collidAnchor[self.mask_dic['attack']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 
        elif self.state == self.actionSpace['stick']:
            image = self.collidAnchor[self.mask_dic['stick']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 
        elif self.state == self.actionSpace['jumpCut']:
            image = self.collidAnchor[self.mask_dic['jumpCut']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 
        elif self.state == self.actionSpace['pickOn']:
            image = self.collidAnchor[self.mask_dic['pickOn']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 
        elif self.state == self.actionSpace['combo']:
            image = self.collidAnchor[self.mask_dic['combo']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 
        elif self.state == self.actionSpace['con_combo']:
            image = self.collidAnchor[self.mask_dic['con_combo']].imgs[self.position][self.frame]
            self.attackBox.mask = pygame.mask.from_surface(image) 

        self.mask = pygame.mask.from_surface(self.image) 

