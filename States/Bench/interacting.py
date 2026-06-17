import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State
from pynaccle.objectsystem import objectManager


class Interacting(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # change display message spirte


        # set sprite sheet to be idle animation
        self.timer_limit = self.parent_node.interact_time_limit
        self.timer_init()
        

    def update(self):

        # run interaction timer
        self.run_timer()

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()


        # check if player is in colliding objects
        # if pynaccle.player in self.parent_node.surrounding_game_objects:
        #     pass
            # display message
            # self.parent_node.display_message.draw_surface(position=(self.parent_node.hurtbox.topright[0]+3,self.parent_node.hurtbox.topright[1]-3))

        
        if self.timer_complete:

            self.parent_node.pay(gameobj=self.parent_node.interactingObj)

        elif not self.parent_node.interactingObj.is_interacting:

            if not self.parent_node.buildableBuilt and not self.parent_node.buildableTaken:
                self.emit('IDLE')

            elif self.parent_node.buildableBuilt and not self.parent_node.buildableTaken:
                self.emit('BUILDABLEBUILT')

            elif self.parent_node.buildableBuilt and self.parent_node.buildableTaken:
                self.emit('BUILDABLETAKEN')


        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.spawnLocation)
        # self.parent_node.draw_rect(position=self.parent_node.spawnLocation)


    def collision_check(self):
        pass

        

