from pynaccle.utils import *
import json
from pynaccle.moveableobject import Moveable_Object
from pynaccle.interactable import Interactable,Idle,Interacting
from wall import Wall
import sys
from pynaccle.tilemap import tilemapProcessor
from pynaccle.objectsystem import objectManager
from pynaccle.pathfinding import *
from pynaccle.animatedsprite import AnimatedSprite

class Part(Interactable):

    def __init__(self,buildableObject:str='RobotBoy'):
        
        self.buildableObject = buildableObject
       
        
        Interactable.__init__(self)
        

    def init(self):

        # display message init
        self.display_message.is_text = True
        self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"
        self.display_message.init_sprite()
        self.display_message.hurtbox.center = (0,0)
        self.display_message.timer_limit = 1
        self.can_collide = False
        self.cost = 0
        

        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost

            # set to inactive
            self.is_active = False

            # add to collected parts foir game obj
            # objectManager.player.collectedParts.append(self.name)
            objectManager.player.collectedParts[self.buildableObject].append(self.name)


    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):
        

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':
                    
                # display message
                self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))

                # if player is interacting
                if game_object.is_interacting:
                    self.state.emit('INTERACTING')

                # if player is interacting
                elif not game_object.is_interacting:
                    self.state.emit('IDLE')

    def update_data(self):

        self.update_position()


class Bench(Interactable):

    

    def __init__(self,partsNeeded:int=3,buildableObject:str=''):

        # parts needed to buidl and name of what the bench builds
        self.partsNeeded = partsNeeded
        self.buildableObject = buildableObject
        self.buildableData = {}
        self.buildableBuilt = False
        self.buildableTaken = False

        Interactable.__init__(self)
        
    def init(self):

        # display message init
        # self.display_message.is_text = True
        # self.display_message.img_path = f"Hold E to buy {self.name} [Cost:{self.cost}]"
        # self.display_message.init_sprite()
        # self.display_message.hurtbox.center = (0,0)
        # self.display_message.timer_limit = 1

        self.display_item = AnimatedSprite()
        self.display_item.zlayer_drawing = self.zlayer_drawing + 1
       
        self.cost = 0
        
        super().init()

    # what happens when pickup is done like changing stats etc
    def pay(self,gameobj):

        if gameobj.money >= self.cost:

            gameobj.money -= self.cost


            # make buildable
            if not self.buildableBuilt:

                # init item sprite
                self.display_item.init_sprite()
                self.display_item.hurtbox.center = (self.hurtbox.centerx,self.hurtbox.centery - 14)

                self.buildableBuilt = True
            
            # give to player
            elif not self.buildableTaken:

                self.display_item.is_active = False
                self.display_message.img_path = ' '
                
                # run effect depending on interactable
                self.run_effect(gameobj=gameobj)
              
                self.buildableTaken = True


            
                

        
    # handle collision once the check is confirmed
    def handle_collision(self,game_object:object,axis:str):

        # if inactive dont bother running code        
        if not self.is_active:
            return

        if game_object.object_of_origin == 'Player':

            if game_object.__class__.__name__ == 'Player':

                # only if we have bench specific things to build
                if self.buildableObject:

                    # check if the player has the buildable object and the right amouint
                    if self.buildableObject not in game_object.collectedParts:
                        self.display_message.img_path = f"Wrong work bench"
                
                    
                    elif self.buildableObject in game_object.collectedParts:
                        
                        if len(game_object.collectedParts[self.buildableObject]) != self.buildableData[self.buildableObject]['partsNeeded']:
                            self.display_message.img_path = f"Not enough parts"
                            
                        
                        elif len(game_object.collectedParts[self.buildableObject]) == self.buildableData[self.buildableObject]['partsNeeded']:
                        
                            # set display message and item image path
                            self.display_message.img_path = f"Hold E to interact"
                            self.display_item.img_path = self.buildableData[self.buildableObject]['img_path']

                            # if player is interacting
                            if game_object.is_interacting:
                                self.state.emit('INTERACTING')

                            # if player is interacting
                            elif not game_object.is_interacting:
                                self.state.emit('IDLE')

                # if theres nothing specific that goes 
                elif not self.buildableObject:

                    if not game_object.collectedParts:
                        self.display_message.img_path = f"Not enough parts"
                  

                    elif game_object.collectedParts:

                        # go through all possible buildable objs
                        for buildable in game_object.collectedParts:

                            if len(game_object.collectedParts[buildable]) != self.buildableData[buildable]['partsNeeded']:
                                self.display_message.img_path = f"Not enough parts"
                                continue
                                
                            elif len(game_object.collectedParts[buildable]) == self.buildableData[buildable]['partsNeeded']:

                                # set message and img path
                                self.display_message.img_path = f"Hold E to interact"
                                self.display_item.img_path = self.buildableData[buildable]['img_path']

                                # if player is interacting
                                if game_object.is_interacting:
                                    
                                    self.state.emit('INTERACTING')

                                # if player is interacting
                                elif not game_object.is_interacting:
                                    self.state.emit('IDLE')

                            
                
                # init sprite
                self.display_message.init_sprite()

                # display message
                self.display_message.draw_surface(position=(self.hurtbox.topright[0]+3,self.hurtbox.topright[1]-3))

                


    def update_data(self):

        self.update_position()

        # if object built then diplsay it
        if self.buildableBuilt:

            # display message
            self.display_item.draw_surface(position=self.display_item.hurtbox.center)




