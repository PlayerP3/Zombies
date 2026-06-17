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

        self.parent_node.interactingObj.is_interacting = False
        self.parent_node.interactingObj = None
        self.parent_node.buildableBuilt = True

        # init item sprite
        self.parent_node.display_item.is_active = True
        self.parent_node.display_item.init_sprite()
        self.parent_node.display_item.hurtbox.center = (self.parent_node.hurtbox.centerx,self.parent_node.hurtbox.centery - 14)
        
        self.parent_node.display_message.img_path = 'Hold E to equip'
        self.parent_node.display_message.init_sprite()

        
        self.timer_limit = self.parent_node.interact_time_limit
        self.timer_init()
        

    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()

        # draw item
        self.parent_node.display_item.draw_surface(position=self.parent_node.display_item.hurtbox.center)
        
        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.spawnLocation)
        # self.parent_node.draw_rect(position=self.parent_node.spawnLocation)


    # wall collision check
    def collision_check(self,axis:str='y'):

        # if nothing in interacting
        if not self.parent_node.interactingObj:

           

            if self.parent_node.__class__.__name__ == "Wall":
                return

            # find surrounding objects
            self.parent_node.find_surrounding_game_objects()  
            
            # go through all possible game objects
            for game_object in self.parent_node.surrounding_game_objects:

                if not game_object.can_collide:
                    continue

                # if wall/door use hirtbox collision instead of hitbox
                if array_is_in_array(get_mro(gameObject=game_object),['Wall','Interactable']): 

                    # rect collision check
                    if self.parent_node.hurtbox.colliderect(game_object.hurtbox):

                        # handle collision
                        self.handle_collision(game_object=game_object,axis=axis)

                else:
                   
                    collision,hitbox = self.parent_node.hitbox_collision(game_object=game_object)

                    if collision:

                        self.handle_collision(game_object=game_object,axis=axis)
                        self.parent_node.interactingObj = game_object

        # if something is interacting already
        elif self.parent_node.interactingObj:

            

            collision,hitbox = self.parent_node.hitbox_collision(game_object=self.parent_node.interactingObj)

            if collision:

                self.handle_collision(game_object=self.parent_node.interactingObj,axis=axis)

            elif not collision:

                # remove interacting obj
                self.parent_node.interactingObj.is_interacting = False
                self.parent_node.interactingObj = None
                


        
    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.parent_node.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                
                # if player is interacting
                if game_object.is_interacting:
                    self.emit('INTERACTING')
                
                # display message
                self.parent_node.display_message.draw_surface(position=(self.parent_node.hurtbox.topright[0]+3,self.parent_node.hurtbox.topright[1]-3))