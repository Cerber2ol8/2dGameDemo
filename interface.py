# -*- coding: utf-8 -*-
import pygame
from Src_loader import load_img
#定义一个按钮类
class Button(object):
    def __init__(self, imageUp, imageDown,position,id, name,text=None):
        self.imageUp = imageUp
        self.imageDown = imageDown
        self.position = position
        self.id = id
        self.name = name
        self.isDown = False
        self.text = text
        self.last_down = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('arial', 22)

    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def isClick(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                if pygame.time.get_ticks() - self.last_down > 100:
                    self.last_down = pygame.time.get_ticks()
                    if self.isDown == True:
                        self.isDown = False
                    else:
                        self.isDown = True
    def put_text(self,screen):


        text = self.font.render(self.text, 1, (255, 255, 255))
        w, h = text.get_size()
        x, y = self.position
        pos = (x - w/2, y - h/2)
        screen.blit(text, pos)
        pass

    def render(self, screen):
        w, h = self.imageUp.get_size()
        x, y = self.position

        self.isClick()
        if self.isDown:
            screen.blit(self.imageDown, (x - w/2,y - h/2))
        else:
            screen.blit(self.imageUp, (x - w/2, y - h/2))
        self.put_text(screen)


class UI(pygame.sprite.Sprite):
    def __init__(self,uiImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(uiImg).convert_alpha()
        self.position = [0,0]
        self.last_down = 0

    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.image.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def isClick(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                tick = pygame.time.get_ticks()
                if tick - self.last_down > 50:
                    print('clicked!')

                self.last_down = tick


    def render(self, screen):
        w, h = self.image.get_size()
        x, y = self.position
        screen.blit(self.image, (x - w/2, y - h/2))

class Textbox(object):
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('src/ui/' + 'textbox.png').convert_alpha(),(1024,300))
        self.name = None
        self.id = None
        self.caption = '文本框：'
        self.text = 'This is the first dialogue'
        self.position = (500,600)
        self.textSize = 25
        self.font = pygame.font.SysFont('SimHei', self.textSize)
        self.isShown = True
        self.last_down = pygame.time.get_ticks()

        self.dialogue = []

        self.currText = ''
        self.textList = []
        self.currentDia = 0
        self.textIndex = 0
        self.str = ''   #当前字符
        self.strIndex = 0   #当前字符序号
        self.row = 1    #当前行
        self.rows = 1   #行数
        self.con = True

        self.all = False

        #播放速度控制
        self.count = 0
        self.speed = 5
        self.complete = True

        self.generateDia()
        self.next()
    def generateDia(self):
        dialogue = []
        for i in range(5):
            dialogue.append('dialogue' + str(i))
        #self.dialogue = dialogue
        self.dialogue = ['这是用来测试文本框系统的,点击查看下一条',
                         '这个功能可以用来进行对话',
                         '以及文本描述',
                         '可以用来进行背景叙述、人物对话描写',
                         '文字冒险游戏制作',
                         '对话系统制作',
                         '还有更多暂时想不到了',
                         '还有更多暂时想不到了',
                         '这是个长文本。这是个长文本。这是个长文本。\n这是个长文本。这是个长文本。这是个长文本。这是个长文本。这是个长文本。这是个长\n文本。这是个长文本。这是个长文本。',
                         '这还是个长文本。这还是个长文本。\n这还是个长文本。这还是个长文本。这还是个长文\n本。这还是个长文本。这还是个长文本。这还是个长文本。这还是\n个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。这还是个长文本。'
                         ]
    def isClick(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                tick = pygame.time.get_ticks()
                if tick - self.last_down > 50:
                    if self.isShown:
                        if self.complete:
                            self.next()
                        else:
                            self.all = True

                self.last_down = tick

    def next(self):
        
        
        if self.currentDia >= len(self.dialogue):
            self.currentDia = 0
            self.isShown = False
        else:
            self.text = self.dialogue[self.currentDia]
        self.currentDia += 1
        self.str = ''
        #self.text = ''
        self.strIndex = 0
        self.textIndex = 0
        self.row = 1
        self.all = False
        self.textList, self.rows = self.cut(self.text)

        pass


    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.image.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y


    def render(self, screen):
        w, h = self.image.get_size()
        x, y = self.position

        self.isClick()
        if self.isShown:
            screen.blit(self.image, (x - w/2,y - h/2))
            self.put_text(screen)

    def put_text(self,screen):
        caption = self.font.render(self.caption, 1, (255, 255, 255))
        #text = self.font.render(self.text, 1, (255, 255, 255))
        w, h = self.image.get_size()
        x, y = self.position
        pos = (x - w/2 + 40, y - h/2 + 40)
        screen.blit(caption, (x - w/2 + 20, y - h/2 + 20))
        #screen.blit(text, pos)
        self.play(pos,screen)

        pass

    def _play(self,pos,screen):
        if self.strIndex < len(self.dialogue[self.currentDia]):
            self.str = self.dialogue[self.currentDia][self.strIndex]
            self.strIndex += 1
            if len(self.text)*self.textSize > self.image.get_size()[0]:
                self.text.append(self.str)
                self.textIndex += 1
            else:
                self.text[self.textIndex] += self.str
            self.con = False
        else:
            self.con = True

        for i in range(self.textIndex):
            screen.blit(self.font.render(self.text[self.textIndex], 1, (255, 255, 255)), (pos[0] ,pos[1]+ i * self.textSize))
        #exit()
        pass



    def play(self,pos,screen):
        if self.all:
            for i in range(self.rows):
                #直接显示
                screen.blit(self.font.render(self.textList[i], 1, (255, 255, 255)), (pos[0] ,pos[1]+ i * self.textSize + 2))
                self.complete = True
        else:
            if self.strIndex < len(self.textList[self.row - 1]):
                self.complete = False
                #控制逐字显示速率
                self.count += 1 
                if self.count > 10 / self.speed:
                    self.count = 0
                    self.strIndex += 1
            else:
            
                if self.row < self.rows:
                    self.strIndex = 0
                    self.row += 1
                    self.complete = False
                else:
                    self.complete = True
                

            #将分块后的字符切片
            #print(self.textList[self.row - 1])
            #exit()
            try:
                self.currText = self.textList[self.row - 1][:self.strIndex]
            except:
                print(self.row,self.strIndex)
            if self.row > 1:
                for i in range(self.row - 1):
                    #最后一行之前的直接显示
                    screen.blit(self.font.render(self.textList[i], 1, (255, 255, 255)), (pos[0] ,pos[1]+ i * self.textSize + 2))

            #最后一行逐字显示
            screen.blit(self.font.render(self.currText, 1, (255, 255, 255)), (pos[0] ,pos[1]+ (self.row - 1) * self.textSize + 2))

    def next_line(self, str):
        """寻找文本中的转义换行符，发现换行符则进行换行
        """
        l = []
        i = 0
        j = i

        while(j < len(str)-1):
            if str[j] == "\\"  and str[j+1] == "n":
                l.append(str[i:j])
                if j < len(str)-2:
                    j += 1
                    i = j+1
                print("找到换行符")
            j += 1
        l.append(str[i:])
        return l

    def cut(self,str):
        """
        切割字符串，使之能够实现换行显示
        """
        strlist = []
        print(strlist)
        n = int(self.image.get_size()[0] / self.textSize -1)


        lists = self.new_line(str)
        for l in lists:
            ss = self.next_line(l)
            for s in ss:
                strlist.append(s)

        #段落数
        para = len(strlist)
        rows = 0
        text = []


        for i in range(para):
            #为单段落执行换行
            #rows += int(len(list[i]) / n) + 1
            for j in range(int(len(strlist[i]) / n) + 1):
                text.append(strlist[i][n * j:n + n * j])

        print(text)
        rows = len(text)
        return text,rows
        pass

    def new_line(self,str):
        """返回 使用换行符分割的字符串列表"""
        list = []
        last = 0
        for i in range(len(str)):
            if str[i] == '\n':
                s = str[last:i]
                if not s.startswith('   '):
                    list.append('   ' + s)
                else:
                    list.append(s)
                
                #print(str[last:i])
                last = i+1
                print('换行')




        list.append('   ' +  str[last:i+1])

        #print(str[i:len(str) - 1])
        #print(list)

        return list

        pass