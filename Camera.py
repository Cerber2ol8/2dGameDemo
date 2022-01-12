# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from pygame.transform import scale
class Camera(object):
    """摄像机类"""
    def __init__(self,pos, resolution):
        self.name = 'camera'
        self.screen = pygame.display.set_mode(resolution)
        self.res = resolution
        self.area = self.screen.get_rect()
        self.width = self.area.width
        self.height = self.area.height
        self.pos = (self.width/2, self.height/2) #摄像机下的局部坐标 x',y'
        self.Cxy = (0, 0)   #摄像机坐标原点 x0,y0          x = x0 + x'  y = y0 + y'
        self.xy = [self.pos[0]+self.Cxy[0], self.pos[1]+self.Cxy[1]] #摄像机全局坐标
        self.background_bottom = pygame.Surface(self.screen.get_size())
        self.background_bottom = self.background_bottom.convert()
        self.background_bottom.fill((0,0,0))
        #self.screen.blit(self.background_bottom, (0, 0))
        pygame.display.flip()
        
        #self.rect = pygame.Rect(0,0,3000,3000)
        self.surface = pygame.Surface((4000,4000))

    def render(self,sprites):
        "在屏幕上一层一层叠加图像"
        #self.screen.blit(self.background_bottom, (0, 0))
        #self.surface.blit(self.background_bottom, (0, 0))
        #sprites.draw(self.surface)
        img = self.surface.subsurface((self.Cxy[0],self.Cxy[1],self.res[0],self.res[1]))
        self.screen.blit(img,(0,0))
        sprites.draw(self.screen)

        #pygame.display.flip()
        sprites.empty()

    def putText(self,text,pos):
        "在摄像机前显示文本"
        if text == None:
            pass
        else:
            if pygame.font:
                font = pygame.font.SysFont('arial', 36)
                text = font.render(text, 1, (255, 255, 255))
                if pos == None:
                    pos = text.get_rect(centerx=self.background_bottom.get_width()/2)
                self.screen.blit(text, pos)




    def move(self,Wx,Wy):
        """移动镜头到世界坐标系的位置"""
        self.xy = [Wx,Wy]



    def update(self):
        #self.xy = self._getXy()
        pass
            
        #exit()

    def _getXy(self):
        """得到摄像机的世界坐标"""
        xc = self.pos[0]
        yc = self.pos[1]
        """ y'=-(y-y0)  x' = x-x0
            y =-(y'-y0) x  = x'+x0
            摄像机坐标原点的世界坐标 (x0,y0) Cxy
            摄像机下的局部坐标 (x',y') pos
        """
        xw = xc + self.Cxy[0]
        yw = yc + self.Cxy[1]
        return[xw,yw]
    def focus(self,sprites):
        dx = sprites.xy[0] - self.xy[0]
        dy = sprites.xy[1] - self.xy[1]
        self.scroll(dx, dy)

    def scroll(self, dx, dy):
        #self.Cxy[0] += dx
        self.xy[0] += dx
        #self.Cxy[1] += dy
        self.xy[1] += dy

    def scroll_view(self, zoom_factor, image, direction, view_rect):
        """(int,surface,surface,int,rect)"""
        dx = dy = 0
        src_rect = None
        zoom_view_rect = self.screen.get_clip()
        image_w, image_h = image.get_size()
        if direction == 0:
            if view_rect.top > zoom_factor:
                self.screen.scroll(dy=zoom_factor)
                view_rect.move_ip(0, -zoom_factor)
                src_rect = view_rect.copy()
                src_rect.h = zoom_factor
                dst_rect = zoom_view_rect.copy()
                dst_rect.h = zoom_factor
        elif direction == 2:
            if view_rect.bottom < image_h-zoom_factor:
                self.screen.scroll(dy=-zoom_factor)
                view_rect.move_ip(0, zoom_factor)
                src_rect = view_rect.copy()
                src_rect.h = zoom_factor
                src_rect.bottom = view_rect.bottom
                dst_rect = zoom_view_rect.copy()
                dst_rect.h = zoom_factor
                dst_rect.bottom = zoom_view_rect.bottom
        elif direction == 1:
            if view_rect.left > zoom_factor:
                self.screen.scroll(dx=zoom_factor)
                view_rect.move_ip(-zoom_factor, 0)
                src_rect = view_rect.copy()
                src_rect.w = zoom_factor
                dst_rect = zoom_view_rect.copy()
                dst_rect.w = zoom_factor
        elif direction == 3:
            if view_rect.right < image_w-zoom_factor:
                self.screen.scroll(dx=-zoom_factor)
                view_rect.move_ip(zoom_factor, 0)
                src_rect = view_rect.copy()
                src_rect.w = zoom_factor
                src_rect.right = view_rect.right
                dst_rect = zoom_view_rect.copy()
                dst_rect.w = zoom_factor
                dst_rect.right = zoom_view_rect.right
        if src_rect is not None:
            scale(image.subsurface(src_rect),
                  dst_rect.size,
                  self.screen.subsurface(dst_rect))
            pygame.display.update(zoom_view_rect)



