import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State
from pynaccle.utils import *
from pynaccle.objectsystem import objectManager


class Cycling(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.interactingObj = None
        self.parent_node.interactTimer.reset_timer()

        self.parent_node.interactTimer.timer_limit = self.parent_node.idleInteractTimerLimit

        self.parent_node.animationPlayer.timer_speed = 10
        self.parent_node.animationPlayer.animationType = 'forward'
        self.parent_node.animationPlayer.currentFrameNumber = 0
        self.parent_node.animationPlayer.reset_timer()
        self.parent_node.animationPlayer.start_timer()

        # reset timer
        self.reset_timer()
        self.start_timer()

    def update(self):

        # run timer
        self.run_timer()

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.submit_to_render()

        # if timer is complete emit cycling
        if self.timer_complete:

            self.emit('DISPLAY')


    def collision_check(self,axis:str='y'):

        pass

    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

       pass