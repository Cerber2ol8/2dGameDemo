from interface import UI,Textbox
import pygame
from Src_loader import load_img
from GameObject import GameObject
class Bag(UI):
    def __init__(self):
        uiImg = 'src/ui/bag.png'
        UI.__init__(self,uiImg)
        self.index = 0
        self.isOpen = False
        self.capacity = 10
        self.grids = 5
        self.info = None
        self.contain = []
        self.enable = True
        self.position = [500,400]
        self.distance = [0,0]
        self.subWidget =[]
        self.onClick = False
        self.onDrag = False
    def init(self):
        #载入背包信息 
        self.load()
    def getInfo(self,info):
        self.info = info
    def load(self):
        for info in self.info:

            content = BagContent(info[0],self.index,number=info[1])
            self.contain.append(content)
            self.index += 1



    def join(self,itemId):
        pass

    def select(self):

        pass
    def sort(self):
        pass

    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        left = x - self.image.get_size()[0]/2
        top = y - self.image.get_size()[1]/2
        w = self.image.get_size()[0]
        h = 100
        in_x = left < point_x < left + w
        in_y = top < point_y < top + h
        res =  in_x and in_y
        if res:
            pass
            #print(left,top)
        return res



    def drag(self):

        b1,b2,b3 = pygame.mouse.get_pressed()
        if b1 == 1:
            if self.isOver() or self.onDrag:
                px, py = pygame.mouse.get_pos()
                x, y = self. position
                w, h = self.image.get_size()[0], self.image.get_size()[1]
                left = x - w/2
                top = y - h/2
                if self.onClick == False:
                    
                    self.distance = [px-left,py-top]
                    self.onClick = True
                    self.onDrag = True
                    #print(self.distance)

                else:
                    x = px-self.distance[0] + w/2
                    y = py-self.distance[1] + h/2
                    #print(x,y)
                    self.position = [x,y]
                                     
        else:
            self.onClick = False
            self.onDrag = False
        pass
    def update(self):
        self.drag()
        pass
    def render(self, screen):
        if self.isOpen and self.enable:
            w, h = self.image.get_size()
            x, y = self.position
            left = x - w/2
            top = y - h/2
            screen.blit(self.image, (left, top))
            wi,hi = 26,36
            rows = self.index%self.grids
            i = 0
            while i < self.index:
                xi = left + 45 + i*36
                yi = top + 115
                if self.info != None:
                    content = self.contain[i]
                    self.contain[i].position = [xi,yi]
                    self.contain[i].isClick()
                    if self.contain[i].toDestory:
                        del self.contain[i]
                        if i > 0:
                            i -= 1
                        self.index -= 1
                        continue
                    else:
                        screen.blit(content.image,(xi,yi))
                        if content.selected == True:
                            rect = (content)
                            #pygame.draw.rect(screen,(0,0,255),sprite.rect,1)
                        #显示道具数量
                        screen.blit(content.font.render(str(content.number), 
                                    1, (255, 255, 255)), 
                                    (xi ,yi + 36 - content.textSize))
                        i += 1
                else:
                    break
                    print('No Item Info')

    pass
class BagContent(UI):
    def __init__(self,item,index,number):
        self.item = item
        UI.__init__(self,'src/ui/' + self.item.img)
        self.index = index
        self.number = number
        self.usable = self.item.usable
        self.position = [0,0]
        self.selected = False
        self.toDestory = False
        self.textSize = 10
        self.font = pygame.font.SysFont('SimHei', self.textSize)
        self.draging = False
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = 26,36

        in_x = x < point_x < x + w
        in_y = y < point_y < y + h
        return in_x and in_y


    def isClick(self):
        if self.isOver():
            self.selected = True
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                tick = pygame.time.get_ticks()
                if tick - self.last_down > 50:
                    if self.number > 0:
                        self.item.use()
                        self.number -= 1
                        print('use ' + str(self.item.name) + 'x1, ' + str(self.number) + 'last')
                        if self.number == 0:
                           self.toDestory = True
                self.last_down = tick
        else:
            self.selected = False

class Item(object):
    def __init__(self,id, img, name, text, usage, usable):
        self.id = id
        self.img = img
        self.name = name
        self.text = text
        self.usage = usage
        self.sub = None
        self.target = None
        self.usable = usable
    def bindSub(self,sub, target):
        self.sub = sub
        self.target = target

        pass
    def use(self,*args):
        if self.sub != None:
            self.sub(self.target)

        else:
            print('No sub binding')
    pass

class System(object):
    def __init__(self):
        self.bag = Bag()
        self.world = None
        self.ui = None

    def setup(self,world):
        self.world = world
        #暂时用背包代替ui显示
        self.ui = self.bag

        self.loadItem()
        self.bag.init()

    def update(self):
        self.ui.update()


    def loadItem(self):
        HealthDrag = Item(1,'drag.png','Healing potion','heal 50 health','click to use',True)

        HealthDrag.bindSub(self.heal(),self.world.player)

        ItemList = []
        templete1 = [HealthDrag,2]
        templete2 = [HealthDrag,3]
        templete3 = [HealthDrag,5]
        ItemList.append(templete1)
        ItemList.append(templete2)
        ItemList.append(templete3)

        self.bag.getInfo(ItemList)
    def heal(self):
        
        def wrapper(target):
            print('heal 50 hp')
            target.get_heal(50)
            #return func(*args,**kwargs)    # 此处若返回引用，则被装饰函数不执行
        return wrapper