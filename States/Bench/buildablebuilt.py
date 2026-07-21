import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State
from pynaccle.objectsystem import objectManager
from pynaccle.utils import *


class BuildableBuilt(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.clear_interactingObj()

        self.parent_node.interactingObj = None
        self.parent_node.buildableBuilt = True
        self.parent_node.buildableTaken = False

        # init item sprite
        self.parent_node.buildableSprite.hurtbox.center = (self.parent_node.hurtbox.centerx,self.parent_node.hurtbox.centery - 14)
        
        self.parent_node.display_message.update_message('Hold E to equip')

        # set new time limit
        self.parent_node.interactTimer.timer_limit = self.parent_node.stateInteractTimeLimit[self.__class__.__name__.upper()]


    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()

        # draw item
        self.parent_node.buildableSprite.submit_to_render()

        # draw surface
        self.parent_node.submit_to_render()
        
        self.parent_node.run_interaction_timer()
       
        self.end_condition()

    # wall collision check
    def collision_check(self,axis:str='y'):

        # if we dont have an interacting object
        if not self.parent_node.interactingObj:

            # find surrounding objects
            self.parent_node.find_surrounding_game_objects()

            # filter surrounding objects
            self.parent_node.filter_surrounding_game_objects(['Player'])

            # go through all possible game objects
            for game_object in self.parent_node.surrounding_game_objects: 

                # check for self collision with object
                collision,hitbox = self.parent_node.hitbox_collision(game_object=game_object)

                # if there is a collision
                if collision:

                    if game_object.is_interacting:
                    
                        self.handle_collision(game_object=game_object,axis=axis)

                        # set interacting obj
                        self.parent_node.interactingObj = game_object
 
                    elif not game_object.is_interacting:
                        
                        self.handle_collision(game_object=game_object,axis=axis)


        # if we have an interacting object
        elif self.parent_node.interactingObj:

            # look fror collision
            collision,hitbox = self.parent_node.hitbox_collision(game_object=self.parent_node.interactingObj)

            # the interacting obj stopped interacting
            if not self.parent_node.interactingObj.is_interacting:
                    
                self.parent_node.clear_interactingObj()
                
            # the interacting obj is still interactring
            elif self.parent_node.interactingObj.is_interacting:

                if collision:

                    self.handle_collision(game_object=self.parent_node.interactingObj,axis=axis)

                elif not collision:

                    self.parent_node.clear_interactingObj()
                
        
    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.parent_node.is_active:
            return

        # display message
        # self.parent_node.display_message.hurtbox.center = (game_object.hurtbox.topright[0] + 15,game_object.hurtbox.topright[1] - 15) 
        self.parent_node.display_message.submit_to_render()


    # end condition
    def end_condition(self):

        # pay up
        if self.parent_node.interactTimer.timer_complete:
            self.pay(self.parent_node.interactingObj)
  


    def pay(self,gameobj):

        if gameobj.money >= self.parent_node.cost:

            gameobj.money -= self.parent_node.cost
    
            # run effect depending on interactable
            self.parent_node.give_weapon(gameobj)

            self.emit('BUILDABLETAKEN')


