import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State
from pynaccle.utils import *


class Idle(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        self.parent_node.interactingObj = None

    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.draw_surface(position=self.parent_node.spawnLocation)
        # self.parent_node.draw_rect(position=self.parent_node.spawnLocation)

    def collision_check(self,axis:str='y'):

        # if it has been built and taken just continue
        if self.parent_node.interactingObj:
            pass


        if not self.parent_node.interactingObj:

            if self.parent_node.__class__.__name__ == "Wall":
                return

            # find surrounding objects
            self.parent_node.find_surrounding_game_objects()  

            
            # print(objectManager.object_positions[(-224.0, -160.0)])
            # sys.exit()
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

                # only if we have bench specific things to build
                if self.parent_node.buildableObject:

                    # check if the player has the buildable object and the right amouint
                    if self.parent_node.buildableObject not in game_object.collectedParts:
                        self.parent_node.display_message.img_path = f"Wrong work bench"
                
                    
                    elif self.parent_node.buildableObject in game_object.collectedParts:
                        
                        if len(game_object.collectedParts[self.parent_node.buildableObject]) != self.parent_node.buildableData[self.parent_node.buildableObject]['partsNeeded']:
                            self.parent_node.display_message.img_path = f"Not enough parts"
                            
                        
                        elif len(game_object.collectedParts[self.parent_node.buildableObject]) == self.parent_node.buildableData[self.parent_node.buildableObject]['partsNeeded']:
                        
                            # set display message and item image path
                            self.parent_node.display_message.img_path = f"Hold E to interact"
                            self.parent_node.display_item.img_path = self.parent_node.buildableData[self.parent_node.buildableObject]['img_path']

                            # if player is interacting
                            if game_object.is_interacting:
                                self.emit('INTERACTING')
                                self.parent_node.interactingObj = game_object

                # if theres nothing specific that goes 
                elif not self.parent_node.buildableObject:

                    if not game_object.collectedParts:
                        self.parent_node.display_message.img_path = f"Not enough parts"
                

                    elif game_object.collectedParts:

                        # go through all possible buildable objs
                        for buildable in game_object.collectedParts:

                            if len(game_object.collectedParts[buildable]) != self.parent_node.buildableData[buildable]['partsNeeded']:
                                self.parent_node.display_message.img_path = f"Not enough parts"
                                continue
                                
                            elif len(game_object.collectedParts[buildable]) == self.parent_node.buildableData[buildable]['partsNeeded']:

                                # set message and img path
                                self.parent_node.display_message.img_path = f"Hold E to interact"
                                self.parent_node.display_item.img_path = self.parent_node.buildableData[buildable]['img_path']

                                # if player is interacting
                                if game_object.is_interacting:
                                    
                                    self.parent_node.buildableObject = buildable
                                    self.parent_node.interactingObj = game_object
                                    self.emit('INTERACTING')

