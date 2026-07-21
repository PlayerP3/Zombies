import pygame,os,re,math,random,string,sys
import json
from pygame.math import Vector2
from pynaccle.statemachine import State
from pynaccle.utils import *
from pynaccle.objectsystem import objectManager
from pynaccle.inventory import gameInventory

class Idle(State):

    def __init__(self):

        State.__init__(self)

    def enter(self):

        # set new time limit
        self.parent_node.interactTimer.timer_limit = self.parent_node.stateInteractTimeLimit[self.__class__.__name__.upper()]
        
        self.buildableToRemove = None

        self.parent_node.clear_interactingObj()
        

    def update(self):

        # set sprite sheet to be idle animation
        self.parent_node.update_data()  

        # run move and collide, end condition is in here
        self.parent_node.move_and_collide()  

        # draw surface
        self.parent_node.submit_to_render()

        # run interact timer
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
        
        # if no buildable has even been picked up
        if 'buildable' not in gameInventory.inventory:
            return
            
        # if a buildable has been picked up
        # if no buildable has even been picked up
        elif 'buildable' in gameInventory.inventory:
            
            # regardless of if interact
            if self.parent_node.buildableObject:

                # check if the player has the buildable object and the right amouint
                if self.parent_node.buildableObject not in gameInventory.inventory['buildable']:
                    self.parent_node.display_message.update_message("Wrong work bench")
            
                
                elif self.parent_node.buildableObject in gameInventory.inventory['buildable']:

                    if len(gameInventory.inventory['buildable'][self.parent_node.buildableObject]) != self.parent_node.buildableData[self.parent_node.buildableObject]['partsNeeded']:
                        self.parent_node.display_message.update_message("Not enough parts")      
                    
                    elif len(gameInventory.inventory['buildable'][self.parent_node.buildableObject]) == self.parent_node.buildableData[self.parent_node.buildableObject]['partsNeeded']:
                    
                        # set display message and item image path
                        self.parent_node.display_message.update_message(f"Hold E to interact")
                        self.parent_node.buildableSprite.img_path = self.parent_node.buildableData[self.parent_node.buildableObject]['img_path']
                        

            # if theres nothing specific that goes 
            elif not self.parent_node.buildableObject:
            
                if not gameInventory.inventory['buildable']:
                    self.parent_node.display_message.update_message(f"Not enough parts")
                    
                elif  gameInventory.inventory['buildable']:

                    # go through all possible buildable objs
                    for buildable in gameInventory.inventory['buildable']:

                        if len(gameInventory.inventory['buildable'][self.parent_node.buildableObject]) != self.parent_node.buildableData[buildable]['partsNeeded']:
                            self.parent_node.display_message.update_message("Not enough parts")
                            continue
                            
                        elif len(gameInventory.inventory['buildable'][self.parent_node.buildableObject]) == self.parent_node.buildableData[buildable]['partsNeeded']:

                            # set message and img path
                            self.parent_node.display_message.update_message(f"Hold E to interact")
                            self.parent_node.buildableSprite.img_path = self.parent_node.buildableData[buildable]['img_path']

                            # set buildable to be whatever buidlable we are currently cycling throughj
                            self.parent_node.buildableObject = buildable

                            break

        # draw display message if colliding             
        self.parent_node.display_message.submit_to_render()

    def end_condition(self):
        
        if self.parent_node.interactTimer.timer_complete:

            # remove buildable
            # del objectManager.player.collectedParts[self.parent_node.buildableObject]

            self.emit('BUILDABLEBUILT')