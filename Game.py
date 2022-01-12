# -*- coding: utf-8 -*-
import os, sys, gc, argparse
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
from interface import Textbox
from system import System
import time

def start():

    #pygame.key.set_repeat(20)
    global world, camera, icon, player, level, system, clock
    world = GameWorld()
    #world.setup()
    camera = Camera([0,-768],(1024, 768))


    icon = MouseIcon()
    player = Character()
    level = Level_test()
    system = System()
    

    world.setup(level,player,camera,system)

    world.mouseIcon.add(icon)
    #world.level = Level_test()

    from pympler.classtracker import ClassTracker
    global tracker
    tracker = ClassTracker()
    tracker.track_object(world)
    world.tracker = tracker

    spriteTracker = ClassTracker()
    spriteTracker.track_object(world.render)
    world.spriteTracker = spriteTracker

    world.tracker.create_snapshot("world memory usage")
    world.spriteTracker.create_snapshot("sprite memory usage")


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
        #print(dt)
        world.update(dt)
        world.camera.render(world.render)
        #camera.render(pygame.sprite.RenderPlain(icon,world.sprites))

        if world.toReset == True:
            break


    cleanMemery()
    restart()




def cleanMemery():
    from pympler import asizeof

    global world, camera, icon, player, level
    world.tracker.create_snapshot("world memory usage")
    world.spriteTracker.create_snapshot("sprite memory usage")

    world.tracker.stats.print_summary()
    world.spriteTracker.stats.print_summary()

    del camera
    del icon
    del player
    del level
    del world

    gc.collect()
def restart():


    start()
        
    #print('exit')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="set True to switch to debug mode")
    args = parser.parse_args()
    if(args.debug):
        print("debug mode on")
        tools.DEBUG = True
    else:
        tools.DEBUG = False


    pygame.init()
    pygame.display.set_caption('Game_Alpha')
    pygame.mouse.set_visible(0)
    start()
    sys.exit()
