import pygame,os,re,math,random,string,sys
import json
from pynaccle.objectsystem import objectManager
from pygame.math import Vector2
from pynaccle.statemachine import State


class Idle(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # clear any interacting objs
        self.parent_node.clear_interactingObj()

        # set new time limit
        # self.parent_node.interactTimer.timer_limit = self.parent_node.stateInteractTimeLimit[self.__class__.__name__.upper()]

    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.submit_to_render()

        # run end contiion
        self.end_condition()


    # collision check
    def collision_check(self,axis:str='y'):

        # find surrounding objects
        self.parent_node.find_surrounding_game_objects()  

        # go through all possible game objects
        for game_object in self.parent_node.surrounding_game_objects:

            # skip collision if game object exists already
            if game_object in self.parent_node.nearbyObjs:
                continue

            # check for collision and handle
            collision,hitbox = self.parent_node.hitbox_collision(game_object=game_object)

            if collision:

                self.handle_collision(game_object=game_object,axis=axis)
                
    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.parent_node.is_active:
            return
        
        if self.parent_node.soulsCollected < self.parent_node.soulsToCollect:

            if game_object.object_of_origin == 'Enemy':

                if game_object.__class__.__name__ == 'Enemy':

                    if game_object not in self.parent_node.nearbyObjs:

                        self.parent_node.nearbyObjs.append(game_object)


        # elif self.parent_node.soulsCollected >= self.parent_node.soulsToCollect:
                
        #     if game_object.object_of_origin == 'Player':

        #         if game_object.__class__.__name__ == 'Player':

        #             if game_object.is_interacting:
        #                 self.state.emit('INTERACTING')

        #             elif not game_object.is_interacting:
        #                 self.state.emit('IDLE')

    # end condition
    def end_condition(self):
        
        if self.parent_node.soulsCollected >= self.parent_node.soulsToCollect:
            self.emit('FILLED')
