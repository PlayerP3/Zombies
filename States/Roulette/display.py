import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from ...statemachine import State
from ...utils import *
from ...objectsystem import objectManager


class Display(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.interactingObj = None
        self.parent_node.interactTimer.reset_timer()

        self.parent_node.interactTimer.timer_limit = self.parent_node.idleInteractTimerLimit

        # reset timer
        self.parent_node.animationPlayer.timer_speed = 0
        self.parent_node.animationPlayer.currentFrameNumber = self.parent_node.animationPlayer.totalFrames - 1

        # self.parent_node.animationPlayer.animationType = 'reverse'
        self.parent_node.animationPlayer.reset_timer()
        # self.parent_node.animationPlayer.start_timer(startTime=1)

        # reset timer
        self.reset_timer()
        self.start_timer()

        # find final display
        self.parent_node.predetermine_final_display()


    def update(self):

        # run timer
        self.run_timer()

        # set sprite sheet to be idle animation
        self.parent_node.update_position()

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.submit_to_render()
        # self.parent_node.draw_surface(position=self.parent_node.spawnLocation)
        # self.parent_node.draw_rect(position=self.parent_node.spawnLocation)

        # display item
        self.parent_node.displayItem.submit_to_render()

        if self.parent_node.interactTimer.timer_complete:
            
            self.parent_node.pay()
            
            self.emit('RESET')

        elif self.timer_complete:

            self.emit('RESET')
            
    def collision_check(self,axis:str='y'):

        # if nothinbg is interacting
        if not self.parent_node.interactingObj:
                
            # only check for a collision with a purchasing object
            collision,hitbox = self.parent_node.hitbox_collision(game_object=self.parent_node.purchasingObj)

            if collision:

                self.parent_node.interactingObj = self.parent_node.purchasingObj

                self.handle_collision(game_object=objectManager.player,axis=axis)
                

        # if something is interacting already
        elif self.parent_node.interactingObj:

            collision,hitbox = self.parent_node.hitbox_collision(game_object=self.parent_node.interactingObj)

            if collision:


                self.handle_collision(game_object=self.parent_node.interactingObj,axis=axis)

            elif not collision:

                # remove interacting obj
                self.parent_node.interactingObj.is_interacting = False
                self.parent_node.interactingObj = None

                # reset timer
                self.parent_node.interactTimer.reset_timer()


    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.parent_node.is_active:
            return

        # if player is interacting
        if self.parent_node.purchasingObj.is_interacting:

            self.parent_node.interactTimer.start_timer()
            self.parent_node.interactTimer.run_timer()
            
            self.parent_node.interactingObj = self.parent_node.purchasingObj

        # if player not interacting
        elif not objectManager.player.is_interacting:

            self.parent_node.interactTimer.reset_timer()


     # end condition
    def end_condition(self):

        # dont pay up but move to reset
        if self.timer_complete:

            self.parent_node.finalDisply = None

        # pay up
        if self.parent_node.interactTimer.timer_complete:

            # pay up
            self.parent_node.pay(self.purchasingObj)

            # remove final display
            self.parent_node.finalDisplay = None

            self.emit('RESET')